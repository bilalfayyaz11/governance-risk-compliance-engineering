# Business Impact Analysis

## Critical Business Process

The protected workload represents a transaction-processing service that records business transactions in a persistent SQLite database and exposes operational health and transaction data through an HTTP service.

The process is considered business-critical because loss of availability or transaction data directly affects the organization's ability to record completed business activity and maintain an accurate operational record.

## Key Dependencies

| Dependency | Requirement |
|---|---|
| Compute | Linux host capable of running Docker |
| Container Runtime | Docker Engine |
| Application Image | `dr-stateful-workload:1.0` |
| Persistent Data | SQLite database stored on mounted host storage |
| Network | Local HTTP service availability |
| Backup Platform | restic repository |
| Replication Platform | rsync secondary copy |
| Scheduling | cron/systemd automation |
| Staff | Platform/operations responder with failover authority |

## Impact Analysis

Impact ratings use:

- Low
- Moderate
- High
- Severe

| Outage Duration | Financial | Operational | Reputational | Regulatory | Overall |
|---|---|---|---|---|---|
| 1 hour | Low | Moderate | Low | Low | Moderate |
| 4 hours | Moderate | High | Moderate | Moderate | High |
| 24 hours | High | Severe | High | High | Severe |
| 72 hours | Severe | Severe | Severe | Severe | Severe |

## Impact Rationale

### 1 Hour

A one-hour outage causes delayed transaction processing but is still recoverable through operational workarounds. Financial impact remains limited, though the inability to record new transactions creates moderate operational disruption.

### 4 Hours

At four hours, transaction backlog and reconciliation effort become significant. Operational impact becomes high, with increasing financial and compliance exposure if records cannot be restored accurately.

### 24 Hours

A full-day outage creates unacceptable disruption. Transaction history may become incomplete, recovery effort increases substantially, and management may need to invoke formal continuity procedures.

### 72 Hours

A multi-day outage represents a severe business continuity failure with material operational, financial, reputational, and regulatory consequences.

## Recovery Time Objective

**RTO: 15 minutes**

The workload must be restored or failed over within 15 minutes of disaster declaration.

### RTO Rationale

The impact analysis shows that disruption becomes progressively serious well before the four-hour mark. Because a pre-staged secondary data location and container image are available, a 15-minute technical failover objective is achievable and substantially reduces exposure.

The failover design therefore uses:

- pre-existing container image
- continuously replicated data
- scripted shutdown and secondary startup
- automated service-health validation

These mechanisms eliminate lengthy manual rebuild steps.

## Recovery Point Objective

**RPO: 5 minutes**

No more than five minutes of committed transaction data should be lost.

### RPO Rationale

The workload receives transactions continuously. Losing several hours of data would create reconciliation and integrity problems.

A five-minute RPO balances:

- transaction frequency
- recovery complexity
- resource usage
- operational risk

Replication and backup scheduling must therefore execute at least every five minutes.

The rsync replication path will provide the primary near-real-time recovery copy, while restic will provide encrypted historical recovery points.

## Maximum Tolerable Downtime

**MTD: 4 hours**

The organization can temporarily tolerate degraded operations, but the BIA rates operational impact as High at four hours.

The MTD is therefore set at four hours. Recovery procedures must restore service well before this threshold.

Relationship:

    RTO = 15 minutes
    MTD = 4 hours

The RTO provides significant recovery margin before business impact reaches the MTD.

## Data Recovery Requirement

The business process requires:

- transaction database integrity
- preservation of committed transaction records
- ability to validate recovered records
- encrypted historical backup copies
- independently replicated secondary data

The RPO decision therefore requires:

    replication cadence <= 5 minutes
    backup cadence <= 5 minutes

## Resource Requirements

### Staff

- Incident/continuity coordinator
- Platform or systems administrator
- Application owner
- Risk/control owner
- Business process owner

### Systems

- Linux host
- Docker
- SQLite
- restic
- rsync
- cron or equivalent scheduler
- curl/jq for validation

### Data

Critical recovery data consists primarily of:

    workload/data/transactions.db

Supporting evidence includes:

- transaction logs
- replication logs
- backup snapshots
- recovery timing logs
- integrity checksums

## Recovery Strategy

### Primary Recovery Path

Fail over to the continuously replicated secondary data copy.

Target:

    RTO <= 15 minutes
    RPO <= 5 minutes

### Secondary Recovery Path

Restore the most recent encrypted restic snapshot.

This recovery path protects against:

- primary storage loss
- accidental deletion
- corruption propagated to the secondary replica
- requirement for historical recovery points

## Control Decision Summary

| Requirement | Target | BIA Basis |
|---|---:|---|
| RTO | 15 minutes | Operational impact increases rapidly and becomes High by 4 hours |
| RPO | 5 minutes | Continuous transactions make larger data-loss windows unacceptable |
| MTD | 4 hours | High operational impact reached at 4-hour outage interval |
| Replication Cadence | <= 5 minutes | Must satisfy RPO |
| Backup Cadence | <= 5 minutes | Must maintain recoverable historical state |
| Failover Method | Scripted secondary startup | Must satisfy 15-minute RTO |

## Conclusion

The BIA demonstrates that recovery objectives are derived from business impact rather than selected arbitrarily.

The 15-minute RTO is supported by scripted failover to pre-replicated data, while the five-minute RPO drives both backup and replication cadence. The four-hour MTD represents the point at which operational impact becomes unacceptable and provides the upper boundary for continuity planning.
