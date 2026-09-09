# Disaster Recovery Tabletop Scenario

## Exercise Title

Primary Storage Corruption and DR Failover Decision

## Purpose

This tabletop exercise validates whether the organization can:

- detect a workload disruption
- escalate the event appropriately
- declare a disaster
- authorize failover
- activate the secondary recovery path
- communicate status to stakeholders
- preserve evidence
- operate within defined RTO and RPO objectives

## Business Context

The protected workload is a transaction-processing service using a persistent SQLite database.

Business Impact Analysis targets:

- RTO: 15 minutes
- RPO: 5 minutes
- MTD: 4 hours

The primary service normally runs from:

    workload/data/transactions.db

The secondary recovery copy is maintained at:

    backups-secondary/transactions.db

Historical encrypted recovery points are maintained in:

    backups-primary/restic-repo

## Scenario

At 14:00 UTC, corruption begins on the primary workload storage.

At 14:05 UTC, application requests begin returning errors.

At 14:10 UTC, transaction-processing failures are visible in operational checks.

At 14:20 UTC, the incident is formally detected and escalated.

The primary storage is determined to be unreliable.

The latest successful rsync replication occurred less than five minutes before the corruption event.

The latest restic snapshot is also available.

## Exercise Injects

### Inject 1 — Initial Detection

Time:

    14:20

Condition:

The application health endpoint is no longer returning a valid response.

Expected actions:

- validate application status
- confirm service impact
- open incident record
- identify business process owner
- begin recovery clock

### Inject 2 — Storage Failure Confirmed

Time:

    14:23

Condition:

The primary SQLite database is unreadable or unavailable.

Expected actions:

- classify incident severity
- determine whether local repair is viable
- compare repair estimate against RTO
- consider disaster declaration

### Inject 3 — Recovery Options Available

Time:

    14:25

Available recovery paths:

1. rsync secondary replica
2. latest restic snapshot
3. older restic historical snapshot

Expected decision:

Select the secondary replica as the primary failover path because it provides the shortest expected RTO.

### Inject 4 — Failover Authorization

Time:

    14:27

The Incident Coordinator determines that restoring the primary workload within the remaining RTO window is uncertain.

Expected action:

Declare a disaster and authorize failover.

### Inject 5 — Secondary Service Activation

Time:

    14:29

Expected actions:

- stop or isolate primary workload
- activate secondary service
- mount replicated data
- run health checks
- validate transaction data
- communicate recovery status

### Inject 6 — Post-Recovery Validation

Time:

    14:33

The secondary workload responds successfully.

Expected actions:

- validate transaction integrity
- calculate actual RTO
- calculate estimated RPO
- capture evidence
- document residual risks
- determine whether primary-site restoration is required

## Disaster Declaration Criteria

A disaster may be declared when one or more of the following conditions are met:

- primary storage is corrupted or unavailable
- estimated repair time threatens the 15-minute RTO
- data integrity cannot be established on the primary site
- service cannot safely resume on the primary workload
- a pre-tested secondary recovery path is available and lower risk

## RACI

| Activity | Incident Coordinator | Platform Engineer | Application Owner | Risk/Control Owner | Business Owner |
|---|---|---|---|---|---|
| Detect outage | I | R | C | I | I |
| Confirm technical impact | C | R | R | I | I |
| Assess business impact | C | C | C | C | R |
| Declare disaster | A | C | C | C | C |
| Authorize failover | A | R | C | C | C |
| Execute failover | I | R | C | I | I |
| Validate application | C | R | R | I | C |
| Validate data integrity | C | R | R | C | I |
| Communicate status | R | C | C | C | A |
| Record control deficiency | C | C | C | R | I |
| Approve return to normal | A | R | C | C | C |

Legend:

- R = Responsible
- A = Accountable
- C = Consulted
- I = Informed

## Communication Plan

### Technical Team

Notification trigger:

    confirmed production outage

Information required:

- incident start time
- affected workload
- current impact
- recovery action
- expected next update

### Business Owner

Notification trigger:

    incident threatens business service availability

Information required:

- operational impact
- expected recovery path
- RTO status
- estimated data-loss exposure

### Risk / Control Owner

Notification trigger:

    recovery control is invoked or fails

Information required:

- affected CP controls
- RTO/RPO performance
- backup/replication status
- control deficiencies
- remediation requirements

## Escalation Path

    Monitoring / user report
            |
            v
      Platform Engineer
            |
            v
    Incident Coordinator
            |
            v
      Business Owner
            |
            v
   Risk / Control Owner

## Decision Principles

Failover decisions must prioritize:

1. data integrity
2. restoration within RTO
3. recovery within RPO
4. controlled execution
5. evidence preservation
6. stakeholder communication

## Expected Exercise Outcome

The tabletop should demonstrate that the organization can make a timely, documented recovery decision and identify any gaps before the live technical failover test.
