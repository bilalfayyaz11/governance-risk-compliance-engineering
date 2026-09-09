# BCM / Disaster Recovery Test Plan

## Scope

This assessment validates business continuity and disaster recovery controls for a stateful containerized transaction-processing workload.

Testing covers:

- Business Impact Analysis
- backup and restoration
- secondary replication
- tabletop exercise
- destructive failover
- service reconstitution
- data integrity
- RTO/RPO measurement
- deficiency identification

## Recovery Objectives

| Metric | Target |
|---|---:|
| RTO | 15 minutes |
| RPO | 5 minutes |
| MTD | 4 hours |

## Test Types

### Tabletop

Validate:

- detection
- escalation
- disaster declaration
- RACI responsibilities
- communication
- failover authorization

### Functional Recovery

Validate:

- destructive primary-data loss
- secondary workload activation
- HTTP availability
- transaction recovery
- integrity checks
- recovery timing

### Backup Restore

Restore the latest encrypted restic snapshot independently from the replicated recovery path.

## Success Criteria

RTO passes when:

    Actual RTO <= 900 seconds

RPO passes when:

    Actual RPO <= 300 seconds

Service availability passes when:

    Failover health endpoint returns HTTP 200

Data integrity passes when:

- recovered transaction state matches the known-good baseline
- recovered data is queryable
- integrity evidence is retained

Backup recovery passes when:

- restic snapshots exist
- repository validation succeeds
- latest snapshot restores successfully

## Evidence

Evidence is retained under:

    docs/evidence/

The single-host environment validates recovery mechanics but does not represent true site-level resilience.
