# Security Assessment Report

## 1. Executive Summary

A technical security control assessment was performed against `ip-172-31-10-5` using OpenSCAP and the Canonical Ubuntu 24.04 Security Technical Implementation Guide profile. The assessment used `xccdf_org.ssgproject.content_profile_stig` from `ssg-ubuntu2404-ds.xml`.

The initial assessment recorded **62 passing** and **88 failing** evaluated rules. Following controlled remediation, the follow-up assessment recorded **68 passing** and **163 failing** rules.

The number of failed rules changed by **-75**. OpenSCAP evidence explicitly verified **1** selected remediation result(s) as transitioning from fail to pass.

The pass percentages reported in this document are simple ratios of passing rules to passing-plus-failing rules. They are assessment metrics for this report and must not be interpreted as an official DISA STIG compliance score, accreditation decision, or authorization to operate.

## 2. Assessment Scope and Methodology

- **Target system:** `ip-172-31-10-5`
- **Operating system:** Ubuntu 24.04 LTS
- **Assessment tool:** OpenSCAP
- **SCAP datastream:** `ssg-ubuntu2404-ds.xml`
- **Profile:** `xccdf_org.ssgproject.content_profile_stig`
- **Assessment type:** Automated technical configuration review
- **Assessor:** Bilal Fayyaz
- **System owner:** Linux Workload Operations Team
- **Report generated:** 2026-09-07 14:48:27 UTC

The assessment followed an evidence-driven workflow consisting of assessment planning, automated baseline evaluation, findings triage, controlled remediation of selected low-risk findings, follow-up evaluation, and preservation of cryptographic evidence hashes.

The Security Assessment Plan and assessor independence statement are maintained in `plans/assessment_plan.md`.

## 3. Results Summary

| Metric | Initial Assessment | Follow-up Assessment |
|---|---:|---:|
| Pass | 62 | 68 |
| Fail | 88 | 163 |
| Not Applicable | 86 | 4 |
| Not Selected | 408 | 408 |
| Not Checked | 4 | 5 |
| Error | 0 | 0 |
| Simple Pass Rate | 41.33% | 29.44% |

**Failed-rule reduction:** -75

## 4. Detailed Findings

| Rule | Finding | Severity | Risk | Owner | Target Date | Status |
|---|---|---|---|---|---|---|
| `xccdf_org.ssgproject.content_rule_dconf_gnome_disable_ctrlaltdel_reboot` | Disable Ctrl-Alt-Del Reboot Key Sequence in GNOME3 | CAT I | High | Linux Workload Operations Team | 2026-10-07 | Open |
| `xccdf_org.ssgproject.content_rule_disable_ctrlaltdel_reboot` | Disable Ctrl-Alt-Del Reboot Activation | CAT I | High | Linux Workload Operations Team | 2026-10-07 | Open |
| `xccdf_org.ssgproject.content_rule_grub2_password` | Set Boot Loader Password in grub2 | CAT I | High | Linux Workload Operations Team | 2026-10-07 | Open |
| `xccdf_org.ssgproject.content_rule_grub2_uefi_password` | Set the UEFI Boot Loader Password | CAT I | High | Linux Workload Operations Team | 2026-10-07 | Open |
| `xccdf_org.ssgproject.content_rule_is_fips_mode_enabled` | Verify '/proc/sys/crypto/fips_enabled' exists | CAT I | High | Linux Workload Operations Team | 2026-10-07 | Open |

## 5. Remediation Status

- Verified selected remediations: **1**
- Remaining failed rules after follow-up assessment: **163**
- Triage records marked remediated/verified: **0**
- Open triage records: **5**

### Verification Evidence

    xccdf_org.ssgproject.content_rule_package_aide_installed: fail -> fail [NOT VERIFIED]
    xccdf_org.ssgproject.content_rule_package_audit_installed: fail -> pass [VERIFIED]

Remediation was deliberately limited to selected low-risk configuration changes. High-impact controls affecting remote access, authentication, boot configuration, networking, or other availability-sensitive components were not changed solely to increase the automated assessment result.

## 6. Assessor Conclusion

The follow-up assessment continues to report **163 failed technical rules**. Therefore, this assessment does not support a conclusion that the target is fully compliant with the selected STIG baseline.

Unresolved findings should be reviewed by the system owner, validated for applicability and operational impact, and tracked through an appropriate remediation or POA&M process. Findings that cannot be remediated should have documented risk treatment, compensating controls, or formally approved exceptions as appropriate.

OpenSCAP provides evidence for machine-testable technical controls; procedural, organizational, physical, and manually assessed controls remain outside the scope of this automated assessment unless separately evaluated.

## 7. Assessment Limitations

- The assessment represents the configuration state observed at scan time.
- Automated checks do not cover every security or governance control.
- Not-applicable and not-selected rules require contextual interpretation where material to the authorization boundary.
- Remediation was intentionally constrained to avoid unsafe changes to the remotely administered assessment host.
- Simple pass-rate calculations in this report are informational assessment metrics rather than an official compliance score.

## 8. Evidence and Appendices

- `plans/assessment_plan.md` — Security Assessment Plan
- `results/scan-results.xml` — Initial XCCDF evidence
- `results/scan-report.html` — Initial human-readable report
- `results/all-failed-findings.csv` — Complete failed-rule inventory
- `results/findings_triage.csv` — Prioritized findings register
- `results/remediation-record.txt` — Remediation activity record
- `results/remediation-verification.txt` — Rule-level verification
- `results/rescan-results.xml` — Follow-up XCCDF evidence
- `results/rescan-report.html` — Follow-up human-readable report
- `results/initial-evidence.sha256` — Initial evidence hashes
- `results/remediation-evidence.sha256` — Follow-up evidence hashes

The superseded `profile_standard` scan is retained separately under `results/invalid-standard-profile-scan/` and is not used as evidence for the conclusions in this report.

