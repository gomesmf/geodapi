from .interactor import DeleteAccountUCI

def delete_account_controller(account_id: int) -> DeleteAccountUCI:
    return DeleteAccountUCI(account_id)
