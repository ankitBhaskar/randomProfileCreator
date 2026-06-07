"""
Employee data generation for bulk CSV download.
Generates randomised, realistic Australian employee records.
"""

from __future__ import annotations

import random
import secrets
from datetime import date, timedelta
from typing import TypedDict

from faker import Faker

fake = Faker("en_AU")

CSV_HEADERS = [
    "worker_reference_id", "payroll_id", "family_name", "first_name",
    "middle_name", "date_of_birth", "email", "phone_number",
    "address_line_1", "address_line_2", "address_line_3",
    "suburb", "postcode", "state", "country",
    "employment_start_date", "employment_end_date",
]


class EmployeeRecord(TypedDict):
    worker_reference_id: str
    payroll_id: str
    family_name: str
    first_name: str
    middle_name: str
    date_of_birth: str
    email: str
    phone_number: str
    address_line_1: str
    address_line_2: str
    address_line_3: str
    suburb: str
    postcode: str
    state: str
    country: str
    employment_start_date: str
    employment_end_date: str


def _fmt(d: date) -> str:
    return f"{d.day}/{d.month}/{d.year}"


def _random_payroll_id() -> str:
    return "P" + str(random.randint(1_000_000, 9_999_999))


def _random_dob() -> date:
    return fake.date_of_birth(minimum_age=18, maximum_age=60)


def _random_employment_start() -> date:
    earliest = date(2025, 7, 1)
    today = date.today()
    if today <= earliest:
        return earliest
    return earliest + timedelta(days=random.randint(0, (today - earliest).days))


def _random_phone() -> str:
    return "04" + "".join(str(random.randint(0, 9)) for _ in range(8))


def _random_email(first: str, last: str) -> str:
    suffix = secrets.token_hex(4)
    return f"no_mfa_{first.lower()}_{last.lower()}_{suffix}@yopmail.com"


_STATE_POSTCODE_RANGES: dict[str, tuple[int, int]] = {
    "NSW": (2000, 2999),
    "VIC": (3000, 3999),
    "QLD": (4000, 4999),
    "SA":  (5000, 5999),
    "WA":  (6000, 6999),
    "TAS": (7000, 7999),
}
_STATES = list(_STATE_POSTCODE_RANGES.keys())

_SUBURBS = [
    "MELBOURNE", "SYDNEY", "BRISBANE", "PERTH", "ADELAIDE",
    "HOBART", "GOLD COAST", "NEWCASTLE", "WOLLONGONG", "GEELONG",
    "TOWNSVILLE", "CAIRNS", "TOOWOOMBA", "LAUNCESTON", "BENDIGO",
    "ALBURY", "BALLARAT", "MANDURAH", "BUNDABERG", "ROCKHAMPTON",
    "MACKAY", "COFFS HARBOUR", "TAMWORTH", "GLADSTONE", "LISMORE",
    "BATHURST", "SOUTHPORT", "BROADBEACH", "MOORABBIN", "COBURG",
    "FOOTSCRAY", "FITZROY", "COLLINGWOOD", "BRUNSWICK", "PRESTON",
    "RINGWOOD", "FRANKSTON", "DANDENONG", "BERWICK", "CRANBOURNE",
    "TRARALGON", "SHEPPARTON", "WARRNAMBOOL", "ECHUCA", "WANGARATTA",
    "BAIRNSDALE", "SALE", "WONTHAGGI", "SEYMOUR", "GISBORNE",
    "DAYLESFORD", "LILYDALE", "BELGRAVE", "PAKENHAM", "BEACONSFIELD",
    "DROUIN", "WARRAGUL", "MORWELL", "ARMIDALE", "DUBBO",
]


def _random_state_postcode() -> tuple[str, str]:
    state = random.choice(_STATES)
    lo, hi = _STATE_POSTCODE_RANGES[state]
    return state, str(random.randint(lo, hi))


def random_employee() -> EmployeeRecord:
    first = fake.first_name()
    last = fake.last_name()
    state, postcode = _random_state_postcode()
    return EmployeeRecord(
        worker_reference_id="",
        payroll_id=_random_payroll_id(),
        family_name=last,
        first_name=first,
        middle_name="",
        date_of_birth=_fmt(_random_dob()),
        email=_random_email(first, last),
        phone_number=_random_phone(),
        address_line_1=str(random.randint(1, 999)) + " " + fake.street_name().upper(),
        address_line_2="",
        address_line_3="",
        suburb=random.choice(_SUBURBS),
        postcode=postcode,
        state=state,
        country="Australia",
        employment_start_date=_fmt(_random_employment_start()),
        employment_end_date="",
    )
