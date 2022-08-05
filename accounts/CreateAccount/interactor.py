from abc import ABC, abstractmethod
from typing import Callable

from accounts.entities import (
    Account,
    validate_acctype,
    validate_name,
    validate_password,
    validate_email
)

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

ERRMSG_INVALID_ACCTYPE = "Invalid account type"
ERRMSG_INVALID_PASSWORD = "Invalid password"
ERRMSG_INVALID_NAME = "Invalid name"
ERRMSG_INVALID_EMAIL = "Invalid email"

def _validate_ucin(ucin: CreateAccountUCI) -> CreateAccountUCO:
    if not validate_acctype(ucin.type):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_ACCTYPE)

    if not validate_password(ucin.password):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_PASSWORD)

    if not validate_name(ucin.name):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_NAME)

    if not validate_email(ucin.email):
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