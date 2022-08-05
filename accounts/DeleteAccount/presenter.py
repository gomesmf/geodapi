from accounts.DeleteAccount.interactor import DeleteAccountUCO

class DeleteAccountVM:
    def __init__(self, account_id: int = None, errmsg: str = None) -> None:
        self.account_id = account_id
        self.errmsg = errmsg

def delete_account_presenter(ucout: DeleteAccountUCO) -> DeleteAccountVM:
    return DeleteAccountVM(account_id=ucout.account_id, errmsg=ucout.errmsg)
