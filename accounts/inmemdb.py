from typing import Dict
from accounts.entities import Account

from accounts.data import DBAccountsInterface

class InMemoryDBAccounts(DBAccountsInterface):
    def __init__(self, data: Dict = None) -> None:
        if data is None:
            data = {"last_account_id": 0, "accounts": {}}

        self.data = data

    def account_id_exists(self, account_id: int) -> bool:
        return account_id in self.data["accounts"]

    def create(self, a: Account) -> bool:
        self.data["last_account_id"] += 1
        aid = self.data["last_account_id"]
        a.id = aid
        self.data["accounts"][aid] = a
        return True

    def email_exists(self, email: str) -> bool:
        for _, aobj in self.data["accounts"].items():
            if aobj.email == email:
                return True
        return False

    def delete(self, account_id: int) -> bool:
        del self.data["accounts"][account_id]
        return True

def get_dba():
    return InMemoryDBAccounts()
