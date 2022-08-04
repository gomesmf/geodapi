from abc import ABC, abstractmethod
from typing import Callable

class DBAccountsInterface(ABC):
    @abstractmethod
    def create(self, ) -> int:
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
ERRMSG_INVALID_PASSWORD = "Invalid password"
ERRMSG_INVALID_NAME = "Invalid name"
ERRMSG_INVALID_EMAIL = "Invalid email"

def _validate_password(p: str) -> bool:
    return len(p) >= MIN_LEN_PASSWORD

def _validate_name(name: str) -> bool:
    return len(name) > 0

def _validate_email(email: str) -> bool:
    return "@" in email

def create_account_interactor(dba: DBAccountsInterface, ph: Callable[[str], str], ucin: CreateAccountUCI) -> CreateAccountUCO:
    if not _validate_password(ucin.password):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_PASSWORD)

    if not _validate_name(ucin.name):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_NAME)

    if not _validate_email(ucin.email):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_EMAIL)

    password_hashed = ph(ucin.password)

    id = dba.create(ucin.type, ucin.email, ucin.name, password_hashed)

    ucout = CreateAccountUCO(id=id)

    return ucout
