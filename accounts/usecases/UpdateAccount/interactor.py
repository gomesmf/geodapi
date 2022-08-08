from typing import Callable
from accounts.interfaces.data import DBAccountsInterface
from accounts.entities import (
    validate_email,
    validate_name,
    validate_password,
    validate_username
)
from accounts.usecases.common import (
    ERRMSG_ACCOUNT_NOT_FOUND,
    ERRMSG_CANNOT_UPDATE_ACCOUNT,
    ERRMSG_EMAIL_EXISTS,
    ERRMSG_INVALID_EMAIL,
    ERRMSG_INVALID_NAME,
    ERRMSG_INVALID_PASSWORD,
    ERRMSG_INVALID_USERNAME,
    ERRMSG_TWO_PASSWD_MUST_MATCH,
    ERRMSG_USERNAME_EXISTS
)

class UpdateAccountUCI:
    def __init__(self, account_id: int, email: str = None, name: str = None, username: str = None, password: str = None, password_again: str = None) -> None:
        self.account_id = account_id
        self.email = email
        self.name = name
        self.username = username
        self.password = password
        self.password_again = password_again

class UpdateAccountUCO:
    def __init__(self, errmsg: str = None) -> None:
        self.errmsg = errmsg

def update_account_interactor(dba: DBAccountsInterface, ph: Callable[[str], str], ucin: UpdateAccountUCI) -> UpdateAccountUCO:
    if not dba.account_id_exists(ucin.account_id):
        return UpdateAccountUCO(errmsg=ERRMSG_ACCOUNT_NOT_FOUND)

    if ucin.email != None:
        if dba.email_exists(ucin.email):
            return UpdateAccountUCO(errmsg=ERRMSG_EMAIL_EXISTS)

        if not validate_email(ucin.email):
            return UpdateAccountUCO(errmsg=ERRMSG_INVALID_EMAIL)

    if ucin.username != None:
        if dba.username_exists(ucin.username):
            return UpdateAccountUCO(errmsg=ERRMSG_USERNAME_EXISTS)

        if not validate_username(ucin.username):
            return UpdateAccountUCO(errmsg=ERRMSG_INVALID_USERNAME)

    if ucin.name != None and not validate_name(ucin.name):
        return UpdateAccountUCO(errmsg=ERRMSG_INVALID_NAME)

    password_hashed = None
    if ucin.password != None:
        if ucin.password != ucin.password_again:
            return UpdateAccountUCO(errmsg=ERRMSG_TWO_PASSWD_MUST_MATCH)

        if not validate_password(ucin.password):
            return UpdateAccountUCO(errmsg=ERRMSG_INVALID_PASSWORD)

        password_hashed = ph(ucin.password)

    if not dba.update(account_id=ucin.account_id, email=ucin.email, name=ucin.name, username=ucin.username, password_hashed=password_hashed):
        return UpdateAccountUCO(errmsg=ERRMSG_CANNOT_UPDATE_ACCOUNT)

    return UpdateAccountUCO()
