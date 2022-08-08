from typing import List
from pydantic import BaseModel

from .presenter import GetAccountTypesVM

class AccountTypeM(BaseModel):
    label: str
    value: str

class GetAccountTypesResM(BaseModel):
    account_types: List[AccountTypeM]

def get_account_types_view(vm: GetAccountTypesVM) -> GetAccountTypesResM:
    atlist = []

    for at in vm.account_types:
        atlist.append(AccountTypeM(label=at["label"], value=at["value"]))

    return GetAccountTypesResM(account_types=atlist)
