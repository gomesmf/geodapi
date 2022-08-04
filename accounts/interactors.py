from abc import ABC, abstractmethod

class DBAccountsInterface(ABC):
    @abstractmethod
    def create(self, ) -> int:
        pass

class PasswordHasherInterface(ABC):
    @abstractmethod
    def hash(self, password: str):
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

def create_account_interactor(dba: DBAccountsInterface, ph: PasswordHasherInterface, ucin: CreateAccountUseCaseInput):
    password_hashed = ph.hash(ucin.password)

    aid = dba.create(ucin.atype, ucin.email, ucin.name, password_hashed)

    ucout = CreateAccountUseCaseOutput(aid=aid)

    return ucout
