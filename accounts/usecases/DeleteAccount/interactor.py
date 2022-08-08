from accounts.interfaces.data import DBAccountsInterface


class DeleteAccountUCI:
    def __init__(self, account_id: int) -> None:
        self.account_id = account_id

class DeleteAccountUCO:
    def __init__(self, account_id: int = None, errmsg: str = None) -> None:
        self.account_id = account_id
        self.errmsg = errmsg

ERRMSG_ACCOUNT_NOT_FOUND = "Account does not exist"
ERRMSG_CANNOT_DELETE_ACCOUNT = "Cannot delete account from database"

def delete_account_interactor(dba: DBAccountsInterface, ucin: DeleteAccountUCI):
    if not dba.account_id_exists(ucin.account_id):
        return DeleteAccountUCO(account_id=ucin.account_id, errmsg=ERRMSG_ACCOUNT_NOT_FOUND)

    if not dba.delete(ucin.account_id):
        return DeleteAccountUCO(account_id=ucin.account_id, errmsg=ERRMSG_CANNOT_DELETE_ACCOUNT)

    return DeleteAccountUCO(account_id=ucin.account_id)
