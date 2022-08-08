from typing import Dict
from accounts.entities import Account

from accounts.interfaces.data import DBAccountsInterface

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

    def update(self, account_id: int, email: str = None, name: str = None, password_hashed: str = None) -> bool:
        aobj = self.data["accounts"][account_id]

        if email != None:
            aobj.email = email

        if name != None:
            aobj.name = name

        if password_hashed != None:
            aobj.password_hashed = password_hashed

        return True

    def get_accounts(self):
        return self.data

    def username_exists(self, username: str) -> bool:
        for _, aobj in self.data["accounts"].items():
            if username == aobj.email:
                return True
        return False

    def get_account_by_username(self, username: str) -> Account:
        for _, aobj in self.data["accounts"].items():
            if username == aobj.email:
                return aobj

    def get_account_by_id(self, account_id: int) -> Account:
        return self.data["accounts"][account_id]

def get_inmemdba():
    return InMemoryDBAccounts()

def fake_password_hash(password: str) -> str:
    return f"hash:{password}"
