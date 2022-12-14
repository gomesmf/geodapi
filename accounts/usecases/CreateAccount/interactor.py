from typing import Callable
from accounts.interfaces.data import DBAccountsInterface

from accounts.entities import (
    MIN_LEN_PASSWORD,
    MIN_LEN_USERNAME,
    Account,
    validate_acctype,
    validate_name,
    validate_password,
    validate_email,
    validate_username
)
from accounts.usecases.common import (
    ERRMSG_CANNOT_CREATE_ACCOUNT,
    ERRMSG_EMAIL_EXISTS,
    ERRMSG_INVALID_ACCTYPE,
    ERRMSG_INVALID_EMAIL,
    ERRMSG_INVALID_NAME,
    ERRMSG_INVALID_PASSWORD,
    ERRMSG_INVALID_USERNAME,
    ERRMSG_USERNAME_EXISTS
)

class CreateAccountUCI:
    def __init__(self, type: str, name: str, email: str, password: str, username: str) -> None:
        self.type = type
        self.name = name
        self.email = email
        self.password = password
        self.username = username

class CreateAccountUCO:
    def __init__(self, id: int = None, errmsg: str = None) -> None:
        self.id = id
        self.errmsg = errmsg

# ERRMSG_INVALID_ACCTYPE = "Invalid account type"
# ERRMSG_INVALID_PASSWORD = f"Invalid password: must have at least {MIN_LEN_PASSWORD} characters"
# ERRMSG_INVALID_NAME = "Invalid name: cannot be empty"
# ERRMSG_INVALID_USERNAME = f"Invalid username: must have at least {MIN_LEN_USERNAME} characters"
# ERRMSG_INVALID_EMAIL = "Invalid email"
# ERRMSG_EMAIL_EXISTS = "Email already used by another account"
# ERRMSG_USERNAME_EXISTS = "Username already used by another account"
# ERRMSG_CANNOT_CREATE_ACCOUNT = "Account cannot be created in the database"

def _validate_ucin(ucin: CreateAccountUCI) -> CreateAccountUCO:
    if not validate_acctype(ucin.type):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_ACCTYPE)

    if not validate_password(ucin.password):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_PASSWORD)

    if not validate_name(ucin.name):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_NAME)

    if not validate_username(ucin.username):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_USERNAME)

    if not validate_email(ucin.email):
        return CreateAccountUCO(errmsg=ERRMSG_INVALID_EMAIL)

def create_account_interactor(dba: DBAccountsInterface, ph: Callable[[str], str], ucin: CreateAccountUCI) -> CreateAccountUCO:
    ucout = _validate_ucin(ucin)

    if ucout:
        return ucout

    if dba.email_exists(ucin.email):
        return CreateAccountUCO(errmsg=ERRMSG_EMAIL_EXISTS)

    if dba.username_exists(ucin.username):
        return CreateAccountUCO(errmsg=ERRMSG_USERNAME_EXISTS)

    password_hashed = ph(ucin.password)

    a = Account(type=ucin.type, name=ucin.name, email=ucin.email, username=ucin.username, password_hashed=password_hashed)

    if not dba.create(a):
        return CreateAccountUCO(errmsg=ERRMSG_CANNOT_CREATE_ACCOUNT)

    ucout = CreateAccountUCO(id=a.id)

    return ucout
