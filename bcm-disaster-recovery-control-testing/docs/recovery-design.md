# Recovery Design

## Recovery Objectives

- RTO: 15 minutes
- RPO: 5 minutes
- MTD: 4 hours

These values are inherited directly from the Business Impact Analysis.

## Backup Control

Encrypted historical backups are implemented using restic.

Repository:

    backups-primary/restic-repo

Backup scope:

    workload/data

Features:

- encrypted repository
- deduplicated snapshots
- incremental backup behavior
- timestamped workload tagging
- execution logging

Cadence:

    Every 5 minutes

This cadence satisfies the stated five-minute RPO.

## Replication Control

Near-real-time recovery data is maintained using rsync.

Source:

    workload/data/

Destination:

    backups-secondary/

Replication options include:

- archive mode
- checksum comparison
- delete-after synchronization

Cadence:

    Every 5 minutes

The secondary copy is the preferred failover source because it minimizes restore processing before service restart.

## Failover Strategy

The failover process:

1. records failover start time
2. stops the primary workload
3. launches a secondary workload container
4. mounts the replicated secondary data
5. performs HTTP health validation
6. records failover completion time
7. calculates actual RTO

Primary endpoint:

    127.0.0.1:8080

Failover endpoint:

    127.0.0.1:8081

## RTO Design

Target:

    15 minutes / 900 seconds

The failover container image is prebuilt and secondary data is pre-replicated.

This eliminates:

- application rebuild time
- package installation
- database reconstruction
- full historical restore during the primary failover path

## RPO Design

Target:

    5 minutes

Both backup and replication execute every five minutes.

The expected worst-case data loss interval is therefore approximately five minutes, excluding scheduler or execution failure.

Replication logs and backup logs must be reviewed during testing to confirm execution occurred successfully.

## Recovery Path Priority

1. rsync secondary replica
2. restic latest snapshot
3. earlier restic historical snapshot where corruption has propagated to the replica

## Control Relationships

- CP-2: recovery strategy and recovery objectives
- CP-9: encrypted backup capability
- CP-10: restoration and reconstitution
- CP-4: exercise and technical testing

