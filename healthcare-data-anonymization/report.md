# Healthcare Data Anonymization Assessment

## Executive Summary

A synthetic healthcare dataset containing 600 records was processed using
ARX Data Anonymization Tool.

The implemented privacy model combines:

- k-anonymity: k = 5
- distinct l-diversity: l = 3
- t-closeness: t = 0.2
- maximum suppression: 5%

The selected transformation was:

`[1, 4, 0, 3, 3]`

ARX reported the following residual sample-based risks:

- Highest sample re-identification risk: 1.5625%
- Average sample re-identification risk: 1.3333333333333335%
- Prosecutor risk: 1.5625%
- Journalist risk: 1.5625%
- Marketer risk: 1.3333333333333335%

Observed suppression:

- 0.0%

The ARX Loss Metric for the selected optimum was:

`0.5747544504920252`

## Dataset Design

The original synthetic dataset included a unique `patient_id`.

That direct identifier was removed before anonymization.

The anonymization input contains:

- zipcode
- age
- gender
- nationality
- diagnosis
- admission_date

## Attribute Classification

### Removed Identifier

`patient_id`

This field uniquely identifies an individual record and was therefore removed
before anonymization rather than generalized.

### Quasi-Identifiers

The following attributes were treated as quasi-identifiers:

- zipcode
- age
- gender
- nationality
- admission_date

These attributes may not uniquely identify an individual alone, but their
combination can support linkage attacks using external information.

### Sensitive Attribute

`diagnosis`

Diagnosis contains health information and was protected using distinct
l-diversity and t-closeness.

## Generalization Design

### Zipcode

Generalization path:

5-digit value -> 3-digit prefix -> region -> suppressed

### Age

Generalization path:

exact age -> 5-year band -> decade -> broad age band -> suppressed

### Gender

Generalization path:

exact value -> suppressed

### Nationality

Generalization path:

country -> subregion -> region -> suppressed

### Admission Date

Generalization path:

exact date -> month -> quarter -> year -> suppressed

## Privacy Models

### k-Anonymity

The selected value is:

k = 5

Each released quasi-identifier equivalence class therefore contains at least
five records after ARX's configured transformation and suppression behavior.

The theoretical maximum prosecutor-style record linkage probability implied
by a class size of five is 1/5, or 20%, before considering stronger protections
from l-diversity and t-closeness.

### Distinct l-Diversity

The selected value is:

l = 3

Each relevant equivalence class must contain at least three distinct diagnosis
values.

This reduces attribute-disclosure risk that would remain if every member of a
k-anonymous group shared the same diagnosis.

### t-Closeness

The selected threshold is:

t = 0.2

The diagnosis distribution within equivalence classes is constrained relative
to the overall dataset distribution.

This further reduces sensitive-attribute inference risk.

## Risk Analysis

ARX measured:

| Risk Model | Result |
|---|---:|
| Highest sample risk | 1.5625% |
| Average sample risk | 1.3333333333333335% |
| Prosecutor | 1.5625% |
| Journalist | 1.5625% |
| Marketer | 1.3333333333333335% |

The configured k-anonymity threshold implies that the highest equivalence-class
risk should not exceed 20%.

These values describe the modeled dataset and ARX's configured attacker/risk
assumptions. They do not prove that every conceivable real-world
re-identification method is impossible.

## Utility Analysis

ARX selected the global optimum using its Loss Metric.

Optimal transformation:

`[1, 4, 0, 3, 3]`

Loss score:

`0.5747544504920252`

Suppression:

`0.0%`

A separate neighboring transformation was also evaluated to demonstrate the
privacy-utility trade-off.

The full comparison is retained in:

`evidence/transformation_comparison.txt`

The global optimum is treated as the preferred/Pareto-relevant operating point
because it satisfies the configured privacy constraints while ARX minimizes
information loss under the selected quality model.

## Transformation Comparison

~~text
Transformation comparison
=========================

OPTIMAL NODE
transformation = [1, 4, 0, 3, 3]
total generalization level = 11
lowest loss score = 0.5747544504920252
highest loss score = 0.5747544504920252
suppression rate = 0.0%
highest sample risk = 1.5625%
prosecutor risk = 1.5625%
journalist risk = 1.5625%
marketer risk = 1.3333333333333335%

COMPARISON NODE
transformation = [1, 4, 1, 3, 3]
total generalization level = 12
lowest loss score = 0.8089178468044493
highest loss score = 0.8089178468044493
suppression rate = 0.0%
highest sample risk = 0.6993006993006993%
prosecutor risk = 0.6993006993006993%
journalist risk = 0.6993006993006993%
marketer risk = 0.6666666666666667%

Interpretation
--------------
Lower ARX loss scores indicate better retained utility.
The global optimum is ARX's selected minimum-loss solution under the configured constraints.

~~

## GDPR Assessment

GDPR Article 4(5) defines pseudonymisation as processing that prevents data
from being attributed to a specific person without additional information,
where that additional information is separately protected.

GDPR Recital 26 distinguishes this from anonymous information. Information
that cannot reasonably identify a natural person falls outside the personal
data concept, while data that can still be attributed to an individual using
additional information remains personal data.

The removal of direct identifiers and application of k-anonymity,
l-diversity, and t-closeness materially lowers re-identification risk.

However, satisfying these numerical privacy models alone does not demonstrate
that identification is impossible using every reasonably likely external data
source or future technique.

Accordingly, the defensible conclusion is:

**The output is technically anonymized against the tested linkage and
attribute-disclosure models, but this assessment does not by itself establish
that the dataset is legally anonymous for every GDPR context.**

Until a contextual re-identification assessment demonstrates that individuals
are no longer reasonably identifiable, the dataset should continue to receive
strong data-protection controls.

## Saudi PDPL Assessment

Saudi PDPL implementing rules distinguish pseudonymisation from anonymisation.

Anonymisation requires removal of direct and indirect identifiers in a way
that permanently prevents identification of the data subject.

The implementing regulation also requires controllers to evaluate
re-identification risk, maintain suitable safeguards, and reassess the
effectiveness of anonymisation techniques.

This implementation removes the direct patient identifier and substantially
reduces linkage risk through generalization and suppression.

Nevertheless, k=5, l=3, and t=0.2 do not mathematically demonstrate permanent
impossibility of re-identification against every possible external dataset.

Therefore the conservative classification is:

**The dataset demonstrates strong technical de-identification/anonymization
controls, but should not be declared permanently anonymous under Saudi PDPL
solely from these ARX thresholds.**

## UAE PDPL Assessment

The UAE PDPL distinguishes pseudonymisation from anonymisation and describes
anonymisation in terms of preventing the data from being attributed to or
used to identify a natural person.

The ARX transformation significantly reduces identification risk, but a legal
anonymous-data conclusion requires a broader contextual determination that
identification is no longer realistically possible.

## Retention and Access Recommendations

Even after transformation, the released dataset should use:

- documented secondary-use purposes
- minimum necessary retention
- controlled research access
- least-privilege authorization
- dataset versioning
- disclosure logging
- periodic re-identification testing
- prohibition on unauthorized linkage attempts
- separation from source patient records
- documented destruction schedules

The original identifiable dataset and any linkage keys should remain subject
to stronger access controls than the transformed output.

## Auditability

The following artifacts preserve the technical decision trail:

- `data/patients.csv`
- `output/patients_anonymized.csv`
- `hierarchies/zipcode_hierarchy.csv`
- `hierarchies/age_hierarchy.csv`
- `hierarchies/gender_hierarchy.csv`
- `hierarchies/nationality_hierarchy.csv`
- `hierarchies/admission_date_hierarchy.csv`
- `evidence/attribute_classification.md`
- `evidence/hierarchy_design.md`
- `evidence/arx_configuration.txt`
- `evidence/anonymization_metrics.txt`
- `evidence/transformation_comparison.txt`
- `src/HealthcareAnonymizer.java`
- `src/CompareTransformations.java`

## Conclusion

The healthcare dataset was transformed with a layered privacy model combining
k-anonymity, distinct l-diversity, t-closeness, hierarchical generalization,
and bounded suppression.

The implementation demonstrates a measurable reduction in linkage and
attribute-disclosure risk while explicitly considering information loss.

The resulting dataset is suitable as evidence of a defensible technical
de-identification workflow, while the legal classification remains dependent
on contextual re-identification feasibility rather than privacy-model
thresholds alone.
