import re


US_LOCATIONS = {
    "greenwich",
    "houston",
    "miami",
    "new york",
    "chicago",
    "dallas",
    "boston",
    "san francisco",
    "los angeles",
    "washington",
    "united states",
    "us",
}

CHINA_LOCATIONS = {
    "beijing",
    "shanghai",
    "shenzhen",
    "guangzhou",
    "hangzhou",
    "chengdu",
    "china"
}

HONG_KONG_LOCATIONS = {
    "hong kong",
}

TARGET_LOCATIONS = (
    US_LOCATIONS
    | CHINA_LOCATIONS
    | HONG_KONG_LOCATIONS
)


def is_target_location(location):
    if not isinstance(location, str) or not location.strip():
        return True

    # Normalize formats such as "US-MA-Boston", "Boston, MA", and
    # pipe-separated iCIMS location lists into searchable words.
    normalized_location = re.sub(
        r"[^a-z0-9]+",
        " ",
        location.casefold(),
    ).strip()
    padded_location = f" {normalized_location} "

    return any(
        f" {target} " in padded_location
        for target in TARGET_LOCATIONS
    )
