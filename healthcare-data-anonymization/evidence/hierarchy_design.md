# Generalization Hierarchy Design

## Zipcode

Hierarchy:

~~text
5-digit zipcode
    |
    v
3-digit prefix
    |
    v
broader region
    |
    v
*
~~

Rationale:

Exact postal codes can sharply reduce the candidate population when combined
with age, gender, and nationality.

The hierarchy therefore preserves local geographic utility at lower levels
while allowing progressively broader geographic masking where necessary.

## Age

Hierarchy:

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

Rationale:

Age is analytically useful in healthcare research, so the hierarchy uses
progressive interval widening rather than immediate suppression.

Five-year intervals preserve more utility, while decade and broad-age bands
provide stronger protection when equivalence classes remain too small.

## Nationality

Hierarchy:

~~text
country
    |
    v
GCC / Non-GCC
    |
    v
regional grouping
    |
    v
*
~~

Rationale:

Nationality can materially contribute to uniqueness when combined with other
demographic fields.

The first level preserves policy-relevant GCC distinctions while removing
country-level specificity.

The second level provides broader geographic grouping where stronger
generalization is required.

## Admission Date

Hierarchy:

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

Rationale:

Exact healthcare encounter dates can be linked with external information.

Generalizing dates by month, quarter, or year reduces linkage risk while still
retaining useful temporal information for analysis.

## Utility Trade-Off

Increasing generalization reduces re-identification risk but also removes
analytical precision.

The anonymization search should therefore prefer the lowest transformation
levels that satisfy:

- k = 5
- distinct l = 3
- t = 0.2
- suppression <= 5%

The preferred transformation should minimize information loss while satisfying
all configured privacy constraints.
