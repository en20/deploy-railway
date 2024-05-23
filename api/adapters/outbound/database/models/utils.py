import uuid
from datetime import date


def id_generator() -> str:
    return str(uuid.uuid4())[:16]


def format_date_string(date: date):
    return date.strftime("%Y-%m-%d %H:%M:%S")
