from abc import ABC, abstractmethod

from .CreateAccount.controller import CreateAccountReqM
from .CreateAccount.view import CreateAccountResM
from .DeleteAccount.view import DeleteAccountResM
from .GetAccountTypes.view import GetAccountTypesResM

class AccountsServiceInterface(ABC):
    @abstractmethod
    def create_account(self, reqm: CreateAccountReqM) -> CreateAccountResM:
        pass

    @abstractmethod
    def get_account_types(self) -> GetAccountTypesResM:
        pass

    @abstractmethod
    def delete_account(self, account_id: int) -> DeleteAccountResM:
        pass
