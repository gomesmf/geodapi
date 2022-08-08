from .interactor import GetAccountTypesUCO

class GetAccountTypesVM:
    def __init__(self, account_types) -> None:
        self.account_types = account_types

def get_account_types_presenter(ucout: GetAccountTypesUCO):
    return GetAccountTypesVM(ucout.account_types)
