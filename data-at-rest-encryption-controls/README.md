# Layered Data-at-Rest Encryption and Key Management

## What This Does

This implementation protects sensitive database information through multiple independent cryptographic layers. PostgreSQL data is stored on a LUKS-encrypted block device, individual sensitive fields are additionally encrypted with PostgreSQL pgcrypto, and encryption keys are managed separately through HashiCorp Vault KV v2.

The architecture demonstrates how infrastructure encryption, database-level cryptography, centralized secret management, and key rotation can work together to reduce the impact of storage, database, or credential compromise.

## Architecture

~~text
                       Application / Administrator
                                  |
                                  v
                    +---------------------------+
                    |       HashiCorp Vault     |
                    |          KV v2            |
                    |                           |
                    | Active pgcrypto key       |
                    | Secret version history    |
                    +-------------+-------------+
                                  |
                           Key retrieval
                                  |
                                  v
                    +---------------------------+
                    |      PostgreSQL           |
                    |      privacy_db           |
                    |                           |
                    | customers                 |
                    |                           |
                    | full_name                 |
                    | national_id_encrypted     |
                    |         BYTEA             |
                    +-------------+-------------+
                                  |
                        pgcrypto AES-256
                                  |
                                  v
                    +---------------------------+
                    | PostgreSQL Tablespace     |
                    |       secure_ts           |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    |      ext4 filesystem      |
                    | /mnt/secure_pgdata        |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    |       LUKS2 / dm-crypt    |
                    |      secure_pgdata        |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    |       Loop Device         |
                    |      db_disk.img          |
                    +---------------------------+
~~

## Prerequisites

- Ubuntu 22.04+ or equivalent Linux environment
- sudo/root privileges
- cryptsetup
- util-linux loop-device tooling
- ext4 filesystem utilities
- PostgreSQL
- PostgreSQL contrib extensions
- pgcrypto
- HashiCorp Vault
- OpenSSL
- jq
- Git

The host must support Linux loop devices and device-mapper/dm-crypt functionality.

## Setup & Installation

~~bash
sudo apt update

sudo apt install -y \
  cryptsetup \
  postgresql \
  postgresql-contrib \
  ca-certificates \
  gnupg \
  wget \
  unzip \
  jq

wget -qO- https://apt.releases.hashicorp.com/gpg \
| gpg --dearmor \
| sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg >/dev/null

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(. /etc/os-release && echo "$UBUNTU_CODENAME") main" \
| sudo tee /etc/apt/sources.list.d/hashicorp.list >/dev/null

sudo apt update
sudo apt install -y vault

sudo systemctl enable --now postgresql
~~

Verify:

~~bash
cryptsetup --version
psql --version
vault --version
pg_isready
~~

## How to Reproduce

### 1. Create the Virtual Block Device

~~bash
sudo fallocate -l 1G /var/lib/db_disk.img

LOOP_DEV=$(sudo losetup --find --show /var/lib/db_disk.img)

echo "$LOOP_DEV"
~~

Using dynamic loop-device discovery prevents assumptions about whether the available device is `/dev/loop0`, `/dev/loop10`, or another identifier.

### 2. Initialize LUKS Encryption

~~bash
sudo cryptsetup luksFormat "$LOOP_DEV"
~~

Confirm the destructive initialization by typing:

~~text
YES
~~

and configure a strong temporary unlock passphrase.

Open the encrypted mapping:

~~bash
sudo cryptsetup luksOpen "$LOOP_DEV" secure_pgdata
~~

Create an ext4 filesystem:

~~bash
sudo mkfs.ext4 -F /dev/mapper/secure_pgdata
~~

### 3. Mount the Encrypted Storage

~~bash
sudo mkdir -p /mnt/secure_pgdata

sudo mount \
  /dev/mapper/secure_pgdata \
  /mnt/secure_pgdata

sudo chown postgres:postgres /mnt/secure_pgdata
sudo chmod 700 /mnt/secure_pgdata
~~

Verify:

~~bash
sudo cryptsetup status secure_pgdata

lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS

findmnt /mnt/secure_pgdata
~~

The expected storage chain is conceptually:

~~text
db_disk.img
     |
loop device
     |
LUKS / dm-crypt
     |
ext4
     |
/mnt/secure_pgdata
~~

### 4. Create the PostgreSQL Tablespace

~~bash
sudo -u postgres psql \
-c "CREATE TABLESPACE secure_ts LOCATION '/mnt/secure_pgdata';"
~~

Create the protected database:

~~bash
sudo -u postgres createdb \
  --tablespace=secure_ts \
  privacy_db
~~

Verify:

~~bash
sudo -u postgres psql -c "\db+"
~~

### 5. Enable PostgreSQL Field Encryption

~~bash
sudo -u postgres psql -d privacy_db <<'SQL'
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name TEXT,
    national_id_encrypted BYTEA
);
SQL
~~

Generate a high-entropy temporary encryption key:

~~bash
DEMO_KEY=$(openssl rand -base64 32 | tr -d '\n')
~~

Insert encrypted personal data:

~~bash
sudo -u postgres psql \
-d privacy_db \
-v enc_key="$DEMO_KEY" <<'SQL'
INSERT INTO customers (
    full_name,
    national_id_encrypted
)
VALUES (
    'Ahmed Al-Farsi',
    pgp_sym_encrypt(
        '784-1990-1234567',
        :'enc_key',
        'cipher-algo=aes256'
    )
);
SQL
~~

### 6. Verify Ciphertext and Decryption

Display the raw encrypted representation:

~~bash
sudo -u postgres psql -d privacy_db \
-c "SELECT id, full_name, encode(national_id_encrypted, 'hex') AS ciphertext_hex FROM customers;"
~~

Decrypt using the correct key:

~~bash
sudo -u postgres psql \
-d privacy_db \
-v enc_key="$DEMO_KEY" <<'SQL'
SELECT
    full_name,
    pgp_sym_decrypt(
        national_id_encrypted,
        :'enc_key'
    ) AS national_id
FROM customers;
SQL
~~

A different key should fail authentication/decryption.

### 7. Start HashiCorp Vault

Development mode was used only for isolated local validation:

~~bash
vault server \
  -dev \
  -dev-root-token-id="root-dev-token" \
  -dev-listen-address="127.0.0.1:8200"
~~

Configure the client:

~~bash
export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_TOKEN="root-dev-token"
~~

Vault dev mode and predictable root credentials must never be used in production.

### 8. Store the pgcrypto Key in Vault

Enable KV v2 if required:

~~bash
vault secrets enable -path=secret kv-v2
~~

Store the encryption key:

~~bash
vault kv put secret/pii-key value="$DEMO_KEY"
~~

Retrieve:

~~bash
VAULT_KEY=$(vault kv get -field=value secret/pii-key)
~~

Use the Vault-managed value to perform authorized database decryption.

### 9. Remove Temporary Local Key Material

Once the original key has been migrated into Vault:

~~bash
shred -u /tmp/privacy_db_demo_key
~~

Temporary plaintext secret material should not remain unnecessarily on disk.

### 10. Rotate the Encryption Key

Retrieve the currently active key:

~~bash
OLD_KEY=$(vault kv get -field=value secret/pii-key)
~~

Generate a replacement:

~~bash
NEW_KEY=$(openssl rand -base64 32 | tr -d '\n')
~~

Create a new Vault KV version:

~~bash
vault kv put secret/pii-key value="$NEW_KEY"
~~

Re-encrypt existing data:

~~bash
sudo -u postgres psql \
-d privacy_db \
-v old_key="$OLD_KEY" \
-v new_key="$NEW_KEY" <<'SQL'
UPDATE customers
SET national_id_encrypted =
    pgp_sym_encrypt(
        pgp_sym_decrypt(
            national_id_encrypted,
            :'old_key'
        ),
        :'new_key',
        'cipher-algo=aes256'
    );
SQL
~~

### 11. Verify Rotation

Retrieve the current Vault key:

~~bash
CURRENT_KEY=$(vault kv get -field=value secret/pii-key)
~~

Validate the new key:

~~bash
sudo -u postgres psql \
-d privacy_db \
-v enc_key="$CURRENT_KEY" <<'SQL'
SELECT
    pgp_sym_decrypt(
        national_id_encrypted,
        :'enc_key'
    )
FROM customers;
SQL
~~

Attempting to decrypt the current ciphertext with the retired key should fail.

Ciphertext should also differ after re-encryption:

~~sql
SELECT
    id,
    encode(national_id_encrypted, 'hex')
FROM customers;
~~

Ciphertext differences by themselves are not definitive proof of key rotation because OpenPGP encryption uses randomness. Stronger evidence is:

- Vault secret version incremented
- Data was re-encrypted
- New key successfully decrypts
- Retired key fails against current ciphertext

## Tools Used

- Linux
- LUKS2
- dm-crypt
- cryptsetup
- Loop devices
- ext4
- PostgreSQL
- PostgreSQL tablespaces
- pgcrypto
- AES-256
- HashiCorp Vault
- Vault KV v2
- OpenSSL
- jq
- Git

## Key Skills Demonstrated

- Implementing block-level encryption with LUKS
- Building encrypted PostgreSQL storage architectures
- Configuring PostgreSQL tablespaces
- Applying field-level encryption to sensitive data
- Managing encryption keys independently from ciphertext
- Integrating HashiCorp Vault with database cryptography
- Performing cryptographic key rotation
- Migrating existing ciphertext to new encryption keys
- Testing retired-key failure
- Validating encryption controls with technical evidence
- Implementing defense-in-depth for personal data
- Translating regulatory security requirements into infrastructure controls

## Real-World Use Case

A company processing sensitive customer information may need multiple encryption boundaries instead of relying exclusively on cloud-disk encryption. Database storage can reside on encrypted infrastructure while particularly sensitive columns, such as government identifiers, are independently encrypted at the database layer.

Centralized key management ensures the cryptographic secret is separated from the ciphertext. This architecture reduces the impact of storage theft, database-file exposure, backup compromise, and unauthorized database access while supporting controlled key lifecycle operations.

## Lessons Learned

- Storage encryption and field encryption protect against different compromise scenarios and work best as complementary controls.
- Cryptographic keys should not be permanently embedded in SQL, source code, or configuration files.
- Database tablespaces provide a controlled way to place PostgreSQL workloads on dedicated encrypted storage.
- Key rotation is incomplete unless existing ciphertext is migrated to the replacement key.
- Successful new-key decryption and retired-key failure provide stronger evidence of rotation than ciphertext comparison alone.
- Linux loop devices and device-mapper capabilities must be verified before attempting LUKS workflows in hosted environments.
- Development-mode secret managers provide useful demonstrations but do not reproduce production security guarantees.

## Troubleshooting Log

### LUKS Confirmation Requires Uppercase YES

During LUKS initialization, cryptsetup displayed:

~~text
Are you sure? (Type 'yes' in capital letters):
~~

Entering lowercase:

~~text
yes
~~

caused the operation to abort.

The required confirmation is:

~~text
YES
~~

### Dynamic Loop Device Selection

Hardcoding a loop device such as:

~~text
/dev/loop0
~~

is unreliable because hosted machines can already have several loop devices assigned.

The implementation instead uses:

~~bash
sudo losetup --find --show /var/lib/db_disk.img
~~

to allocate and capture the correct available device.

### CREATE TABLESPACE Transaction Restriction

An initial idempotency approach attempted to execute `CREATE TABLESPACE` from inside a PostgreSQL `DO` block.

PostgreSQL rejected this because `CREATE TABLESPACE` cannot execute inside a transaction/function context.

The corrected implementation checks existence first from the shell and then executes:

~~bash
sudo -u postgres psql \
-c "CREATE TABLESPACE secure_ts LOCATION '/mnt/secure_pgdata';"
~~

as a standalone PostgreSQL command.

### Encryption Key Separation

The initial field-encryption key existed temporarily outside Vault so that the encrypted database record could be created.

After Vault was initialized, the key was transferred to KV v2 and the temporary local key file was removed.

Production systems should avoid this bootstrap pattern where possible and generate or control key material directly through approved cryptographic infrastructure.

### Vault Dev Mode

The implementation uses:

~~text
vault server -dev
~~

for isolated testing.

Dev mode:

- Operates in memory
- Uses simplified initialization
- Is automatically unsealed
- Uses a root-level token
- Does not provide production persistence or resilience

It must never be used as a production Vault deployment.

### Shell Secret Exposure

Retrieving a key into a shell variable is convenient for controlled demonstration:

~~bash
KEY=$(vault kv get -field=value secret/pii-key)
~~

but production systems should avoid exposing long-lived secrets through shell state, process arguments, logs, or command history.

Applications should authenticate directly to the secret-management platform using narrowly scoped machine identities.

## Compliance Mapping

### GDPR Article 32

The implemented architecture supports security-of-processing controls through encryption, confidentiality safeguards, and technical verification.

LUKS and pgcrypto provide independent encryption layers, while Vault separates key material from encrypted data. Key rotation and retired-key testing provide repeatable evidence that cryptographic controls remain operational.

### KSA PDPL

The architecture supports the technical and organizational security measures required for protecting personal data under KSA PDPL security obligations.

Disk encryption, field encryption, centralized key management, controlled key lifecycle operations, and separation of key material from encrypted personal data collectively reduce the likelihood and impact of unauthorized disclosure.

See `compliance_mapping.md` for the detailed implementation-to-control mapping.

## Production Improvements

A production implementation should additionally:

- Replace Vault dev mode with a persistent HA deployment
- Use TLS for PostgreSQL and Vault
- Authenticate workloads through dedicated machine identities
- Use Vault policies instead of root credentials
- Enable Vault audit logging
- Prefer HSM/KMS-backed root key protection
- Define formal cryptographic rotation schedules
- Implement transactional and recoverable re-encryption workflows
- Secure and test encrypted backups
- Separate key custodians from database administrators
- Monitor cryptographic and privileged-access events
- Prevent sensitive keys from appearing in shell history or process arguments
