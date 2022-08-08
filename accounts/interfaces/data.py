from abc import ABC, abstractmethod

from accounts.entities import Account


class DBAccountsInterface(ABC):
    @abstractmethod
    def account_id_exists(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def create(self, a: Account) -> bool:
        pass

    @abstractmethod
    def email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def delete(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, account_id: int, email: str = None, name: str = None, username: str = None, password_hashed: str = None) -> bool:
        pass

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def get_account_by_username(self, username: str) -> Account:
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Account:
        pass
