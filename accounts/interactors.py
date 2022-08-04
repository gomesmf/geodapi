from abc import ABC, abstractmethod
from typing import Callable

class DBAccountsInterface(ABC):
    @abstractmethod
    def create(self, ) -> int:
        pass

class CreateAccountUCI:
    def __init__(self, type: str, name: str, email: str, password: str) -> None:
        self.type = type
        self.name = name
        self.email = email
        self.password = password

class CreateAccountUCO:
    def __init__(self, aid: int) -> None:
        self.aid = aid

def create_account_interactor(dba: DBAccountsInterface, ph: Callable, ucin: CreateAccountUCI):
    password_hashed = ph(ucin.password)

    aid = dba.create(ucin.type, ucin.email, ucin.name, password_hashed)

    ucout = CreateAccountUCO(aid=aid)

    return ucout
