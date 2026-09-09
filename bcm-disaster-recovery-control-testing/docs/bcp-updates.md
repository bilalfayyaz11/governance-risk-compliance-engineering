# BCP / DRP Updates

## RTO Measurement

Define the RTO clock as starting when the business service becomes unavailable, not when a disaster is formally declared.

## Monitoring

Add automated monitoring for:

- application availability
- failed transaction writes
- container failure
- backup failure
- replication failure

## Recovery Infrastructure

Separate production recovery infrastructure from the primary system failure domain.

## Application-Consistent Backup

Use SQLite-aware backup or checkpoint procedures before creating recovery artifacts.

## Failover Authorization

Define explicit disaster declaration and pre-authorized failover thresholds.

## Replication Protection

Maintain versioned historical backups separately from the continuously synchronized replica.

## Credential Protection

Store backup credentials independently using an appropriate secrets-management solution.

## Recovery Validation

Every functional test should validate:

- service availability
- database integrity
- transaction recency
- RTO
- RPO
- backup restoration

## Exercise Governance

Every recovery exercise should produce:

- test plan
- evidence
- measured results
- deficiency register
- remediation ownership
- updated recovery procedures
