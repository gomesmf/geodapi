from .interactor import CreateAccountUCO

class CreateAccountVM:
    def __init__(self, id: int = None, errmsg: str = None) -> None:
        self.id = id
        self.errmsg = errmsg

def create_account_presenter(ucout: CreateAccountUCO) -> CreateAccountVM:
    return CreateAccountVM(id=ucout.id, errmsg=ucout.errmsg)
