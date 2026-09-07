# Authorization Decision Record Rationale

## Purpose

The authorization decision is recorded in an append-only JSON Lines ledger rather than maintained solely as an editable narrative document.

This design provides a simple audit trail for authorization activity while preserving the sequence and integrity relationships between individual decision records.

## Why Append-Only JSON Lines

Each authorization decision is stored as an independent JSON object on a new line.

This provides several operational advantages:

- new decisions can be appended without rewriting earlier entries;
- each record can be independently parsed and inspected;
- automated systems can process the ledger without proprietary document formats;
- historical decisions remain visible when authorization status changes;
- the format is suitable for version control, archival, and downstream audit processing.

## Hash Chaining

Every record contains a cryptographic SHA-256 hash calculated over its decision content.

Each record also stores the hash of the immediately preceding record.

The first entry references a defined `GENESIS` value.

This creates the relationship:

    Record 1
    previous_record_hash = GENESIS
              |
              v
         record_hash
              |
              v
    Record 2
    previous_record_hash = Record 1 hash
              |
              v
         record_hash
              |
              v
    Record 3 ...

If an earlier record is modified, its recalculated hash changes. The following record will then reference a hash that no longer matches, allowing the verification process to detect the broken chain.

## Evidence Chain-of-Custody Link

The authorization record also stores the SHA-256 digest of the signed evidence index reviewed during the authorization process.

This establishes a cryptographic reference between:

- the authorization decision;
- the evidence snapshot presented for review; and
- the detached GPG signature protecting that evidence index.

The decision therefore identifies the specific evidence state upon which the simulated authorization was based.

## Integrity Versus Non-Repudiation

Hash chaining provides tamper evidence but does not by itself establish the identity of the Authorizing Official.

The evidence index is separately protected using a detached GPG signature.

In a production authorization workflow, the AO decision itself should also use an organization-approved digital-signature or identity-backed approval mechanism.

## Operational Limitation

A local append-only file is not inherently immutable.

A sufficiently privileged administrator could replace the entire ledger and recalculate its hashes.

Production implementations should therefore combine this pattern with controls such as:

- restricted write permissions;
- centralized audit logging;
- digitally signed decision records;
- immutable or WORM storage;
- trusted timestamps;
- enterprise identity;
- independent archival copies; and
- controlled authorization workflows.

The implementation demonstrates integrity and audit-trail principles without claiming that a local JSONL file alone provides complete non-repudiation.
