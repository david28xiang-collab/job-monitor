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

# These patterns intentionally use word boundaries so titles such as
# "International Analyst" are not mistaken for internships.
EXCLUDED_ROLE_PATTERNS = (
    r"\bintern(?:ship|ships|s)?\b",
    r"\bsummer analyst\b",
    r"\badministrative\b",
    r"\bexecutive assistant\b",
    r"\boffice (?:assistant|coordinator|manager)\b",
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


def is_target_role(title):
    """Return False for internship and administrative job titles."""
    if not isinstance(title, str) or not title.strip():
        return True

    normalized_title = re.sub(r"\s+", " ", title.casefold()).strip()
    return not any(
        re.search(pattern, normalized_title)
        for pattern in EXCLUDED_ROLE_PATTERNS
    )
