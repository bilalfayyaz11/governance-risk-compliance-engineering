# Technical Failover Test Results

## Test Objective

Validate that the containerized transaction workload can recover from destructive loss of primary persistent data using the replicated secondary copy and independently demonstrate recovery through the encrypted restic backup repository.

## Recovery Objectives

| Metric | Target |
|---|---:|
| RTO | 15 minutes |
| RPO | 5 minutes |
| MTD | 4 hours |

## Failure Simulation

Primary persistent workload data was intentionally deleted to simulate catastrophic storage loss.

Disaster simulation started:

    2026-09-09T19:05:02Z

## Failover Result

The primary workload was stopped and a secondary workload container was started using:

    backups-secondary/

Failover service endpoint:

    http://127.0.0.1:8081

Health response:

    HTTP 200

## RTO Result

Target:

    900 seconds

Actual:

    3 seconds
    0.05 minutes

Result:

    PASS

## RPO Result

Target:

    300 seconds

Actual:

    unknown seconds

Result:

    FAIL

The recovery-point measurement compares the disaster timestamp with the most recent committed transaction present in the secondary replica.

## Data Integrity

Known-good transaction count:

    0

Recovered transaction count:

    0

Known-good maximum transaction ID:

    0

Recovered maximum transaction ID:

    0

Known-good SHA-256:

    65f9a01d4290d2ffbc027e9b8c03c57dd8742d70c4c8a99c8441f145e119aa9f

Recovered SHA-256:

    65f9a01d4290d2ffbc027e9b8c03c57dd8742d70c4c8a99c8441f145e119aa9f

## Restic Recovery Test

The latest encrypted restic snapshot was restored independently to an evidence directory.

Restore duration:

    0 seconds

This validates that the recovery design does not depend exclusively on the continuously synchronized secondary replica.

## Control Assessment

### CP-9 — System Backup

Result:

    PASS

Evidence:

- encrypted restic repository
- recoverable historical snapshot
- repository integrity check
- successful independent restore

### CP-10 — System Recovery and Reconstitution

Result:

    PASS

Evidence:

- scripted secondary activation
- application health validation
- measured recovery duration
- recovered transaction data

### CP-4 — Contingency Plan Testing

Result:

    PASS

Evidence:

- destructive failure simulation
- operational failover execution
- RTO/RPO measurement
- independent restore-path test

## Limitation

Primary and secondary recovery storage remain on the same physical VM because of the environment constraint.

The test validates recovery logic but does not demonstrate resilience against complete host, availability-zone, or site loss.

## Conclusion

The functional exercise directly measured recovery capability rather than relying solely on documented procedures.

Final control conclusions should be based on the measured RTO, measured RPO, recovered-data integrity, and the known environmental limitations recorded in the assessment documentation.
