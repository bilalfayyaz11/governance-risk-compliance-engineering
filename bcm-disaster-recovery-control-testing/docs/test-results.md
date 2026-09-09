# BCM / Disaster Recovery Test Results

## Recovery Objectives

| Metric | Target |
|---|---:|
| RTO | 15 minutes |
| RPO | 5 minutes |
| MTD | 4 hours |

## Functional Failover

The primary workload data was intentionally removed after creating a controlled known-good backup and replicated recovery point.

The secondary workload was started from the replicated data location and validated through its HTTP health endpoint and transaction database.

Result:

    PASS

## RTO

Target:

    <= 15 minutes

Measured recovery timing is retained in:

    evidence/failover-timing.txt
    evidence/technical-test-summary.txt

Result:

    PASS

## RPO

Target:

    <= 5 minutes

Recovery-point timing is retained in:

    evidence/rpo-calculation.txt

Result:

    PASS

## Data Integrity

Validation included:

- transaction count
- maximum transaction identifier
- SHA-256 comparison
- application query response

Result:

    PASS

## Backup Recovery

The encrypted restic repository was independently restored and validated.

Evidence includes:

    evidence/restic-check.txt

Result:

    PASS

## Tabletop Exercise

Result:

    PASS WITH FINDINGS

The tabletop identified deficiencies involving:

- delayed detection
- shared failure domain
- corruption propagation
- manual disaster declaration
- active SQLite consistency

## Control Results

| Control | Assessment |
|---|---|
| CP-2 | PASS WITH FINDINGS |
| CP-4 | PASS |
| CP-9 | PASS WITH FINDINGS |
| CP-10 | PASS |

## Overall Result

    PASS WITH FINDINGS

The recovery implementation satisfies the defined recovery objectives in the controlled environment while retaining documented deficiencies that require remediation before production reliance.
