# Secure Data Portability Export Pipeline

## What This Does

This implementation builds a machine-readable personal-data portability workflow that separates user-provided information from internally derived business data. Portable information is exported to JSON and CSV, protected with a detached GPG signature, transferred over SFTP, and validated against a strict JSON Schema.

The workflow demonstrates how privacy requirements can be translated into enforceable backend controls rather than handled only through policy documentation.

It also verifies that excluded internal analytics and administrative fields cannot silently leak into a portability package.

## Architecture

~~text
+---------------------------+
|   Source User Record      |
|                           |
| User-Provided Data        |
| Internal Derived Data     |
+-------------+-------------+
              |
              v
+---------------------------+
| Portable Field Filter     |
| exporter.py               |
+-------------+-------------+
              |
       +------+------+
       |             |
       v             v
+------------+   +------------+
| JSON       |   | CSV        |
| Export     |   | Export     |
+-----+------+   +------------+
      |
      v
+---------------------------+
| GPG Detached Signature    |
| export.json.sig           |
+-------------+-------------+
              |
              v
+---------------------------+
| SFTP Delivery             |
| OpenSSH localhost         |
+-------------+-------------+
              |
              v
+---------------------------+
| Integrity Validation      |
| SHA-256 + GPG Verify      |
+-------------+-------------+
              |
              v
+---------------------------+
| JSON Schema Validation    |
| additionalProperties=false|
+---------------------------+
~~

## Prerequisites

- Ubuntu or another Linux distribution
- Python 3.12+
- Python virtual environment support
- pip
- GnuPG
- OpenSSH client and server
- Git
- jsonschema Python package

## Setup & Installation

~~bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    gnupg \
    openssh-server

python3 -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
python -m pip install jsonschema
~~

Confirm SSH is available:

~~bash
sudo systemctl enable --now ssh
sudo systemctl is-active ssh
~~

## How to Reproduce

Activate the Python environment:

~~bash
source venv/bin/activate
~~

Generate the machine-readable exports:

~~bash
python exporter.py

cat export.json
cat export.csv
~~

Verify that internal fields were excluded:

~~bash
grep -Eqi \
    "admin_notes|internal_risk_score" \
    export.json export.csv \
    && echo "FAIL: internal field leaked" \
    || echo "PASS: no internal fields leaked"
~~

Validate the JSON structure:

~~bash
python validate.py
~~

Verify the detached signature:

~~bash
gpg --verify export.json.sig export.json
~~

The expected result is a valid signature for the current `export.json`.

## Portable Data Boundary

The export contains:

- `user_id`
- `full_name`
- `email`
- `phone`
- `signup_date`
- `preferences`

The following internally generated information is deliberately excluded:

- `internal_risk_score`
- `admin_notes`

This boundary is enforced in both application logic and JSON Schema validation.

## JSON Export Example

~~json
{
  "user_id": "U1001",
  "full_name": "Aisha Al Farsi",
  "email": "aisha@example.com",
  "phone": "+971500000000",
  "signup_date": "2023-01-15",
  "preferences": {
    "newsletter": true
  }
}
~~

## Repository Structure

~~text
secure-data-portability/
├── README.md
├── sample_data.py
├── exporter.py
├── validate.py
├── schema.json
├── export.json
├── export.csv
└── export.json.sig
~~

## Tools Used

- Python 3
- JSON
- CSV
- JSON Schema
- jsonschema
- GnuPG
- OpenSSH
- SFTP
- SHA-256
- Linux shell utilities
- Git

## Key Skills Demonstrated

- Privacy engineering
- Personal-data minimization
- Data portability workflow design
- Python data transformation
- JSON and CSV interoperability
- Nested-data serialization
- JSON Schema enforcement
- Cryptographic integrity verification
- Detached digital signatures
- Secure file transfer
- SSH key-based authentication
- File-integrity comparison
- Reproducible backend compliance controls

## Real-World Use Case

A SaaS, fintech, marketplace, or consumer platform receiving a data-portability request needs to extract only information appropriate for transfer while excluding internal scoring, administrative annotations, and proprietary derived data.

This workflow demonstrates a lightweight implementation in which portable data is filtered programmatically, exported into interoperable formats, cryptographically signed, securely transferred, and validated before delivery.

The same pattern can be extended into production systems using authenticated request workflows, object storage, access control, audit logging, key-management infrastructure, and automated retention policies.

## Lessons Learned

- Privacy requirements are stronger when enforced directly in application logic rather than relying only on procedural documentation.
- Export schemas should reject unexpected properties so accidental disclosure of internal fields fails validation.
- Nested CSV values should use a machine-readable serialization format instead of Python-specific string representations.
- Detached signatures protect integrity without modifying the underlying export.
- Secure delivery should be validated independently using hashes as well as transport-layer protections.

## Troubleshooting Log

### Global pip Missing

The fresh environment contained Python but did not expose pip through the system interpreter.

Resolution:

~~bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv
~~

Python dependencies were then isolated inside a virtual environment.

### Incorrect Portable Field Count

The source instructions described five portable fields, but the supplied field list contained six:

~~text
user_id
full_name
email
phone
signup_date
preferences
~~

The implementation uses all six fields consistently across the exporter and schema.

### Nested CSV Serialization

Using Python `str()` on the preferences dictionary would generate a Python-specific representation:

~~text
{'newsletter': True}
~~

The exporter instead uses JSON serialization:

~~json
{"newsletter":true}
~~

This preserves machine readability.

### Interactive GPG Key Creation

Interactive key generation is inconvenient for repeatable automation.

A dedicated local signing key was therefore generated in batch mode for this disposable environment.

Production signing keys should use stronger private-key protection and preferably dedicated key-management infrastructure.

### Local SFTP Authentication

Interactive localhost SFTP could require a password and interrupt automated execution.

A local ED25519 SSH key was generated and authorized for localhost, allowing reproducible batch-mode SFTP transfer.

### Weak Schema Boundary

A schema that only defines known properties can still accept unexpected additional properties.

The implementation uses:

~~json
"additionalProperties": false
~~

This ensures fields such as `internal_risk_score` or `admin_notes` cause validation failure instead of silently passing.

### File Integrity After Transfer

Successful SFTP transport alone does not prove that delivered files are identical to their sources.

SHA-256 hashes are compared after transfer, and the delivered JSON is independently verified against its detached GPG signature.
