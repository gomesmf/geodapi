from abc import ABC, abstractmethod

from accounts.entities import Account


class DBAccountsInterface(ABC):
    @abstractmethod
    def create(self, a: Account) -> int:
        pass
