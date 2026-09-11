# Need-to-Know Access Control with PostgreSQL

## Overview

This implementation demonstrates a role-based need-to-know access model for employee records using PostgreSQL.

The design combines:

- Role-Based Access Control
- Column-level privileges
- Row-Level Security
- pgAudit logging
- Segregation-of-duties testing
- PDPL-aligned access-control documentation

The goal is to ensure that each business function can access only the data required for its authorized purpose while generating evidence of access-control enforcement.

---

## Architecture

The access model uses three functional roles:

- HR
- Finance
- Audit

The authorization flow is:

~~text
Authenticated Role
      |
      v
Column Privileges
      |
      v
Row-Level Security
      |
      v
Authorized Result Set
      |
      v
pgAudit / PostgreSQL Logs
~~

This provides layered enforcement:

- column privileges determine which attributes a role may query
- RLS determines which records a role may see
- audit logging records access activity and permission failures

---

## Database Model

The protected table contains:

~~text
employee_records
├── emp_id
├── full_name
├── department
├── salary
├── ssn
└── audit_flag
~~

Sensitive attributes are exposed differently according to business purpose.

---

## Roles

### HR

Purpose:

Personnel administration.

Access:

- emp_id
- full_name
- department
- salary
- ssn
- audit_flag

Row scope:

- All employee records

---

### Finance

Purpose:

Payroll and finance operations.

Access:

- emp_id
- full_name
- department
- salary

Restricted:

- ssn
- audit_flag

Row scope:

- Finance department records only

RLS policy:

~~sql
USING (department = 'Finance')
~~

---

### Audit

Purpose:

Review records specifically marked for audit attention.

Access:

- emp_id
- department
- audit_flag

Restricted:

- full_name
- salary
- ssn

Row scope:

- Records where audit_flag = true

RLS policy:

~~sql
USING (audit_flag = TRUE)
~~

---

## Column-Level Access Control

Default table access is removed from PUBLIC.

Permissions are then granted selectively.

Finance:

~~sql
GRANT SELECT (
    emp_id,
    full_name,
    department,
    salary
)
ON employee_records
TO finance_role;
~~

Audit:

~~sql
GRANT SELECT (
    emp_id,
    department,
    audit_flag
)
ON employee_records
TO audit_role;
~~

HR:

~~sql
GRANT SELECT
ON employee_records
TO hr_role;
~~

This prevents roles from querying sensitive attributes outside their business need.

Examples:

~~text
finance_role -> SELECT ssn    -> denied
audit_role   -> SELECT salary -> denied
hr_role      -> SELECT *      -> allowed
~~

---

## Row-Level Security

RLS is enabled on the employee table:

~~sql
ALTER TABLE employee_records
ENABLE ROW LEVEL SECURITY;
~~

### Finance Policy

~~sql
CREATE POLICY finance_dept_policy
ON employee_records
FOR SELECT
TO finance_role
USING (department = 'Finance');
~~

### HR Policy

~~sql
CREATE POLICY hr_full_visibility_policy
ON employee_records
FOR SELECT
TO hr_role
USING (TRUE);
~~

### Audit Policy

~~sql
CREATE POLICY audit_flag_policy
ON employee_records
FOR SELECT
TO audit_role
USING (audit_flag = TRUE);
~~

---

## Segregation of Duties

The model was tested by authenticating directly as each role.

Validated behavior:

| Role | Test | Result |
|---|---|---|
| finance_role | Read approved finance columns | Allowed |
| finance_role | Read SSN | Denied |
| finance_role | Read HR rows | Zero rows |
| audit_role | Read audit columns | Allowed |
| audit_role | Read salary | Denied |
| audit_role | Read non-flagged rows | Zero rows |
| hr_role | Read all employee data | Allowed |

Observed row visibility:

~~text
finance_role = 1 row
audit_role   = 2 rows
hr_role      = 3 rows
~~

This demonstrates separation between:

- attribute authorization
- record authorization
- business function

---

## pgAudit

pgAudit is enabled through PostgreSQL shared preload configuration.

~~text
shared_preload_libraries = 'pgaudit'
~~

Audit classes enabled:

~~text
read
write
role
~~

Relation logging:

~~text
pgaudit.log_relation = on
~~

This allows successful database activity to be captured with additional PostgreSQL error logging for denied access attempts.

---

## Audit Evidence

Evidence artifacts:

~~text
evidence/access_test_matrix.csv
evidence/access_test_raw.log
evidence/pgaudit_access_evidence.log
~~

These capture:

- allowed queries
- denied queries
- RLS filtering
- role identity
- access-test results
- audited database activity

---

## PDPL Alignment

### Purpose Limitation

Each role corresponds to a defined organizational purpose:

~~text
HR      -> personnel administration
Finance -> compensation operations
Audit   -> assurance and review
~~

Access is granted according to function rather than general organizational membership.

---

## Data Minimization

Finance cannot retrieve:

- SSN
- audit flags
- non-Finance records

Audit cannot retrieve:

- full name
- salary
- SSN
- non-flagged records

This reduces unnecessary exposure of personal data.

---

## Integrity and Confidentiality

The design uses:

- explicit role grants
- revoked PUBLIC access
- column-level restrictions
- Row-Level Security
- non-superuser business roles
- no BYPASSRLS privileges
- password-authenticated role sessions
- database audit logging

Together, these controls reduce unauthorized internal access.

---

## Accountability

pgAudit and PostgreSQL logs provide evidence of:

- database identity
- queried objects
- successful statements
- privilege failures

The segregation-of-duties matrix provides additional evidence that authorization rules behave as expected.

---

## PDPL Data-Sharing Risk

Need-to-know controls reduce the risk of excessive data disclosure between internal functions or organizations.

A receiving function does not automatically gain unrestricted database access simply because it can connect to the system.

The authorization path is:

~~text
Recipient Identity
       |
       v
Functional Role
       |
       v
Approved Columns
       |
       v
Approved Rows
       |
       v
Audited Result
~~

---

## Important Limitation

Technical access controls do not themselves establish whether a disclosure is legally permitted.

A production environment must separately determine:

- lawful processing purpose
- disclosure authorization
- recipient authorization
- retention requirements
- transfer restrictions
- contractual obligations

The database controls enforce the approved access decision.

---

## Production Role Design

The scenario uses shared functional LOGIN roles.

A stronger production design separates user authentication from authorization.

Recommended pattern:

~~text
Individual LOGIN User
        |
        v
NOLOGIN Functional Role
        |
        v
Database Permissions
~~

Example:

~~text
fatima.finance
      |
      v
finance_role
      |
      v
Finance-scoped employee data
~~

This improves:

- individual accountability
- revocation
- identity lifecycle management
- access reviews
- audit attribution

---

## Evidence Files

~~text
evidence/
├── access_test_matrix.csv
├── access_test_raw.log
└── pgaudit_access_evidence.log
~~

Test automation:

~~text
scripts/test_access_matrix.sh
~~

Compliance documentation:

~~text
access_model_pdpl.md
~~

---

## Verification

Check the functional roles:

~~bash
sudo -u postgres psql \
-d agency_records \
-c "
SELECT
    rolname,
    rolcanlogin,
    rolsuper,
    rolbypassrls
FROM pg_roles
WHERE rolname IN (
    'hr_role',
    'finance_role',
    'audit_role'
);
"
~~

Check RLS:

~~bash
sudo -u postgres psql \
-d agency_records \
-c "
SELECT
    relname,
    relrowsecurity
FROM pg_class
WHERE relname = 'employee_records';
"
~~

Check policies:

~~bash
sudo -u postgres psql \
-d agency_records \
-c "
SELECT
    polname
FROM pg_policy p
JOIN pg_class c
  ON c.oid = p.polrelid
WHERE c.relname = 'employee_records';
"
~~

Check pgAudit:

~~bash
sudo -u postgres psql \
-d agency_records \
-c "
SELECT
    extname,
    extversion
FROM pg_extension
WHERE extname = 'pgaudit';
"
~~

Check test results:

~~bash
cat evidence/access_test_matrix.csv
~~

Expected:

~~text
0 failed access-control tests
~~

---

## Skills Demonstrated

- PostgreSQL RBAC
- Least privilege
- Column-level security
- Row-Level Security
- Need-to-know enforcement
- Segregation of duties
- pgAudit
- Database audit evidence
- Privacy engineering
- PDPL-aligned control design
- Access-control testing
- Compliance evidence generation
- Database security architecture

---

## Production Improvements

A production implementation should also include:

- individual user accounts
- NOLOGIN functional roles
- identity-provider integration
- MFA
- credential rotation
- privileged access management
- database TLS
- centralized immutable logs
- SIEM ingestion
- periodic access reviews
- joiner/mover/leaver automation
- time-bound privileged access
- policy regression testing
- automated entitlement review
- anomaly detection for repeated permission failures

---

## Final Outcome

The implementation creates an end-to-end need-to-know enforcement model:

~~text
Business Function
       |
       v
Database Role
       |
       v
Column Authorization
       |
       v
Row-Level Security
       |
       v
Authorized Data
       |
       v
Audit Evidence
       |
       v
Compliance Documentation
~~

The result demonstrates that least privilege can be enforced technically at the database layer while producing verifiable evidence for security and privacy governance.
