from enum import Enum

MIN_LEN_PASSWORD = 4

class AccountType(Enum):
    SELLER = "SELLER"
    BUYER = "BUYER"
    DELIVERYGUY = "DELIVERYGUY"

class Account:
    def __init__(self, id: int = None, type: str = None, name: str = None, email: str = None, password_hashed: str = None) -> None:
        self.id = id
        self.type = type
        self.name = name
        self.email = email
        self.password_hashed = password_hashed

def validate_acctype(t: str) -> bool:
    try:
        AccountType(t)
    except ValueError:
        return False
    return True

def validate_password(p: str) -> bool:
    return len(p) >= MIN_LEN_PASSWORD

def validate_name(name: str) -> bool:
    return len(name) > 0

def validate_email(email: str) -> bool:
    return "@" in email
