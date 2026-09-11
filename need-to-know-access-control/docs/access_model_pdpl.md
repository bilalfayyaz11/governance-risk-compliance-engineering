# Need-to-Know Access Model for Employee Records

## Overview

This implementation applies role-based access control, column-level privileges,
row-level security, and database audit logging to protect employee records
according to job function.

The model is designed around three business functions:

- HR
- Finance
- Audit

The objective is to ensure that each role can access only the personal data
required for its defined business purpose.

---

## Roles and Justification

### hr_role

Purpose:

HR requires broad visibility into employee records for personnel administration.

Permitted access:

- emp_id
- full_name
- department
- salary
- ssn
- audit_flag

Row scope:

- All employee rows

Justification:

HR performs identity, compensation, and personnel-management activities that
require broader access than other functions.

---

### finance_role

Purpose:

Finance requires compensation information for payroll and finance operations.

Permitted access:

- emp_id
- full_name
- department
- salary

Explicitly restricted:

- ssn
- audit_flag

Row scope:

- Finance department records only

Policy:

~~sql
USING (department = 'Finance')
~~

Justification:

Finance does not require national identifiers or unrelated departmental
records to perform its assigned function.

---

### audit_role

Purpose:

Audit requires visibility into records specifically marked for audit review.

Permitted access:

- emp_id
- department
- audit_flag

Explicitly restricted:

- full_name
- salary
- ssn

Row scope:

- Records where audit_flag = true

Policy:

~~sql
USING (audit_flag = TRUE)
~~

Justification:

Audit access is limited to evidence necessary to perform assurance activities
without granting unnecessary access to compensation or identity data.

---

## Controls Implemented

### Column-Level Restrictions

PostgreSQL column privileges restrict which attributes each role can query.

| Role | Accessible Columns |
|---|---|
| hr_role | All employee columns |
| finance_role | emp_id, full_name, department, salary |
| audit_role | emp_id, department, audit_flag |

These controls prevent a role from retrieving restricted columns even if it
can query the table.

Examples:

~~text
finance_role -> SELECT ssn    -> Denied
audit_role   -> SELECT salary -> Denied
~~

---

## Row-Level Security

PostgreSQL Row-Level Security provides a second authorization layer.

### Finance Policy

~~sql
CREATE POLICY finance_dept_policy
ON employee_records
FOR SELECT
TO finance_role
USING (department = 'Finance');
~~

Finance therefore sees only records belonging to its own department.

### HR Policy

~~sql
CREATE POLICY hr_full_visibility_policy
ON employee_records
FOR SELECT
TO hr_role
USING (TRUE);
~~

HR can access all rows because its personnel-management function requires
organization-wide employee visibility.

### Audit Policy

~~sql
CREATE POLICY audit_flag_policy
ON employee_records
FOR SELECT
TO audit_role
USING (audit_flag = TRUE);
~~

Audit sees only records specifically flagged for review.

---

## Defense in Depth

The access model combines two different authorization mechanisms:

~~text
User Role
   |
   v
Column Privileges
   |
   | Which fields may this role access?
   v
Row-Level Security
   |
   | Which records may this role see?
   v
Authorized Result Set
~~

Column restrictions and row restrictions are intentionally applied together.

A role must satisfy both controls.

---

## Audit Logging

pgAudit is enabled for:

~~text
read
write
role
~~

Relationship-level logging is also enabled:

~~text
pgaudit.log_relation = on
~~

The PostgreSQL configuration loads pgAudit through:

~~text
shared_preload_libraries = 'pgaudit'
~~

Audit evidence is retained in:

~~text
evidence/pgaudit_access_evidence.log
~~

The evidence captures successful database activity and is supplemented by
PostgreSQL permission-denial events for rejected access attempts.

---

## Segregation of Duties Validation

The access model was tested by authenticating directly as each role.

Evidence:

~~text
evidence/access_test_matrix.csv
evidence/access_test_raw.log
~~

Validated behavior:

| Role | Test | Result |
|---|---|---|
| finance_role | Read finance columns | Allowed |
| finance_role | Read SSN | Denied |
| finance_role | Read HR rows | Zero rows through RLS |
| audit_role | Read audit columns | Allowed |
| audit_role | Read salary | Denied |
| audit_role | Read non-flagged records | Zero rows through RLS |
| hr_role | Read complete employee records | Allowed |

Observed row visibility:

~~text
finance_role = 1 row
audit_role   = 2 rows
hr_role      = 3 rows
~~

---

## Saudi PDPL Alignment

### Purpose Limitation

Each database role is tied to a defined organizational function.

~~text
HR      -> personnel administration
Finance -> compensation processing
Audit   -> assurance and review
~~

Access is not granted merely because a user belongs to the organization.

The authorization decision is tied to the purpose for which the data is
required.

This supports the PDPL principle that personal data should be processed only
for a defined and legitimate purpose.

---

## Data Minimization

The model reduces personal-data exposure through both column and row controls.

Finance cannot retrieve:

~~text
ssn
audit_flag
non-Finance employee rows
~~

Audit cannot retrieve:

~~text
full_name
salary
ssn
non-flagged employee rows
~~

This implements need-to-know at query time rather than relying only on policy
documents.

The design supports the PDPL requirement to limit personal data processing to
the minimum data necessary for the relevant purpose.

---

## Integrity and Confidentiality

The following controls protect employee information from unauthorized access:

- Explicit role grants
- Removal of PUBLIC table access
- Column-specific privileges
- PostgreSQL Row-Level Security
- No BYPASSRLS privilege for business roles
- Password-authenticated database identities
- Audit logging

These controls reduce the risk that employees or internal functions can access
personal data outside their assigned responsibilities.

---

## Accountability

pgAudit and PostgreSQL logs provide evidence of:

- Which database identity performed an action
- Which table was accessed
- Which statements were executed successfully
- Which requests were denied by PostgreSQL privileges

The test matrix provides additional evidence that the implemented controls
behave as designed.

This supports accountability by providing technical records that can be used
to demonstrate and review access-control enforcement.

---

## Data Sharing and Cross-Agency Risk

The same need-to-know model can be applied where employee information is
shared across departments or public entities.

Without role restrictions, a shared employee database could allow one
function or agency to retrieve information unrelated to its lawful purpose.

The implemented model reduces that risk by applying:

~~text
Recipient Role
      |
      v
Approved Data Columns
      |
      v
Approved Record Scope
      |
      v
Audited Access
~~

A receiving function therefore does not automatically gain unrestricted
access merely because it has database connectivity.

---

## Important Limitation

RBAC and RLS do not by themselves establish that a disclosure is legally
permitted.

A production organization must separately determine:

- lawful basis
- authorized disclosure purpose
- recipient authorization
- retention requirements
- applicable transfer requirements
- contractual or inter-agency controls

The database model enforces the approved access decision after those
governance requirements have been established.

---

## Evidence Produced

~~text
evidence/access_test_matrix.csv
evidence/access_test_raw.log
evidence/pgaudit_access_evidence.log
~~

These artifacts demonstrate:

- column-level authorization
- row-level authorization
- segregation of duties
- successful access
- rejected access
- auditability

---

## Security Improvements for Production

A production implementation should additionally use:

- Individual user identities mapped to group roles
- Central identity-provider integration
- Multi-factor authentication
- Secret rotation
- Privileged access management
- Separate database ownership roles
- NOLOGIN group roles with individual LOGIN users
- Time-bound privileged access
- TLS-protected database connections
- Centralized immutable audit-log storage
- SIEM ingestion
- Periodic access certification
- Joiner/mover/leaver automation
- Database activity monitoring
- Alerting for repeated permission failures
- Automated policy regression tests
- Formal data-sharing approvals

---

## Recommended Production Role Pattern

Rather than sharing one LOGIN account among multiple employees, production
systems should separate authorization roles from human identities.

~~text
Individual Identity
       |
       v
LOGIN User
       |
       v
NOLOGIN Functional Role
       |
       v
Database Permissions
~~

For example:

~~text
fatima.finance
      |
      v
finance_role
      |
      v
Finance-scoped employee data
~~

This improves individual accountability and makes revocation easier.

---

## Conclusion

The implementation demonstrates a layered need-to-know access architecture
for regulated employee data.

PostgreSQL column privileges restrict sensitive attributes, Row-Level Security
limits record visibility by business purpose, and pgAudit provides evidence
of database activity.

Together, these controls provide a practical technical implementation of
least privilege, data minimization, purpose-scoped access, confidentiality,
and accountability principles relevant to Saudi PDPL governance.
