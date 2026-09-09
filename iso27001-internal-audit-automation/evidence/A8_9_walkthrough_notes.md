# Technical Walkthrough Notes

## Control

A.8.9 — Configuration management

## Evidence Source

    /etc/login.defs

## Observed Values

    PASS_MAX_DAYS = 99999
    PASS_MIN_DAYS = 0
    PASS_WARN_AGE = 7

## Simulated Organizational Requirement

The fictitious organization requires:

    Maximum password age <= 90 days

for applicable locally managed password accounts.

## Auditor Evaluation

The observed PASS_MAX_DAYS value is:

    99999

The expected maximum is:

    90

If the observed value exceeds 90, the sampled configuration does not conform to the organization's simulated internal password-aging requirement.

## Evidence Limitation

/etc/login.defs provides default values used when local accounts are created or managed. It does not by itself prove the effective password-aging configuration of every existing account.

A production audit would therefore supplement this evidence with account-level inspection, identity-provider configuration, authentication architecture, and approved configuration standards.
