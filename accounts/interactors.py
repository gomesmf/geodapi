from abc import ABC, abstractmethod
from typing import Callable

from accounts.entities import Account, AccountType

class DBAccountsInterface(ABC):
    @abstractmethod
    def create(self, a: Account) -> int:
        pass

class CreateAccountUCI:
    def __init__(self, type: str, name: str, email: str, password: str) -> None:
        self.type = type
        self.name = name
        self.email = email
        self.password = password

class CreateAccountUCO:
    def __init__(self, id: int = None, errmsg: str = None) -> None:
        self.id = id
        self.errmsg = errmsg

MIN_LEN_PASSWORD = 4
ERRMSG_INVALID_ACCTYPE = "Invalid account type"
ERRMSG_INVALID_PASSWORD = "Invalid password"
ERRMSG_INVALID_NAME = "Invalid name"
ERRMSG_INVALID_EMAIL = "Invalid email"

def _validate_acctype(t: str) -> bool:
    try:
        AccountType(t)
    except ValueError:
        return False
    return True

def _validate_password(p: str) -> bool:
    return len(p) >= MIN_LEN_PASSWORD

def _validate_name(name: str) -> bool:
    return len(name) > 0

def _validate_email(email: str) -> bool:
    return "@" in email

def _validate_ucin(ucin: CreateAccountUCI) -> CreateAccountUCO:
    if not _validate_acctype(ucin.type):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_ACCTYPE)

    if not _validate_password(ucin.password):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_PASSWORD)

    if not _validate_name(ucin.name):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_NAME)

    if not _validate_email(ucin.email):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_EMAIL)

def create_account_interactor(dba: DBAccountsInterface, ph: Callable[[str], str], ucin: CreateAccountUCI) -> CreateAccountUCO:
    ucout = _validate_ucin(ucin)

    if ucout:
        return ucout

    password_hashed = ph(ucin.password)

    a = Account(type=ucin.type, name=ucin.name, email=ucin.email, password_hashed=password_hashed)

    id = dba.create(a)

    ucout = CreateAccountUCO(id=id)

    return ucout
