# Data Subject Rights Workflow Automation

## What This Does

This implementation automates the operational lifecycle of Data Subject Access Requests using Python and SQLite. It provides structured request intake, rights-specific response templates, OTP-based identity verification, machine-readable JSON portability exports, SHA-256 integrity validation, and SLA compliance reporting.

The workflow translates privacy requirements into repeatable technical controls that can support privacy operations, governance, and compliance engineering teams.

## Architecture

~~text
                         DATA SUBJECT
                              |
                              v
                  +-------------------------+
                  |     DSAR Intake Layer   |
                  |       intake.py         |
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |      SQLite DSAR DB     |
                  |        dsar.db          |
                  |                         |
                  | - Request type          |
                  | - Status                |
                  | - SLA deadline          |
                  | - Verification state    |
                  +----+---------------+----+
                       |               |
              +--------+               +----------------+
              |                                         |
              v                                         v
 +---------------------------+              +---------------------------+
 | Identity Verification     |              | Rights Response Templates |
 |                           |              |                           |
 | verify_otp.py             |              | access_template.txt       |
 | PyOTP / TOTP              |              | deletion_template.txt     |
 | Local SMTP :1025          |              | portability_template.txt  |
 +-------------+-------------+              +---------------------------+
               |
               v
       +----------------+
       | Verified DSAR  |
       +--------+-------+
                |
        +-------+-------------------+
        |                           |
        v                           v
+----------------------+   +-------------------------+
| Portability Pipeline |   | SLA Compliance Engine   |
|                      |   |                         |
| customer.db          |   | sla_report.py           |
| export_portability.py|   | Deadline monitoring     |
| JSON export          |   | Overdue detection       |
| SHA-256 checksum     |   | Compliance reporting    |
+----------+-----------+   +------------+------------+
           |                            |
           v                            v
+----------------------+      +----------------------+
| portability_bundle   |      | compliance_report    |
| .json                |      | .txt                 |
+----------------------+      +----------------------+
~~

## Prerequisites

- Ubuntu 22.04+ or equivalent Linux environment
- Python 3.10+
- Python virtual environment support
- SQLite 3
- pip
- PyOTP
- aiosmtpd
- Git
- Local TCP port 1025 available for SMTP testing

Docker is not required for this implementation.

## Setup & Installation

~~bash
sudo apt update
sudo apt install -y sqlite3 python3-venv

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install pyotp aiosmtpd

mkdir -p tickets scripts templates reports
~~

## How to Reproduce

### 1. Initialize the DSAR Database

~~bash
sqlite3 tickets/dsar.db <<'SQL'
CREATE TABLE requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject_email TEXT NOT NULL,
  request_type TEXT NOT NULL,
  status TEXT DEFAULT 'received',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sla_deadline TIMESTAMP,
  verified INTEGER DEFAULT 0
);
SQL
~~

Create a request:

~~bash
python scripts/intake.py
~~

Verify the stored request:

~~bash
sqlite3 -header -column tickets/dsar.db \
"SELECT id, subject_email, request_type, status, created_at, sla_deadline, verified FROM requests;"
~~

The intake workflow validates the requested privacy right, creates the request record, assigns its initial status, and calculates the response deadline.

### 2. Review Rights-Specific Templates

~~bash
cat templates/access_template.txt
cat templates/deletion_template.txt
cat templates/portability_template.txt
~~

The templates provide structured operational fields for:

- Data access requests
- Data erasure requests
- Data portability requests
- Requester identity
- Verification status
- Scope
- Response deadlines
- Retention exceptions
- Transfer methods
- Integrity checksums

### 3. Start Local SMTP Identity Verification

Python 3.12 removed the legacy `smtpd` standard-library module.

Start the replacement SMTP debugging service:

~~bash
aiosmtpd \
  -n \
  -l localhost:1025 \
  -c aiosmtpd.handlers.Debugging
~~

In another terminal:

~~bash
cd ~/dsar-lab
source .venv/bin/activate
python scripts/verify_otp.py
~~

The workflow:

1. Generates a Base32 secret.
2. Produces a time-based six-digit OTP.
3. Sends the OTP through the local SMTP service.
4. Captures the email for validation.
5. Verifies the submitted OTP using TOTP validation.

Test OTP values are printed only for local validation.

Production implementations must never log OTP secrets or authentication codes.

### 4. Create Sample Customer Data

~~bash
sqlite3 tickets/customer.db <<'SQL'
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT,
  address TEXT,
  signup_date TEXT
);

INSERT INTO customers
VALUES (
  1,
  'Ahmed Ali',
  'ahmed@example.com',
  'Dubai, UAE',
  '2022-01-15'
);
SQL
~~

### 5. Generate the Data Portability Bundle

Run:

~~bash
python scripts/export_portability.py
~~

Inspect the generated JSON:

~~bash
cat reports/portability_bundle.json
~~

Verify its cryptographic integrity:

~~bash
sha256sum reports/portability_bundle.json
~~

The Python-generated SHA-256 digest should match the operating-system `sha256sum` result.

This verifies that the checksum corresponds to the exact portability bundle written to disk.

### 6. Generate the SLA Compliance Report

~~bash
python scripts/sla_report.py
cat reports/compliance_report.txt
~~

The report provides:

- Total received requests
- Completed requests
- Requests considered completed within SLA
- Overdue open requests
- Compliance percentage
- Individual overdue request details

### 7. Validate Python Source

~~bash
python -m py_compile \
  scripts/intake.py \
  scripts/verify_otp.py \
  scripts/export_portability.py \
  scripts/sla_report.py
~~

## Tools Used

- Python 3
- SQLite
- PyOTP
- TOTP
- aiosmtpd
- Python smtplib
- Python email.mime
- JSON
- SHA-256
- hashlib
- Linux CLI
- Git

## Key Skills Demonstrated

- Translating privacy requirements into executable technical controls
- Automating data subject request workflows with Python
- Designing SQLite-backed operational data models
- Implementing TOTP-based identity verification
- Integrating Python applications with SMTP services
- Producing machine-readable personal-data exports
- Applying SHA-256 integrity verification to exported data
- Automating SLA deadline monitoring
- Detecting overdue compliance obligations
- Generating auditable compliance reports
- Designing reproducible governance automation
- Troubleshooting Python platform compatibility changes

## Real-World Use Case

A privacy operations team can use this architecture as the foundation for automating data subject rights requests. Requests can be registered and assigned response deadlines, requester identity can be verified before sensitive information is released or modified, relevant personal records can be exported in a structured machine-readable format, and integrity checks can verify that delivered files have not changed.

The same pattern could be extended in production by integrating enterprise ticketing platforms, customer databases, identity providers, CRM systems, data catalogs, workflow engines, and centralized compliance dashboards.

## Lessons Learned

- Regulatory requirements are easier to enforce when converted into automated operational controls rather than relying entirely on manual processes.
- Request validation should occur before records are committed to the workflow.
- Database paths should resolve from application locations rather than depend on the caller's working directory.
- Identity verification should occur before sensitive personal data is disclosed, deleted, or transferred.
- Machine-readable exports benefit from integrity hashes when files move between systems or teams.
- SLA calculations require accurate lifecycle timestamps to provide defensible compliance evidence.
- Python dependencies should be isolated from the operating system using virtual environments.

## Troubleshooting Log

### Python smtpd Removed

The original workflow attempted to start the SMTP debugging server using:

~~bash
python3 -m smtpd -c DebuggingServer -n localhost:1025
~~

The `smtpd` module was removed from Python 3.12, so the command fails on current Python environments.

It was replaced with:

~~bash
aiosmtpd \
  -n \
  -l localhost:1025 \
  -c aiosmtpd.handlers.Debugging
~~

This provides equivalent local SMTP debugging functionality using maintained tooling.

### SMTP Messages Were Not Initially Captured

The SMTP listener successfully accepted connections and the OTP workflow completed, but redirected output initially contained no captured message body.

The explicit debugging handler:

~~text
aiosmtpd.handlers.Debugging
~~

was added so that received messages are written to the debug output and can be validated.

### Fragile Relative Database Paths

The initial implementation used paths such as:

~~python
DB_PATH = "tickets/dsar.db"
~~

This assumes the application is always executed from its root directory.

The scripts instead resolve the application root using:

~~python
BASE_DIR = Path(__file__).resolve().parent.parent
~~

Database paths are then built relative to that location.

This makes execution independent of the caller's current working directory.

### Missing Customer Handling

The initial portability workflow assumed that every supplied email address would match a database record.

The implementation explicitly detects missing records and raises an informative exception rather than creating an empty or invalid portability package.

### SLA Schema Limitation

The current request schema contains:

~~text
created_at
sla_deadline
status
~~

but does not contain a historical completion timestamp.

A production implementation should add:

~~sql
completed_at TIMESTAMP
~~

and evaluate successful SLA completion using:

~~text
completed_at <= sla_deadline
~~

Without `completed_at`, the current completed-within-SLA calculation is an approximation rather than definitive historical evidence.

### Python Package Isolation

Python dependencies are installed inside:

~~text
.venv/
~~

rather than Ubuntu's system-managed Python environment.

This avoids system-package conflicts and provides a cleaner reproducible runtime.
