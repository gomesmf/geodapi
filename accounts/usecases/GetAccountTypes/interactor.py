from typing import Dict, List
from accounts.entities import AccountType

class GetAccountTypesUCO:
    def __init__(self, account_types: List[Dict[str, str]]) -> None:
        self.account_types = account_types

def get_account_types_interactor() -> GetAccountTypesUCO:
    account_types = [
        {"label": "Buyer", "value": AccountType.BUYER.value},
        {"label": "Seller", "value": AccountType.SELLER.value},
        {"label": "Delivery Guy", "value": AccountType.DELIVERYGUY.value},
    ]
    return GetAccountTypesUCO(account_types)
