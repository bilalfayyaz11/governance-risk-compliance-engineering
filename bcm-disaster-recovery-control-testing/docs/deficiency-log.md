# BCM / DR Deficiency Log

| ID | Control | Deficiency | Risk | Root Cause | Owner | Target | Status |
|---|---|---|---|---|---|---|---|
| DR-001 | CP-2 / CP-10 | Primary and secondary recovery data share one host | High | Single-host architecture | Platform Engineering | 60 days | Open |
| DR-002 | CP-9 | Replication can propagate deletion or corruption | High | Mirror-based replication | Platform Engineering | 45 days | Open |
| DR-003 | CP-4 / CP-10 | Detection delay can consume RTO | High | Missing automated alerting | Operations | 30 days | Open |
| DR-004 | CP-9 | Live SQLite copies may lack application consistency | High | Filesystem-level copying | Application Owner | 30 days | Open |
| DR-005 | CP-2 | Disaster declaration relies on manual judgment | Moderate | Undefined automated thresholds | Continuity Manager | 45 days | Open |
| DR-006 | CP-9 | Backup repository credentials reside on recovery host | Moderate | Test-environment design | Security / Platform | 60 days | Open |

## DR-001 — Shared Failure Domain

Production recovery data should be moved to separate infrastructure so a complete host failure cannot remove primary data, secondary data, and historical backups simultaneously.

## DR-002 — Replicated Corruption

The secondary replica should not be treated as a historical backup.

Production controls should evaluate:

- immutable recovery points
- delayed replication
- retention locking
- object versioning

## DR-003 — Detection Delay

Automated health monitoring should initiate escalation close to the actual service interruption.

The RTO clock should begin at business service disruption rather than formal disaster declaration.

## DR-004 — Application Consistency

Production SQLite protection should use an application-consistent method such as:

- SQLite backup API
- controlled checkpointing
- quiesced backup
- application-aware snapshot

## DR-005 — Failover Authorization

Document explicit pre-authorized failover conditions such as:

- storage corruption
- loss of data integrity
- recovery estimate exceeding available RTO
- repeated service-health failure

## DR-006 — Credential Separation

Production restic credentials should use centralized secrets management and be separated from the backup repository.
