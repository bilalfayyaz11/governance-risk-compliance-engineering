VALID_RATINGS = ("Low", "Moderate", "High")
SEVERITY = {rating: index for index, rating in enumerate(VALID_RATINGS)}


def high_water_mark(ratings: list[str]) -> str:
    """
    Return the highest FIPS 199 impact level in a collection
    of Low, Moderate, and High ratings.
    """
    if not ratings:
        raise ValueError("At least one impact rating is required.")

    invalid = [rating for rating in ratings if rating not in SEVERITY]
    if invalid:
        raise ValueError(f"Invalid FIPS 199 impact rating(s): {invalid}")

    return max(ratings, key=SEVERITY.get)


# Final ratings after operational-context review
information_types = {
    "D.14.1 Access to Care": {
        "Confidentiality": "Low",
        "Integrity": "Moderate",
        "Availability": "Moderate",
    },
    "C.2.8.9 Personal Identity and Authentication": {
        "Confidentiality": "Moderate",
        "Integrity": "Moderate",
        "Availability": "Moderate",
    },
}

objectives = ("Confidentiality", "Integrity", "Availability")

system_category = {
    objective: high_water_mark([
        ratings[objective]
        for ratings in information_types.values()
    ])
    for objective in objectives
}

overall_impact = high_water_mark(list(system_category.values()))

print("FIPS 199 SYSTEM SECURITY CATEGORIZATION")
print("---------------------------------------")

for information_type, ratings in information_types.items():
    print(f"\n{information_type}")
    for objective in objectives:
        print(f"  {objective}: {ratings[objective]}")

print("\nHIGH-WATER MARK")
print("----------------")
for objective in objectives:
    print(f"Overall {objective}: {system_category[objective]}")

print(f"\nOverall System Impact: {overall_impact}")
print(
    "SC = {(confidentiality, %s), (integrity, %s), (availability, %s)}"
    % (
        system_category["Confidentiality"].upper(),
        system_category["Integrity"].upper(),
        system_category["Availability"].upper(),
    )
)
