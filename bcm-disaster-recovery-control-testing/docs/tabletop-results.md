# Tabletop Exercise Results

## Exercise Summary

A simulated corruption event affecting the primary transaction database was reviewed using the established disaster-recovery process.

The exercise tested:

- incident detection
- escalation
- disaster declaration
- failover authorization
- recovery-path selection
- communication responsibilities
- alignment to RTO and RPO objectives

## Recovery Objectives

| Metric | Target |
|---|---:|
| RTO | 15 minutes |
| RPO | 5 minutes |
| MTD | 4 hours |

## Timeline

| Time | Event | Decision / Action |
|---|---|---|
| 14:00 | Primary storage corruption begins | No action yet |
| 14:05 | Application errors begin | Monitoring expected to detect degradation |
| 14:20 | Incident formally detected | Recovery clock initiated |
| 14:23 | Primary storage failure confirmed | Repair viability assessed |
| 14:25 | Secondary replica confirmed available | Replica selected as preferred recovery source |
| 14:27 | Disaster declared | Failover authorized |
| 14:29 | Secondary activation begins | Failover procedure executed |
| 14:33 | Secondary service validated | Recovery declared successful |

## Tabletop RTO Assessment

Recovery timeline measured from formal detection at 14:20 to validated service at 14:33:

    13 minutes

Target:

    15 minutes

Result:

    PASS

The tabletop recovery sequence is capable of meeting the stated RTO when decisions are made without unnecessary delay.

## Tabletop RPO Assessment

Replication cadence:

    5 minutes

Target:

    5 minutes

Expected maximum transaction-loss window:

    <= 5 minutes

Result:

    PASS by design

This result must still be validated during the live technical failover exercise.

## Decisions Made

### Decision 1 — Declare Disaster

The event qualifies as a disaster because primary storage integrity cannot be trusted and repair time may exceed the remaining RTO window.

### Decision 2 — Use Secondary Replica First

The rsync secondary replica is selected as the primary recovery source.

Rationale:

- data already staged
- minimal recovery preparation
- lowest expected RTO
- no full restore operation required

### Decision 3 — Retain Restic as Secondary Recovery Path

Restic is retained as a separate recovery mechanism for:

- historical recovery
- corruption propagated to replica
- accidental deletion
- secondary-copy integrity failure

## Gaps Identified

### Gap 1 — Detection Delay

The scenario assumes corruption begins at 14:00 but is not formally detected until 14:20.

Risk:

A 20-minute detection delay already exceeds the 15-minute RTO if the RTO clock is interpreted from actual service disruption rather than disaster declaration.

Risk Rating:

    High

Recommended action:

Implement automated workload-health monitoring and define exactly when the RTO measurement clock begins.

### Gap 2 — Same-Host Primary and Secondary Storage

Both primary and secondary recovery locations exist on the same VM.

Risk:

A host-level failure could affect both copies.

Risk Rating:

    High

Recommended action:

Move the secondary replica and backup repository to separate infrastructure in production.

### Gap 3 — Replication Can Propagate Corruption

rsync uses deletion synchronization.

Risk:

Primary corruption or deletion may be propagated to the secondary copy before recovery begins.

Risk Rating:

    High

Recommended action:

Retain independent versioned restic snapshots and consider delayed or immutable replication for production.

### Gap 4 — Manual Disaster Declaration

Failover requires a human decision.

Risk:

Approval delays may reduce available recovery time.

Risk Rating:

    Moderate

Recommended action:

Define explicit disaster-declaration thresholds and pre-authorized recovery conditions.

### Gap 5 — SQLite Backup Consistency

The workload may be active when backup or replication occurs.

Risk:

Copying a live database file without an application-consistent snapshot mechanism may result in inconsistent recovery data.

Risk Rating:

    High

Recommended action:

Use SQLite online backup capability, checkpointing, or another application-consistent backup method before copying the database.

## Action Items

| ID | Action | Owner | Priority | Target |
|---|---|---|---|---|
| TT-001 | Define RTO clock-start policy | Incident Coordinator | High | 30 days |
| TT-002 | Add automated health monitoring | Platform Engineer | High | 30 days |
| TT-003 | Separate production DR storage from primary host | Platform Engineer | High | 60 days |
| TT-004 | Implement application-consistent SQLite backup | Application Owner | High | 30 days |
| TT-005 | Define pre-authorized failover thresholds | Business Owner | Medium | 45 days |
| TT-006 | Evaluate immutable/versioned secondary recovery copies | Risk/Control Owner | Medium | 60 days |

## Control Observations

### CP-2

Recovery objectives, recovery resources, and responsible roles are defined.

Observation:

The recovery strategy is documented but requires clarification of the official RTO clock-start point.

### CP-4

The contingency plan is exercised through a structured tabletop.

Observation:

Decision-making and communication paths are functional, but detection delay represents a material weakness.

### CP-9

Backup and recovery mechanisms are defined.

Observation:

Encrypted restic snapshots provide versioned recovery protection; live SQLite consistency requires additional validation.

### CP-10

Reconstitution procedures are defined around secondary workload activation.

Observation:

The planned failover sequence appears capable of meeting the 15-minute RTO but requires live technical validation.

## Exercise Conclusion

The tabletop demonstrates that the recovery design is operationally viable, but several deficiencies require remediation.

The most significant findings are:

1. detection delay can consume or exceed the recovery objective
2. primary and secondary recovery locations share a common host
3. replication may propagate corruption
4. live SQLite consistency requires stronger controls

The next stage is a functional failover test to determine actual RTO, actual recoverable data state, and service integrity.
