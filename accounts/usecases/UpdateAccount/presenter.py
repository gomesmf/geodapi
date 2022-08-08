from .interactor import UpdateAccountUCO

class UpdateAccountVM:
    def __init__(self, errmsg: str = None) -> None:
        self.errmsg = errmsg

def update_account_presenter(ucout: UpdateAccountUCO) -> UpdateAccountVM:
    return UpdateAccountVM(ucout.errmsg)
