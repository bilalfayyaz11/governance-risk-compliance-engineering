# BCM / DR Control Mapping

## CP-2 — Contingency Plan

Activities:

- Business Impact Analysis
- RTO/RPO/MTD definition
- resource requirements
- roles and responsibilities
- recovery strategy
- communications
- BCP/DRP updates

Evidence:

- `bia.md`
- `recovery-design.md`
- `tabletop-scenario.md`
- `bcp-updates.md`

Assessment:

    Implemented with findings

## CP-4 — Contingency Plan Testing

Activities:

- tabletop exercise
- destructive recovery test
- failover execution
- recovery measurement
- evidence collection

Evidence:

- `tabletop-results.md`
- `technical-failover-results.md`
- `evidence/`

Assessment:

    Tested successfully with findings

## CP-9 — System Backup

Activities:

- encrypted restic backups
- scheduled snapshots
- repository validation
- independent restore test

Evidence:

- backup automation
- restic snapshot history
- `evidence/restic-check.txt`

Assessment:

    Operational with findings

## CP-10 — System Recovery and Reconstitution

Activities:

- rsync recovery replica
- automated secondary startup
- service validation
- transaction recovery
- measured RTO/RPO

Evidence:

- failover automation
- `technical-failover-results.md`
- `evidence/failover-timing.txt`
- `evidence/rpo-calculation.txt`

Assessment:

    Successfully demonstrated

## CGRC Domain 4 — Implementation

Demonstrated through:

- translating business impact into technical requirements
- implementing backup
- implementing replication
- automating failover
- implementing scheduled recovery controls

## CGRC Domain 5 — Assessment

Demonstrated through:

- developing success criteria
- tabletop testing
- functional testing
- evidence collection
- RTO/RPO measurement
- deficiency identification
- remediation planning

## Traceability

    Business Impact Analysis
            |
            v
       RTO / RPO / MTD
            |
            v
       Recovery Controls
      /        |        \
   restic    rsync    failover
      \        |        /
            Testing
               |
               v
            Evidence
               |
               v
       Control Assessment
               |
               v
       Deficiency Tracking
               |
               v
          BCP Updates
