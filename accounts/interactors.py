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
    def __init__(self, id: int) -> None:
        self.id = id

def create_account_interactor(dba: DBAccountsInterface, ph: Callable, ucin: CreateAccountUCI):
    password_hashed = ph(ucin.password)

    id = dba.create(ucin.type, ucin.email, ucin.name, password_hashed)

    ucout = CreateAccountUCO(id=id)

    return ucout
