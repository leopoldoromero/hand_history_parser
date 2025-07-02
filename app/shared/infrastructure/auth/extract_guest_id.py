from fastapi import Header
from typing import Optional


def extract_guest_id(x_guest_id: Optional[str] = Header(None)):
    return x_guest_id
