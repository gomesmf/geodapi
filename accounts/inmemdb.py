from typing import Dict
from accounts.entities import Account

from accounts.data import DBAccountsInterface

class InMemoryDBAccounts(DBAccountsInterface):
    def __init__(self, data: Dict = None) -> None:
        if data is None:
            data = {"last_account_id": 0, "accounts": {}}

        self.data = data

    def create(self, a: Account):
        self.data["last_account_id"] += 1
        aid = self.data["last_account_id"]
        a.id = aid
        self.data["accounts"][aid] = a
        return aid

    def email_exists(self, email: str) -> bool:
        for _, aobj in self.data["accounts"].items():
            if aobj.email == email:
                return True
        return False

def get_dba():
    return InMemoryDBAccounts()
