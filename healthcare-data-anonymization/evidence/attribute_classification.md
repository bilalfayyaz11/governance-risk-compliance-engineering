# Attribute Classification

## Direct Identifier Removed

### patient_id

Classification: Direct / persistent identifier

The source dataset contains a unique patient identifier for provenance and
generation purposes, but it is removed from the dataset supplied to the
anonymization process.

A stable unique identifier would enable direct record-level linkage and would
undermine the purpose of k-anonymity if retained unchanged.

---

## Quasi-Identifiers

### zipcode

Classification: Quasi-identifier

A postal code may not identify a person by itself, but in combination with
demographic characteristics it can significantly narrow the candidate
population.

Planned generalization:

5-digit value -> 3-digit prefix -> broader region

---

### age

Classification: Quasi-identifier

Exact age can strongly contribute to re-identification when combined with
location and demographic variables.

Planned generalization:

exact age -> 5-year interval -> decade interval

---

### gender

Classification: Quasi-identifier

Gender is a low-cardinality characteristic but may contribute to linkage when
combined with age, location, nationality, and dates.

---

### nationality

Classification: Quasi-identifier

Nationality may substantially reduce the candidate population when combined
with demographic and geographic attributes.

Planned generalization:

country -> GCC/non-GCC grouping -> broader geographic region

---

### admission_date

Classification: Quasi-identifier

An exact healthcare encounter date may be linkable to external information,
such as workplace absence, public events, insurance records, or knowledge of a
specific hospitalization.

It should therefore not automatically be treated as harmless metadata.

---

## Sensitive Attribute

### diagnosis

Classification: Sensitive attribute

Diagnosis represents health information whose disclosure is the primary
confidentiality concern.

It will be protected using:

- distinct l-diversity
- t-closeness

Diagnosis is not generalized merely as a quasi-identifier; instead, privacy
models will constrain the distribution of diagnoses within equivalence
classes.

---

## Design Rationale

The working anonymization dataset therefore contains no stable direct patient
identifier.

The quasi-identifiers are:

- zipcode
- age
- gender
- nationality
- admission_date

The sensitive attribute is:

- diagnosis

This classification assumes a linkage attacker may possess external
demographic or encounter information.

The privacy model will therefore evaluate combinations of quasi-identifiers
rather than assuming any single field is harmless in isolation.
