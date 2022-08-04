from typing import Dict

from accounts.interactors import DBAccountsInterface

class InMemoryDBAccounts(DBAccountsInterface):
    def __init__(self, data: Dict = None) -> None:
        if data is None:
            data = {"last_account_id": 0, "accounts": {}}

        self.data = data

    def create(self, atype: str, name: str, email: str, password_hashed: str):
        self.data["last_account_id"] += 1
        aid = self.data["last_account_id"]
        self.data["accounts"][aid] = {
            "type": atype,
            "name": name,
            "email": email,
            "password_hashed": password_hashed
        }
        return aid

def get_dba():
    return InMemoryDBAccounts()

def fake_password_hash(password: str) -> str:
    return f"hash:{password}"
