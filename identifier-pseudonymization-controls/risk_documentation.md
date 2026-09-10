# Pseudonymization Risk and Key Management Controls

## 1. Residual Re-identification Risk

Pseudonymization reduces direct exposure of Emirates IDs, but it does not eliminate the possibility of re-identification. If the token vault or HMAC key is compromised, an attacker could recover the original identifiers or regenerate valid mappings; additionally, compressing HMAC output into an 8-digit numeric space introduces a finite collision space and makes exhaustive token-space analysis more feasible than with full-length cryptographic identifiers.

Residual risk therefore depends heavily on vault isolation, key secrecy, access logging, and the strength of surrounding infrastructure controls. The tokenized dataset should still be treated as sensitive personal data rather than anonymous data.

## 2. Key Management

The tokenization key should not be stored as a local application file in production. It should be generated, protected, rotated, and accessed through a dedicated secrets or key-management platform such as a cloud KMS, hardware security module, or an enterprise secrets platform such as HashiCorp Vault.

Application workloads should receive only narrowly scoped permission to perform required cryptographic operations or retrieve the key when absolutely necessary. Key access should be logged, monitored, periodically reviewed, and separated from normal database administration privileges.

## 3. Access Control Mapping

Only explicitly authorized privacy, security, or data-governance personnel should be permitted to execute the reidentification workflow. Access should require privileged authentication, least-privilege authorization, business justification, and auditable logging rather than being available to normal application users.

This supports GDPR Article 32 by applying technical and organizational safeguards to personal-data processing, including confidentiality and controlled access. It also aligns with data-minimization principles by ensuring most operational users work only with pseudonymized identifiers and obtain the original identifier only when a legitimate processing purpose requires it.

## 4. Separation of Duties

The raw dataset, pseudonymized dataset, and token vault are deliberately separated because each serves a different trust level. The raw PostgreSQL schema contains directly identifying information, the pseudonymized schema supports routine operational processing, and the vault provides the privileged linkage necessary to reverse a token.

Keeping these components under different access boundaries reduces the impact of a single account or system compromise. An attacker or unauthorized employee who gains access only to the pseudonymized database should not automatically gain access to the original identifiers or the tokenization key.

## Additional Production Controls

- Replace local database passwords with centrally managed secrets.
- Use separate service identities for ingestion, operational reads, and reidentification.
- Store cryptographic keys in KMS/HSM-backed infrastructure.
- Rotate keys according to documented cryptographic lifecycle procedures.
- Record every authorized reidentification event in an immutable audit log.
- Require approval or dual authorization for sensitive reidentification operations.
- Encrypt database storage, backups, and vault data at rest.
- Encrypt administrative and application connections in transit.
- Monitor unusual token lookup and reidentification activity.
- Periodically review database roles, filesystem permissions, and privileged accounts.
