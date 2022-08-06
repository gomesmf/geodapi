from typing import Callable
from accounts.data import DBAccountsInterface
from accounts.entities import validate_name, validate_password

class UpdateAccountUCI:
    def __init__(self, account_id: int, email: str = None, name: str = None, password: str = None, password_again: str = None) -> None:
        self.account_id = account_id
        self.email = email
        self.name = name
        self.password = password
        self.password_again = password_again

class UpdateAccountUCO:
    def __init__(self, errmsg: str = None) -> None:
        self.errmsg = errmsg

ERRMSG_ACCOUNT_NOT_FOUND = "Account does not exists"
ERRMSG_EMAIL_ALREADY_EXISTS = "Email already in use"
ERRMSG_TWO_PASSWD_MUST_MATCH = "Passwords must be equal"
ERRMSG_INVALID_PASSWD = "Invalid password"
ERRMSG_INVALID_NAME = "Invalid name"
ERRMSG_CANNOT_UPDATE_ACCOUNT = "Cannot update account in database"

def update_account_interactor(dba: DBAccountsInterface, ph: Callable[[str], str], ucin: UpdateAccountUCI) -> UpdateAccountUCO:
    if not dba.account_id_exists(ucin.account_id):
        return UpdateAccountUCO(errmsg=ERRMSG_ACCOUNT_NOT_FOUND)

    if ucin.email != None and dba.email_exists(ucin.email):
        return UpdateAccountUCO(errmsg=ERRMSG_EMAIL_ALREADY_EXISTS)

    if ucin.name != None and not validate_name(ucin.name):
        return UpdateAccountUCO(errmsg=ERRMSG_INVALID_NAME)

    password_hashed = None
    if ucin.password != None:
        if ucin.password != ucin.password_again:
            return UpdateAccountUCO(errmsg=ERRMSG_TWO_PASSWD_MUST_MATCH)

        if not validate_password(ucin.password):
            return UpdateAccountUCO(errmsg=ERRMSG_INVALID_PASSWD)

        password_hashed = ph(ucin.password)

    if not dba.update(account_id=ucin.account_id, email=ucin.email, name=ucin.name, password_hashed=password_hashed):
        return UpdateAccountUCO(errmsg=ERRMSG_CANNOT_UPDATE_ACCOUNT)

    return UpdateAccountUCO()
