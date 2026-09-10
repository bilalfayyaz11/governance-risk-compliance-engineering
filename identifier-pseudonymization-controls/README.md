# Identifier Pseudonymization and Controlled Reidentification

## What This Does

This implementation protects sensitive identifiers by replacing real Emirates IDs with deterministic pseudonymous tokens while preserving their original structural format. PostgreSQL separates raw and pseudonymized operational data, while the reversible token mapping and HMAC key are isolated in a restricted filesystem vault. A controlled reidentification path allows authorized recovery of original identifiers without exposing the vault to normal application users.

The design demonstrates practical privacy engineering controls for reducing direct identifier exposure while maintaining controlled reversibility where legitimate business or regulatory processes require it.

## Architecture

~~text
                          Sensitive Customer Data
                                   |
                                   v
                     +---------------------------+
                     | PostgreSQL raw_data       |
                     |                           |
                     | customers                 |
                     | - customer_id             |
                     | - full_name               |
                     | - Emirates ID             |
                     | - phone                   |
                     +-------------+-------------+
                                   |
                                   |
                           Authorized Read
                                   |
                                   v
                     +---------------------------+
                     | Python Tokenization       |
                     | tokenize.py               |
                     |                           |
                     | HMAC-SHA256               |
                     | deterministic mapping     |
                     | format preservation       |
                     +------+-------------+------+
                            |             |
                Tokenized   |             | Original Mapping
                Dataset     |             |
                            v             v
              +-------------------+   +-------------------------+
              | PostgreSQL        |   | Restricted Token Vault  |
              | pseudonymized     |   |                         |
              |                   |   | ~/secure_vault          |
              | customers         |   |                         |
              | - customer_id     |   | vault.json   [600]      |
              | - name            |   | vault.key    [600]      |
              | - token           |   | directory    [700]      |
              | - phone           |   +------------+------------+
              +---------+---------+                |
                        |                          |
                        | Normal Processing        | Privileged Access
                        v                          v
                +---------------+         +----------------------+
                | Application   |         | reidentify.py        |
                | / Analytics   |         | Authorized Recovery  |
                +---------------+         +----------+-----------+
                                                    |
                                                    v
                                         Original Emirates ID
~~

## Prerequisites

- Ubuntu 22.04+ or equivalent Linux environment
- Python 3.10+
- Python virtual environment support
- PostgreSQL
- PostgreSQL command-line client
- Python `psycopg2-binary`
- Python `cryptography`
- OpenSSL
- Git
- sudo privileges for PostgreSQL administration

## Setup & Installation

~~bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib python3-venv

sudo systemctl enable --now postgresql

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install psycopg2-binary cryptography
~~

Verify PostgreSQL:

~~bash
psql --version
pg_isready
systemctl is-active postgresql
~~

## How to Reproduce

### 1. Create the PostgreSQL Database

~~bash
sudo -u postgres createdb privacy_lab
~~

Create the application role:

~~bash
sudo -u postgres psql <<'SQL'
CREATE ROLE lab_app LOGIN PASSWORD 'LabPass123';
SQL
~~

Grant database access:

~~bash
sudo -u postgres psql -d privacy_lab <<'SQL'
GRANT CONNECT ON DATABASE privacy_lab TO lab_app;
SQL
~~

The password shown above is intended only for an isolated demonstration environment. Production credentials should be managed through a dedicated secrets-management system.

### 2. Create the Raw Identifier Schema

~~bash
sudo -u postgres psql -d privacy_lab <<'SQL'
CREATE SCHEMA raw_data;

CREATE TABLE raw_data.customers (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    emirates_id VARCHAR(20) NOT NULL,
    phone VARCHAR(15)
);

INSERT INTO raw_data.customers
(full_name, emirates_id, phone)
VALUES
('Ahmed Al Mansoori', '784-1990-1234567-1', '0501234567'),
('Fatima Al Suwaidi', '784-1985-7654321-2', '0559876543'),
('Sara Khan', '784-1992-1112223-4', '0521112233');

GRANT USAGE ON SCHEMA raw_data TO lab_app;
GRANT SELECT ON raw_data.customers TO lab_app;
SQL
~~

Verify:

~~bash
sudo -u postgres psql -d privacy_lab \
-c "SELECT count(*) FROM raw_data.customers;"
~~

Expected row count:

~~text
3
~~

### 3. Generate Deterministic Tokens

Activate the Python environment:

~~bash
source .venv/bin/activate
~~

Run:

~~bash
python tokenize.py
~~

The tokenization workflow:

1. Reads customer IDs and Emirates IDs from PostgreSQL.
2. Loads an existing tokenization key or generates one on first execution.
3. Computes an HMAC-SHA256 value for the sensitive identifier suffix.
4. Compresses the result into an eight-digit numeric token.
5. Reconstructs the value using the original Emirates ID pattern.
6. Stores reversible token-to-identifier mappings in the token vault.

Example structure:

~~text
Original:
784-1990-1234567-1

Pseudonymized:
784-1990-XXXXXXX-X
~~

The transformation preserves the structural pattern required by downstream systems while replacing the sensitive identifier component.

### 4. Preserve Token Determinism

The tokenization key is generated only when no existing key is available.

Conceptually:

~~text
vault.key exists
        |
       YES
        |
        v
Reuse existing key
        |
        v
Same input produces same token


vault.key missing
        |
        v
Generate 32-byte key
        |
        v
Persist securely
~~

This prevents token values from changing whenever the tokenization process is executed again.

### 5. Isolate the Token Vault

Create the restricted location:

~~bash
mkdir -p ~/secure_vault

mv vault.json vault.key ~/secure_vault/

chmod 700 ~/secure_vault
chmod 600 ~/secure_vault/vault.json
chmod 600 ~/secure_vault/vault.key
~~

Verify:

~~bash
stat -c "%a %U:%G %n" \
~/secure_vault \
~/secure_vault/vault.json \
~/secure_vault/vault.key
~~

Expected permissions:

~~text
700 secure_vault
600 vault.json
600 vault.key
~~

The token vault and cryptographic key must never be available to normal application identities.

### 6. Create the Pseudonymized Data Store

~~bash
sudo -u postgres psql -d privacy_lab <<'SQL'
CREATE SCHEMA pseudonymized;

CREATE TABLE pseudonymized.customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(100),
    emirates_id_token VARCHAR(20) NOT NULL,
    phone VARCHAR(15)
);

GRANT USAGE ON SCHEMA pseudonymized TO lab_app;
GRANT SELECT, INSERT, DELETE ON pseudonymized.customers TO lab_app;
SQL
~~

Create the privileged reidentification database role:

~~bash
sudo -u postgres psql -d privacy_lab <<'SQL'
CREATE ROLE reidentify_role LOGIN PASSWORD 'ReidPass123';

REVOKE ALL ON SCHEMA raw_data FROM reidentify_role;
SQL
~~

The demonstration password should not be reused outside an isolated environment.

### 7. Load Tokenized Records

Run:

~~bash
python load_tokens.py
~~

Verify:

~~bash
sudo -u postgres psql -d privacy_lab \
-c "SELECT customer_id, full_name, emirates_id_token, phone FROM pseudonymized.customers ORDER BY customer_id;"
~~

The pseudonymized table should contain structural tokens rather than original Emirates IDs.

Check that no original IDs were copied into the token field:

~~bash
sudo -u postgres psql -d privacy_lab -tAc \
"SELECT COUNT(*) FROM pseudonymized.customers
 WHERE emirates_id_token IN (
     SELECT emirates_id FROM raw_data.customers
 );"
~~

Expected result:

~~text
0
~~

### 8. Perform Controlled Reidentification

Retrieve a test token:

~~bash
TEST_TOKEN=$(sudo -u postgres psql -d privacy_lab -tAc \
"SELECT emirates_id_token
 FROM pseudonymized.customers
 ORDER BY customer_id
 LIMIT 1;" | xargs)

echo "$TEST_TOKEN"
~~

Run the authorized recovery path:

~~bash
printf '%s\n' "$TEST_TOKEN" | python reidentify.py
~~

Successful output returns the associated customer and original identifier.

Example:

~~text
{
    'customer_id': 1,
    'original_id': '784-1990-1234567-1'
}
~~

Invalid tokens return:

~~text
{'error': 'Token not found'}
~~

### 9. Test Filesystem Separation

A PostgreSQL role is not a Linux operating-system identity, so filesystem permissions must be tested using a real non-owner OS user.

Create a restricted test identity:

~~bash
sudo useradd \
--system \
--no-create-home \
--shell /usr/sbin/nologin \
vault_test_user
~~

Attempt vault access:

~~bash
sudo -u vault_test_user cat ~/secure_vault/vault.json
~~

The request should fail with permission denied.

This demonstrates that possession of ordinary application access does not automatically expose the reversible token mapping.

### 10. Validate Database Separation

Verify that the privileged reidentification database role cannot access the raw schema:

~~bash
sudo -u postgres psql -d privacy_lab -c \
"SELECT has_schema_privilege(
    'reidentify_role',
    'raw_data',
    'USAGE'
) AS raw_schema_usage;"
~~

Expected result:

~~text
f
~~

### 11. Validate Python Source

~~bash
python -m py_compile \
tokenize.py \
load_tokens.py \
reidentify.py
~~

## Tools Used

- PostgreSQL
- Python 3
- psycopg2
- HMAC-SHA256
- hashlib
- Python secrets / os random generation
- JSON
- Linux filesystem permissions
- PostgreSQL roles and schemas
- OpenSSL
- Git

## Key Skills Demonstrated

- Designing pseudonymization controls for sensitive identifiers
- Implementing deterministic HMAC-based tokenization
- Preserving identifier format for downstream compatibility
- Separating raw and pseudonymized data using PostgreSQL schemas
- Applying least-privilege database permissions
- Building reversible token vaults
- Protecting key material using restrictive Linux permissions
- Designing controlled reidentification workflows
- Detecting token collisions
- Managing cryptographic key persistence
- Enforcing separation of duties between processing and reidentification
- Documenting residual privacy and cryptographic risk
- Translating privacy requirements into technical security controls

## Real-World Use Case

Organizations frequently need operational systems, analytics workloads, AI pipelines, and engineering teams to process customer records without exposing direct government-issued identifiers. This architecture allows those systems to operate on stable pseudonymous identifiers while the reversible linkage remains isolated behind a privileged trust boundary.

In production, the local vault would typically be replaced with a dedicated secrets or key-management service, reidentification would require strong authorization and audit logging, and separate service identities would handle ingestion, operational processing, and privileged recovery.

## Lessons Learned

- Pseudonymization reduces exposure but does not make personal data anonymous.
- Deterministic tokenization requires persistent key management; regenerating the key changes every derived token.
- A cryptographic key and reversible mapping require stronger protection than ordinary application data.
- PostgreSQL roles and Linux users are separate security identities and cannot be treated interchangeably.
- Database schema separation helps enforce different trust levels for raw and pseudonymized information.
- Reidentification should be treated as a privileged event rather than ordinary application functionality.
- Restricting vault permissions provides an additional boundary even when an application database is compromised.
- A reduced numeric token space introduces collision risk and should be evaluated before production deployment.

## Troubleshooting Log

### Cryptography Package Missing Inside Virtual Environment

The host operating system already contained the `cryptography` package, but the newly created Python virtual environment did not inherit system-level packages.

The package was installed directly into the isolated environment:

~~bash
source .venv/bin/activate
python -m pip install cryptography
~~

This ensures all Python dependencies are available from the same reproducible runtime.

### Random Key Regeneration

The initial implementation generated the key using:

~~python
SECRET_KEY = os.urandom(32)
~~

on every application execution.

That approach breaks deterministic tokenization because identical source identifiers generate different tokens after every restart.

The implementation instead follows:

~~text
Existing key -> load key
Missing key  -> generate once -> persist securely
~~

This preserves stable token mappings.

### PostgreSQL Role Is Not an Operating-System User

A database role created with:

~~sql
CREATE USER lab_app;
~~

exists only inside PostgreSQL.

It cannot be used automatically with:

~~bash
sudo -u lab_app
~~

because `sudo` requires an operating-system account.

A dedicated non-owner Linux identity was therefore used to verify filesystem access denial.

### Token Collision Risk

The HMAC-SHA256 result is reduced to an eight-digit numeric value in order to preserve the identifier's expected structure.

Because the output space is smaller than the full cryptographic digest space, collisions are theoretically possible.

The implementation detects duplicate generated tokens and fails rather than silently overwriting an existing mapping.

### Database Permission Separation

The `reidentify_role` is explicitly denied access to the raw identifier schema.

Normal application access to the pseudonymized dataset therefore remains logically separate from raw identifier access.

### Local Key Storage

The demonstration stores the HMAC key as:

~~text
~/secure_vault/vault.key
~~

with restrictive permissions.

Production implementations should instead use:

- Cloud KMS
- Hardware Security Modules
- HashiCorp Vault
- Enterprise key-management platforms

Key retrieval, rotation, and use should be logged and independently authorized.

## Residual Risk and Production Controls

### Residual Re-identification Risk

Pseudonymization does not eliminate reidentification risk. Compromise of the token vault or HMAC key could allow an attacker to recover or regenerate mappings between pseudonymous values and original Emirates IDs.

The intentionally constrained eight-digit token space also creates more collision and enumeration exposure than a full-length cryptographic identifier. Tokenized data should therefore continue to be treated as protected personal data.

### Key Management

Production key material should be generated and controlled through dedicated cryptographic infrastructure such as an HSM, managed KMS, or enterprise secrets platform.

Applications should receive only narrowly scoped permission to invoke required cryptographic operations. Key access, rotation, recovery, and administrative activity should be logged and periodically reviewed.

### Access Control

Reidentification should be restricted to explicitly authorized privacy, security, or governance personnel and should require legitimate business justification.

Strong authentication, least privilege, approval workflows, and immutable reidentification logs should protect the recovery path.

### Separation of Duties

Raw identifiers, operational pseudonymous data, and reversible mappings serve different security purposes and should remain under separate trust boundaries.

A compromise of an operational application should therefore not automatically expose the cryptographic key, token vault, or original sensitive identifiers.

## Security Notes

Never commit or distribute:

~~text
vault.key
vault.json
~~

The key contains cryptographic secret material, while the vault contains direct mappings back to original identifiers.

Production systems should additionally implement:

- TLS for database connections
- Encrypted database storage
- Encrypted backups
- Central secrets management
- Key rotation
- Immutable access logging
- Dual authorization for sensitive reidentification
- Privileged-access monitoring
- Dedicated service identities
- Regular permission reviews
