from abc import ABC, abstractmethod
from typing import Callable

class DBAccountsInterface(ABC):
    @abstractmethod
    def create(self, ) -> int:
        pass

class CreateAccountUseCaseInput:
    def __init__(self, atype: str, name: str, email: str, password: str) -> None:
        self.atype = atype
        self.name = name
        self.email = email
        self.password = password

class CreateAccountUseCaseOutput:
    def __init__(self, aid: int) -> None:
        self.aid = aid

def create_account_interactor(dba: DBAccountsInterface, ph: Callable, ucin: CreateAccountUseCaseInput):
    password_hashed = ph(ucin.password)

    aid = dba.create(ucin.atype, ucin.email, ucin.name, password_hashed)

    ucout = CreateAccountUseCaseOutput(aid=aid)

    return ucout
