from enum import Enum

class AccountType(Enum):
    SELLER = "seller"
    BUYER = "buyer"
    DELIVERYGUY = "deliveryguy"

class Account:
    def __init__(self, id: int = None, type: str = None, name: str = None, email: str = None, password_hashed: str = None) -> None:
        self.id = id
        self.type = type
        self.name = name
        self.email = email
        self.password_hashed = password_hashed
