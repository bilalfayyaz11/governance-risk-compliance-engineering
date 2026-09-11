# Healthcare Data Anonymization with ARX

## Overview

This implementation demonstrates a reproducible privacy-preserving data
transformation workflow for healthcare records using the ARX Data
Anonymization Tool.

The workflow combines:

- direct-identifier removal
- quasi-identifier modeling
- hierarchical generalization
- k-anonymity
- distinct l-diversity
- t-closeness
- suppression controls
- re-identification risk analysis
- information-loss analysis
- privacy/compliance assessment

The objective is to reduce linkage and sensitive-attribute disclosure risk
while preserving useful analytical structure.

---

## Privacy Model

The ARX configuration enforces:

~~text
k-anonymity        = 5
distinct l         = 3
t-closeness        = 0.2
suppression limit  = 5%
quality model      = ARX Loss Metric
~~

The sensitive attribute is:

~~text
diagnosis
~~

---

## Dataset

The synthetic healthcare dataset contains 600 records.

Analytical attributes:

~~text
zipcode
age
gender
nationality
diagnosis
admission_date
~~

A synthetic `patient_id` is generated only during source-data creation and is
removed before the dataset enters the anonymization process.

This prevents a stable record identifier from undermining equivalence-class
protection.

---

## Attribute Classification

### Direct Identifier

Removed before anonymization:

~~text
patient_id
~~

### Quasi-Identifiers

~~text
zipcode
age
gender
nationality
admission_date
~~

These attributes may not uniquely identify an individual in isolation but can
support linkage when combined with external demographic or encounter data.

### Sensitive Attribute

~~text
diagnosis
~~

Diagnosis is protected using both distinct l-diversity and t-closeness to
reduce attribute-disclosure risk.

---

## Generalization Hierarchies

### Zipcode

~~text
5-digit value
    |
    v
3-digit prefix
    |
    v
region
    |
    v
*
~~

### Age

~~text
exact age
    |
    v
5-year band
    |
    v
10-year band
    |
    v
broad age group
    |
    v
*
~~

### Gender

~~text
exact value
    |
    v
*
~~

### Nationality

~~text
country
    |
    v
subregion
    |
    v
region
    |
    v
*
~~

### Admission Date

~~text
exact date
    |
    v
month
    |
    v
quarter
    |
    v
year
    |
    v
*
~~

The hierarchy design allows ARX to progressively reduce specificity until the
configured privacy constraints are satisfied.

---

## Architecture

~~text
Synthetic Source Data
        |
        v
Remove Direct Identifier
        |
        v
Classify QIs + Sensitive Attribute
        |
        v
Apply Generalization Hierarchies
        |
        v
+----------------------------+
|            ARX             |
|                            |
| k = 5                      |
| distinct l = 3             |
| t = 0.2                    |
| suppression <= 5%          |
| Loss Metric optimization   |
+-------------+--------------+
              |
              v
Anonymized Dataset
              |
       +------+------+
       |             |
       v             v
 Risk Analysis   Utility Analysis
       |             |
       +------+------+
              |
              v
Compliance Assessment
~~

---

## k-Anonymity

The configuration requires:

~~text
k = 5
~~

Each released quasi-identifier equivalence class must therefore contain at
least five records after generalization and permitted suppression.

For an equivalence class of size five, the theoretical record-level linkage
probability is at most:

~~text
1 / 5 = 20%
~~

under the corresponding prosecutor-style equivalence-class assumption.

---

## l-Diversity

The configuration applies:

~~text
distinct l = 3
~~

to:

~~text
diagnosis
~~

This requires sufficient sensitive-value diversity within equivalence classes.

It addresses a weakness of pure k-anonymity in which all records in an
otherwise anonymous group could share the same diagnosis.

---

## t-Closeness

The configuration applies:

~~text
t = 0.2
~~

using ARX's equal-distance / Earth Mover's Distance model.

This constrains how far the diagnosis distribution inside an equivalence
class may diverge from the overall dataset distribution.

It provides additional protection against sensitive-attribute inference.

---

## Suppression

The transformation allows a maximum suppression rate of:

~~text
5%
~~

Suppression is treated as a bounded fallback rather than the primary privacy
mechanism.

The preferred solution relies on hierarchical generalization while retaining
as many records as practical.

---

## Risk Analysis

ARX sample-based risk analysis is captured in:

~~text
evidence/anonymization_metrics.txt
~~

The assessment records:

- highest sample re-identification risk
- average sample risk
- prosecutor risk
- journalist risk
- marketer risk
- suppression rate
- selected transformation
- ARX information-loss score

The configured k-anonymity threshold provides a maximum theoretical
equivalence-class linkage probability of 20%.

The measured ARX risk values provide a more detailed assessment under the
configured sample-based attacker models.

---

## Utility Analysis

Privacy protection is not evaluated independently of data utility.

ARX's Loss Metric is used to select the global optimum among transformations
satisfying:

~~text
k = 5
l = 3
t = 0.2
suppression <= 5%
~~

A neighboring transformation from the ARX solution lattice is also evaluated.

Evidence:

~~text
evidence/transformation_comparison.txt
~~

The comparison demonstrates the trade-off between:

~~text
More Generalization
       |
       +----> Lower identification risk
       |
       +----> Lower analytical precision
~~

and:

~~text
Less Generalization
       |
       +----> Greater analytical utility
       |
       +----> Higher privacy pressure
~~

---

## ARX Execution

The implementation uses the ARX Java API in a headless environment.

This makes the workflow reproducible without requiring an X11 or desktop
session.

Runtime requirements:

~~text
Java 21
ARX 3.9.2
Python 3
~~

The current ARX release used by this implementation requires Java 21 classfile
support.

---

## Core Implementation

### Dataset Generation

~~text
src/generate_patients.py
~~

Produces deterministic synthetic healthcare data using a fixed random seed.

### ARX Anonymization

~~text
src/HealthcareAnonymizer.java
~~

Configures:

- quasi-identifiers
- hierarchies
- sensitive attribute
- k-anonymity
- l-diversity
- t-closeness
- suppression
- Loss Metric optimization
- risk analysis
- anonymized export

### Transformation Comparison

~~text
src/CompareTransformations.java
~~

Inspects the ARX solution lattice and compares the global optimum against a
neighboring transformation.

---

## Evidence

~~text
evidence/
├── anonymization_metrics.txt
├── arx_configuration.txt
├── attribute_classification.md
├── hierarchy_design.md
└── transformation_comparison.txt
~~

These artifacts preserve the reasoning and technical evidence behind the
transformation.

---

## Compliance Assessment

The complete assessment is available at:

~~text
report.md
~~

It covers:

- quasi-identifier selection
- sensitive-attribute classification
- achieved privacy-model parameters
- residual re-identification risk
- utility loss
- GDPR anonymization vs pseudonymization
- Saudi PDPL anonymization considerations
- UAE PDPL considerations
- retention controls
- access controls
- re-identification testing recommendations

---

## GDPR Interpretation

GDPR Article 4(5) distinguishes pseudonymization from anonymization.

Removing direct identifiers and applying k-anonymity, l-diversity, and
t-closeness substantially reduces identification risk.

However, numerical privacy-model thresholds alone do not prove that no natural
person can be identified using all reasonably likely external information or
techniques.

The defensible conclusion is therefore:

> The output is technically anonymized against the evaluated linkage and
> attribute-disclosure models, but the ARX thresholds alone do not establish
> legal anonymity in every GDPR context.

A contextual re-identification assessment remains necessary before treating
the output as outside the scope of personal-data requirements.

---

## Saudi PDPL Interpretation

Saudi privacy requirements place strong emphasis on preventing direct and
indirect re-identification.

The transformation removes the direct patient identifier and significantly
reduces linkage opportunities through generalization and suppression.

However:

~~text
k = 5
l = 3
t = 0.2
~~

do not independently demonstrate permanent impossibility of re-identification
against every possible external data source.

The output should therefore continue to receive appropriate privacy controls
unless a broader contextual assessment supports a stronger anonymous-data
classification.

---

## Recommended Controls After Transformation

Even transformed datasets should use:

- documented secondary-use purposes
- least-privilege access
- minimum necessary retention
- dataset version control
- controlled research environments
- disclosure logging
- separation from identifiable source data
- prohibition of unauthorized linkage attempts
- periodic re-identification testing
- documented destruction schedules

---

## Reproducibility

The anonymization process is reproducible from:

~~text
data/patients.csv
hierarchies/
src/
~~

ARX configuration evidence is stored in:

~~text
evidence/arx_configuration.txt
~~

The output is:

~~text
output/patients_anonymized.csv
~~

The ARX binary itself is intentionally not stored in the repository.

---

## Repository Structure

~~text
healthcare-data-anonymization/
├── README.md
├── report.md
├── data/
│   └── patients.csv
├── output/
│   └── patients_anonymized.csv
├── hierarchies/
│   ├── age_hierarchy.csv
│   ├── admission_date_hierarchy.csv
│   ├── gender_hierarchy.csv
│   ├── nationality_hierarchy.csv
│   └── zipcode_hierarchy.csv
├── src/
│   ├── generate_patients.py
│   ├── HealthcareAnonymizer.java
│   └── CompareTransformations.java
└── evidence/
    ├── anonymization_metrics.txt
    ├── arx_configuration.txt
    ├── attribute_classification.md
    ├── hierarchy_design.md
    └── transformation_comparison.txt
~~

The source dataset containing the synthetic direct identifier is intentionally
excluded from the recruiter-facing repository.

---

## Skills Demonstrated

- ARX Data Anonymization Tool
- k-anonymity
- l-diversity
- t-closeness
- Privacy Enhancing Technologies
- re-identification risk analysis
- quasi-identifier modeling
- sensitive-attribute modeling
- hierarchical generalization
- suppression analysis
- privacy-utility optimization
- Java API integration
- healthcare data privacy
- GDPR privacy engineering
- GCC privacy governance
- reproducible privacy analysis

---

## Production Improvements

A production implementation should additionally include:

- automated re-identification testing
- population-based risk models
- formal attacker-model documentation
- statistical utility validation
- downstream analytical-quality testing
- dataset release approval workflows
- immutable configuration records
- signed transformation evidence
- privacy regression testing
- external-data linkage simulations
- automated retention enforcement
- controlled clean-room environments
- recurring anonymization-effectiveness reassessment

---

## Final Outcome

The implementation demonstrates an end-to-end privacy-preserving data release
workflow:

~~text
Source Dataset
      |
      v
Identifier Removal
      |
      v
QI / Sensitive Attribute Modeling
      |
      v
Hierarchy Design
      |
      v
ARX Privacy Constraints
      |
      v
Transformation Search
      |
      +----> Risk Analysis
      |
      +----> Utility Analysis
      |
      v
Anonymized Output
      |
      v
Compliance Assessment
~~

The result demonstrates how formal privacy models can be combined with
measurable re-identification risk and information-loss analysis to support
defensible secondary use of sensitive healthcare data.
