# Interview Log

- Auditee Name/Role: Hamza Siddiqui — Cloud Infrastructure Lead
- Date/Time: 2026-09-10 11:00
- Control(s) Discussed: A.8.9 Configuration management
- Interviewer: Omar Khan — Technical Auditor
- Location / Medium: Virtual interview

## Questions Asked

1. How are baseline configurations defined for production Linux systems?
2. How are configuration changes approved and tracked?
3. How frequently are security-related configuration settings reviewed?
4. How are deviations from approved configuration standards identified?

## Responses Summary

- Production systems are provisioned from standardized infrastructure templates.
- Changes to operating system and cloud configuration are expected to follow change-management approval.
- The infrastructure team performs periodic configuration review, but password-aging parameters on local Linux hosts are not currently included in a formal automated compliance baseline.
- Configuration drift is mainly detected through engineering review and operational monitoring rather than a dedicated configuration-compliance platform.

## Evidence Collected

- evidence/A8_9_password_policy_evidence.txt
- evidence/A8_9_walkthrough_notes.md

## Auditor Assessment

Configuration-management practices exist, but evidence indicates that at least one local account password-aging setting materially exceeds the organization's simulated internal requirement of 90 days.

This represents an isolated implementation gap rather than evidence that the entire configuration-management process is absent.

## Follow-Up Required

- Review the approved Linux password-aging baseline.
- Correct PASS_MAX_DAYS where local password authentication is applicable.
- Consider automated configuration-compliance checks for security-sensitive operating system settings.
