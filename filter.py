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
    "united states"
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
    if not location:
        return True

    locations = {
        item.strip().casefold()
        for item in location.split(",")
    }

    return bool(locations & TARGET_LOCATIONS)