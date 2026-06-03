"""
Random Australian profile generator for test/demo purposes.
All data is entirely fictional and should not be used for any real purpose.
"""

from __future__ import annotations

import random
import secrets
import string
from datetime import date, timedelta
from typing import TypedDict

from faker import Faker

fake = Faker("en_AU")


class AustralianProfile(TypedDict):
    first_name: str
    last_name: str
    middle_name: str
    date_of_birth: str
    email: str
    phone_number: str
    address_line_1: str
    suburb: str
    state: str
    postcode: str
    country: str
    passport_number: str
    drivers_licence: str
    medicare_number: str
    tax_file_number: str


def _fmt_date(d: date) -> str:
    return f"{d.day:02d}/{d.month:02d}/{d.year}"


def _random_dob() -> date:
    return fake.date_of_birth(minimum_age=18, maximum_age=75)


def _random_phone() -> str:
    return "04" + "".join(str(random.randint(0, 9)) for _ in range(8))


def _random_email(first: str, last: str) -> str:
    suffix = secrets.token_hex(4)
    return f"no_mfa_{first.lower()}_{last.lower()}_{suffix}@yopmail.com"


_STATE_POSTCODE_RANGES: dict[str, tuple[int, int]] = {
    "NSW": (2000, 2999),
    "VIC": (3000, 3999),
    "QLD": (4000, 4999),
    "SA": (5000, 5999),
    "WA": (6000, 6999),
    "TAS": (7000, 7999),
}
_STATES = list(_STATE_POSTCODE_RANGES.keys())

_SUBURBS: list[str] = [
    "Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide",
    "Hobart", "Gold Coast", "Newcastle", "Wollongong", "Geelong",
    "Townsville", "Cairns", "Toowoomba", "Launceston", "Bendigo",
    "Albury", "Ballarat", "Mandurah", "Bundaberg", "Rockhampton",
    "Mackay", "Coffs Harbour", "Tamworth", "Gladstone", "Lismore",
    "Bathurst", "Southport", "Broadbeach", "Moorabbin", "Coburg",
    "Footscray", "Fitzroy", "Collingwood", "Brunswick", "Preston",
    "Ringwood", "Frankston", "Dandenong", "Berwick", "Cranbourne",
    "Traralgon", "Shepparton", "Warrnambool", "Echuca", "Wangaratta",
    "Bairnsdale", "Sale", "Wonthaggi", "Seymour", "Gisborne",
    "Daylesford", "Lilydale", "Belgrave", "Pakenham", "Beaconsfield",
    "Drouin", "Warragul", "Morwell", "Armidale", "Dubbo",
]


def _random_state_and_postcode() -> tuple[str, str]:
    state = random.choice(_STATES)
    lo, hi = _STATE_POSTCODE_RANGES[state]
    return state, str(random.randint(lo, hi))


def _random_address() -> str:
    number = random.randint(1, 999)
    street = fake.street_name()
    return f"{number} {street}"


def _random_passport() -> str:
    """Australian passport: 2 uppercase letters + 7 digits."""
    letters = "".join(random.choices(string.ascii_uppercase, k=2))
    digits = "".join(str(random.randint(0, 9)) for _ in range(7))
    return f"{letters}{digits}"


# Licence format per state (simplified realistic formats)
_LICENCE_FORMATS: dict[str, str] = {
    "NSW": "########",     # 8 digits
    "VIC": "#########",    # 9 digits
    "QLD": "########",     # 8 digits
    "SA":  "SXXXXXXX",     # S + 7 chars
    "WA":  "#######",      # 7 digits
    "TAS": "#######",      # 7 digits
}


def _random_drivers_licence(state: str) -> str:
    fmt = _LICENCE_FORMATS.get(state, "########")
    result = []
    for ch in fmt:
        if ch == "#":
            result.append(str(random.randint(0, 9)))
        elif ch == "S":
            result.append("S")
        elif ch == "X":
            result.append(random.choice(string.ascii_uppercase + string.digits))
        else:
            result.append(ch)
    return "".join(result)


def _random_medicare() -> str:
    """Medicare: 10 digits formatted as XXXX XXXXX X."""
    # First digit is 2–6 for individuals
    first = str(random.randint(2, 6))
    rest = "".join(str(random.randint(0, 9)) for _ in range(9))
    number = first + rest
    return f"{number[:4]} {number[4:9]} {number[9]}"


def _random_tfn() -> str:
    """Tax File Number: 8 or 9 digits formatted as XXX XXX XXX."""
    digits = "".join(str(random.randint(0, 9)) for _ in range(9))
    return f"{digits[:3]} {digits[3:6]} {digits[6:]}"


def generate_profile() -> AustralianProfile:
    first = fake.first_name()
    last = fake.last_name()
    middle = fake.first_name() if random.random() > 0.5 else ""
    state, postcode = _random_state_and_postcode()
    suburb = random.choice(_SUBURBS)

    return AustralianProfile(
        first_name=first,
        last_name=last,
        middle_name=middle,
        date_of_birth=_fmt_date(_random_dob()),
        email=_random_email(first, last),
        phone_number=_random_phone(),
        address_line_1=_random_address(),
        suburb=suburb,
        state=state,
        postcode=postcode,
        country="Australia",
        passport_number=_random_passport(),
        drivers_licence=_random_drivers_licence(state),
        medicare_number=_random_medicare(),
        tax_file_number=_random_tfn(),
    )
