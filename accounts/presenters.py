from accounts.interactors import CreateAccountUCO

class CreateAccountVM:
    def __init__(self, id: int) -> None:
        self.id = id

def create_account_presenter(ucout: CreateAccountUCO):
    return CreateAccountVM(ucout.id)
