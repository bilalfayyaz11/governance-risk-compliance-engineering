# Cryptographic Controls Compliance Mapping

## Scope

This document maps the implemented encryption and key-management controls to GDPR Article 32 and the Saudi Personal Data Protection Law (KSA PDPL).

The implementation combines block-level encryption, field-level encryption, centralized secret storage, and encryption-key rotation to reduce the risk of unauthorized disclosure of personal data at rest.

## Control Mapping

| Control Implemented | Technical Mechanism | GDPR Reference | KSA PDPL Reference |
|---|---|---|---|
| Encryption at rest | LUKS2 encrypted block device mounted at `/mnt/secure_pgdata` | Article 32(1)(a) — encryption of personal data | Article 19 — organizational, administrative, and technical measures to protect personal data |
| Field-level encryption | PostgreSQL `pgcrypto` using `pgp_sym_encrypt()` / `pgp_sym_decrypt()` with AES-256 | Article 32(1)(a) — encryption of personal data | Article 19 — technical protection measures |
| Layered confidentiality | LUKS protects physical storage while pgcrypto protects sensitive database fields independently | Article 32(1)(b) — ongoing confidentiality and integrity of processing systems | Article 19 — protection of personal data through technical measures |
| Centralized key management | HashiCorp Vault KV v2 stores the pgcrypto encryption key outside the database | Article 32(1)(b) — ongoing confidentiality and integrity | Article 19 — organizational and technical security measures |
| Key rotation | Vault secret versioning plus PostgreSQL re-encryption using a newly generated key | Article 32(1)(d) — regular testing, assessing, and evaluating security measures | Article 19 — continued implementation of appropriate protective measures |
| Key separation | Encryption keys are maintained outside PostgreSQL rather than stored alongside ciphertext | Article 32(1)(a) and 32(1)(b) | Article 19 — technical and organizational protection |
| Unauthorized-key resistance | Decryption with an incorrect or retired key fails | Article 32(1)(b) — confidentiality and integrity | Article 19 — protection against unauthorized access |
| Cryptographic verification | Ciphertext captured before and after rotation and decryption validated with the active key | Article 32(1)(d) — testing and evaluation of security controls | Article 19 — technical security measures |

## LUKS Encryption at Rest

The database tablespace resides on an ext4 filesystem backed by a LUKS-encrypted block device. Data written into the secure PostgreSQL tablespace is therefore encrypted at the underlying storage layer.

This protects database files if the underlying virtual disk image or storage device is obtained without access to the LUKS unlock secret.

## PostgreSQL Field-Level Encryption

Sensitive national identifier data is additionally protected using PostgreSQL `pgcrypto`.

The implementation uses:

~~sql
pgp_sym_encrypt(
    plaintext,
    encryption_key,
    'cipher-algo=aes256'
)
~~

and authorized decryption uses:

~~sql
pgp_sym_decrypt(
    ciphertext,
    encryption_key
)
~~

This provides a second cryptographic boundary independent of storage-level encryption.

An attacker who gains access to PostgreSQL storage without the field-level key should therefore encounter encrypted values rather than plaintext national identifiers.

## Key Management

The field-encryption key is stored in HashiCorp Vault KV v2 rather than permanently embedded in SQL statements or application files.

The application workflow retrieves the active secret only when cryptographic operations require it.

The local Vault server used here operates in development mode and is intentionally unsuitable for production deployment.

A production implementation should use a persistent, authenticated Vault cluster or a managed KMS/HSM-backed key-management service with:

- Strong operator authentication
- Least-privilege policies
- TLS
- Persistent encrypted storage
- Audit logging
- Secret lifecycle policies
- Key rotation procedures
- Recovery controls
- Restricted administrative access

## Key Rotation

The encryption key was rotated by:

1. Retrieving the currently active key.
2. Generating a new high-entropy key.
3. Storing the new value as another Vault KV version.
4. Decrypting existing ciphertext using the previous key.
5. Immediately re-encrypting the plaintext using the new key.
6. Verifying successful decryption using the new Vault-managed key.
7. Confirming the retired key no longer decrypts the current ciphertext.

This demonstrates key lifecycle management rather than simply changing a stored secret without migrating encrypted data.

## Ciphertext Verification

Ciphertext was captured before and after the rotation operation.

The byte representation changed while the underlying plaintext national identifier remained identical.

Ciphertext differences alone are not definitive proof of key rotation because OpenPGP encryption incorporates randomness. The stronger verification is the combination of:

- A new Vault secret version
- Re-encryption of the database value
- Successful decryption with the new key
- Failure of the retired key against the current ciphertext

## GDPR Article 32 Mapping

GDPR Article 32 requires security measures appropriate to the processing risk.

Article 32(1)(a) specifically includes pseudonymisation and encryption of personal data. LUKS and PostgreSQL field-level encryption directly implement encryption controls at separate layers.

Article 32(1)(b) requires the ability to ensure ongoing confidentiality, integrity, availability, and resilience. Separating encrypted data from centrally managed encryption keys strengthens confidentiality and reduces the impact of compromise of any single system.

Article 32(1)(d) requires a process for regularly testing, assessing, and evaluating technical and organizational measures. Key rotation, ciphertext comparison, correct-key verification, and retired-key failure testing provide technical evidence that cryptographic controls are functioning.

## KSA PDPL Mapping

KSA PDPL Article 19 requires controllers to implement necessary organizational, administrative, and technical measures to protect personal data, including when personal data is transferred.

The implemented LUKS storage encryption, PostgreSQL field encryption, centralized secret management, restricted key handling, and key rotation are technical and organizational safeguards supporting that requirement.

The law establishes the security obligation, while the specific implementation architecture should remain risk-based and appropriate to the sensitivity and context of the personal data being processed.

## Residual Risk

Encryption reduces exposure but does not remove all security risk.

Residual risks include:

- Compromise of Vault credentials
- Privileged PostgreSQL administrator abuse
- Exposure of plaintext while data is actively decrypted
- Shell or process-level secret leakage
- Weak Vault policy design
- Theft of an unlocked system
- Memory scraping
- Backup misconfiguration
- Inadequate key rotation procedures
- Lack of audit logging around key access

Production deployments should therefore combine encryption with access controls, privileged-access management, network segmentation, monitoring, immutable audit logging, secure backups, and incident-response procedures.

## Production Improvements

The current implementation is deliberately compact for local validation.

A production architecture should:

- Replace Vault dev mode with a persistent HA deployment
- Enable TLS for Vault and PostgreSQL
- Use Vault policies instead of a root token
- Prefer a dedicated transit/KMS cryptographic service where practical
- Avoid exposing secret values in command-line arguments
- Use dedicated service identities
- Enable Vault audit devices
- Encrypt and test backups
- Document cryptographic ownership and rotation schedules
- Maintain separation between database administrators and key custodians
- Automate rotation through controlled transactional workflows
