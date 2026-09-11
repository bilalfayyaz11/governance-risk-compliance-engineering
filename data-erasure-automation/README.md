# Data Erasure Automation with PostgreSQL

## Overview

This implementation demonstrates a privacy-engineering workflow for locating and erasing personal data distributed across a relational PostgreSQL system.

A Python service traces records associated with a data subject, performs a staged soft-delete and hard-delete workflow, preserves a non-PII audit trail, anonymizes a simulated retained backup representation, and generates an erasure confirmation certificate using a SHA-256 subject reference.

The workflow is designed around GDPR Article 17 operational requirements while preserving an important distinction: erasure is not an unconditional instruction to delete every record regardless of legal retention obligations. The technical workflow supports erasure decisions; applicable legal exceptions and retention requirements must still be evaluated separately.

---

## Architecture

~~text
                       Data Subject
                            |
                            | email lookup
                            v
                  +-------------------+
                  |   Python Service  |
                  |                   |
                  | Record Discovery  |
                  +---------+---------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
       PostgreSQL Users              Related Records
             |                       /             \
             |                  Orders          Tickets
             |                       \             /
             +------------------------+-----------+
                                      |
                                      v
                              Soft Delete
                                      |
                              Grace / Review
                                      |
                                      v
                         Transactional Hard Delete
                                      |
                         +------------+-------------+
                         |                          |
                         v                          v
                    Audit Trail            Backup Representation
                                                    |
                                                    v
                                             Anonymization
                                                    |
                                                    v
                                           Verification Check
                                                    |
                                                    v
                                      Erasure Confirmation Certificate
                                      SHA-256 Subject Reference
~~

---

## Core Capabilities

The implementation provides:

- Cross-table subject discovery
- Parameterized SQL queries
- Multi-table PostgreSQL schema
- Soft-delete workflow
- Transactional hard-delete workflow
- Consistent audit logging
- Rollback on deletion failure
- Backup anonymization simulation
- Post-erasure verification
- SHA-256 subject references
- Erasure confirmation certificates
- Separation of audit evidence from erased PII

---

## Technology Stack

- PostgreSQL
- Python 3
- psycopg2
- SQL
- JSONB
- SHA-256
- Bash
- Git

---

## Repository Structure

~~text
data-erasure-automation/
├── README.md
├── schema.sql
├── erasure_service.py
├── certificates/
│   └── certificate_1.txt
└── evidence/
    └── verification.txt
~~

---

## Data Model

The PostgreSQL schema models personal data distributed across multiple system components.

### Users

~~sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP
);
~~

### Orders

~~sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    amount NUMERIC(10,2) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT NOW()
);
~~

### Support Tickets

~~sql
CREATE TABLE support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
~~

### Audit Log

~~sql
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    user_id INT,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    performed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    details JSONB NOT NULL DEFAULT '{}'::jsonb
);
~~

### Simulated Backup Representation

~~sql
CREATE TABLE users_backup (
    LIKE users INCLUDING ALL
);
~~

The backup table represents a retained copy that cannot simply be treated as part of the live application database.

---

## Subject Record Discovery

The service begins by locating a subject through the `users` table.

~~python
find_user_records("alice@example.com")
~~

Example result:

~~text
{
    "user_id": 1,
    "records": {
        "orders": 2,
        "support_tickets": 1
    }
}
~~

The service then identifies all known related records associated with the internal `user_id`.

---

## SQL Injection Protection

User-controlled values are passed through parameterized SQL queries.

Example:

~~python
cur.execute(
    """
    SELECT user_id
    FROM users
    WHERE email = %s
    """,
    (email,),
)
~~

Table identifiers cannot be passed as ordinary SQL parameters.

For that reason, related tables come from a fixed application allow-list:

~~python
RELATED_TABLES = [
    "orders",
    "support_tickets",
]
~~

Arbitrary table names are never accepted from external input.

---

## Erasure Workflow

The workflow is implemented in stages.

~~text
Locate Subject
      |
      v
Identify Related Records
      |
      v
Soft Delete
      |
      v
Audit SOFT_DELETE
      |
      v
Transactional Hard Delete
      |
      +----> Delete Orders
      |
      +----> Delete Support Tickets
      |
      +----> Delete User
      |
      +----> Audit Every Step
      |
      v
Anonymize Backup
      |
      v
Verify Backup
      |
      v
Generate Certificate
~~

---

## Soft Delete

The first deletion stage marks the user as deleted without immediately removing the record.

~~sql
UPDATE users
SET
    is_deleted = TRUE,
    deleted_at = NOW()
WHERE user_id = %s;
~~

This supports architectures where organizations require:

- Approval workflows
- Short grace periods
- Fraud review
- Legal review
- Operational recovery windows

The action is written to `audit_log` as:

~~text
SOFT_DELETE
~~

---

## Transactional Hard Delete

The permanent deletion step removes records from related tables before deleting the parent user.

Order of operations:

~~text
orders
   |
   v
support_tickets
   |
   v
users
~~

This avoids foreign-key violations.

Every deletion is logged.

Typical audit sequence:

~~text
SOFT_DELETE  users
HARD_DELETE  orders
HARD_DELETE  support_tickets
HARD_DELETE  users
~~

---

## Transaction Safety

The hard-delete workflow executes as one PostgreSQL transaction.

Conceptually:

~~python
with conn:
    delete_orders()
    audit_orders()

    delete_support_tickets()
    audit_support_tickets()

    delete_user()
    audit_user()
~~

If any operation fails:

~~text
ROLLBACK
~~

This prevents states such as:

- User removed but related data left behind
- Related records deleted but audit trail missing
- Partial deletion across application tables

Atomicity is important because erasure evidence must accurately represent what actually happened.

---

## Audit Design

The audit trail deliberately stores:

- Internal numeric subject reference
- Action
- Table
- Timestamp
- Technical deletion metadata

It does not preserve:

- Raw email
- Full name
- Other erased identifiers

Example:

~~text
user_id: 1
action: HARD_DELETE
table_name: orders
details: {"rows_deleted": 2}
~~

This preserves operational evidence without recreating the personal data that was intentionally removed.

---

## Backup Anonymization

Production backup systems are frequently immutable or governed by retention schedules.

This implementation therefore models an alternative pattern:

~~text
Live Records
    |
    v
Hard Delete

Retained Backup Representation
    |
    v
Anonymization
~~

The simulated backup row changes from:

~~text
alice@example.com
Alice Khan
~~

to:

~~text
anon_1@erased.local
REDACTED
~~

The row is also marked deleted.

---

## Backup Verification

The service verifies that:

~~text
email == anon_<user_id>@erased.local
full_name == REDACTED
is_deleted == true
~~

Example:

~~python
verify_backup_anonymized(1)
~~

Expected result:

~~text
True
~~

The workflow separately checks that the original email and name no longer exist in the simulated backup representation.

---

## Production Backup Consideration

The backup table is a simplified model.

Production environments should not assume that immutable or offline backups can always be modified directly.

A more realistic strategy may include:

- Backup retention limits
- Restore-time suppression lists
- Automatic re-erasure after restoration
- Cryptographic erasure
- Data lifecycle expiration
- Restricted backup access
- Documented legal retention
- Restore procedures that prevent erased identities from re-entering production

The key requirement is that retained backup mechanisms must not silently defeat the organization's erasure process.

---

## Erasure Certificate

After the workflow completes, the service generates a technical confirmation certificate.

Example:

~~text
certificates/certificate_1.txt
~~

The certificate contains:

- SHA-256 subject reference
- Internal subject reference
- Deletion actions
- Action timestamps
- Backup anonymization evidence
- Technical compliance statement

It intentionally does not contain the subject's raw email address.

---

## Hashed Subject Reference

Instead of storing:

~~text
alice@example.com
~~

the certificate stores:

~~text
SHA256(email)
~~

using:

~~python
hashlib.sha256(
    email.encode("utf-8")
).hexdigest()
~~

This allows an organization that already knows the original email to reproduce the reference for verification without publishing the email inside the certificate.

---

## Example Certificate Structure

~~text
RIGHT TO ERASURE CONFIRMATION CERTIFICATE
=========================================

Subject Reference (SHA-256):
<hashed-reference>

Internal User Reference:
1

Erasure Actions:

SOFT_DELETE
HARD_DELETE
HARD_DELETE
HARD_DELETE
ANONYMIZE_BACKUP

Verification Summary:

- Live user record removed
- Related application records removed
- Simulated retained backup record anonymized
- Audit evidence retained without storing raw email
~~

---

## GDPR Article 17 Context

The workflow supports implementation of the right to erasure by providing a repeatable technical process for:

1. Finding subject data
2. Identifying related records
3. Removing live application records
4. Addressing retained copies
5. Verifying the result
6. Preserving evidence that the workflow executed

Article 17 should not be interpreted as an unconditional requirement to delete every record in every circumstance.

Applicable legal exceptions, retention obligations, legal claims, regulatory requirements, and other lawful grounds must be evaluated before an erasure request is approved.

This implementation therefore demonstrates technical execution after an erasure decision has been authorized.

---

## Security Decisions

### Parameterized Queries

Subject identifiers are never concatenated directly into SQL.

### Fixed Table Allow-List

Dynamic table operations use known application-controlled table names.

### Transactional Deletion

Related records and audit events succeed or fail together.

### Minimal Audit PII

The audit trail does not retain erased emails or names.

### Hashed Certificate Reference

The certificate contains a SHA-256 reference rather than the raw email.

### Backup Verification

The workflow confirms the anonymization result rather than assuming the update succeeded.

---

## Verification

Check live user records:

~~bash
PGPASSWORD='labpass123' \
psql \
-h localhost \
-U lab_user \
-d erasure_lab \
-c "
SELECT *
FROM users
WHERE user_id = 1;
"
~~

Expected:

~~text
0 rows
~~

Check orders:

~~bash
PGPASSWORD='labpass123' \
psql \
-h localhost \
-U lab_user \
-d erasure_lab \
-c "
SELECT *
FROM orders
WHERE user_id = 1;
"
~~

Expected:

~~text
0 rows
~~

Check support tickets:

~~bash
PGPASSWORD='labpass123' \
psql \
-h localhost \
-U lab_user \
-d erasure_lab \
-c "
SELECT *
FROM support_tickets
WHERE user_id = 1;
"
~~

Expected:

~~text
0 rows
~~

Check backup anonymization:

~~bash
PGPASSWORD='labpass123' \
psql \
-h localhost \
-U lab_user \
-d erasure_lab \
-c "
SELECT
    user_id,
    email,
    full_name,
    is_deleted
FROM users_backup
WHERE user_id = 1;
"
~~

Expected:

~~text
anon_1@erased.local
REDACTED
true
~~

Verify the certificate does not contain the raw email:

~~bash
grep -Fqi \
"alice@example.com" \
certificates/certificate_1.txt && \
echo "FAIL" || \
echo "PASS"
~~

Expected:

~~text
PASS
~~

---

## Key Skills Demonstrated

- PostgreSQL schema design
- Relational data discovery
- Python database programming
- psycopg2
- Parameterized SQL
- Foreign-key-aware deletion
- Database transactions
- Rollback design
- JSONB audit logging
- Soft-delete architecture
- Hard-delete architecture
- Backup anonymization
- Data minimization
- SHA-256 hashing
- Privacy engineering
- GDPR Article 17 implementation
- Compliance evidence generation

---

## Production Improvements

A production implementation should additionally include:

- Subject identity verification
- Authorization and approval workflow
- Legal-hold detection
- Retention-policy checks
- Dynamic personal-data inventory
- Data catalog integration
- Queued asynchronous erasure operations
- Idempotent deletion jobs
- Distributed service coordination
- Object-storage erasure handling
- Search-index deletion
- Cache invalidation
- Analytics warehouse deletion
- SaaS processor deletion APIs
- Backup suppression registries
- Restore-time re-erasure
- Certificate signing
- Immutable audit storage
- Role-based access controls
- Secrets management
- Database connection pooling
- Structured observability
- Erasure SLA monitoring

---

## Final Outcome

The resulting workflow provides a traceable technical pipeline:

~~text
Subject Request
      |
      v
Record Discovery
      |
      v
Soft Delete
      |
      v
Transactional Hard Delete
      |
      v
Related Data Removed
      |
      v
Backup Anonymized
      |
      v
Verification
      |
      v
SHA-256 Referenced Certificate
      |
      v
Non-PII Audit Evidence Retained
~~

This creates a practical foundation for implementing data-subject erasure across relational application systems while maintaining transaction integrity and auditable evidence.
