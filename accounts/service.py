from abc import ABC, abstractmethod

from accounts.UpdateAccount.controller import UpdateAccountReqM
from accounts.UpdateAccount.view import UpdateAccountResM

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

    @abstractmethod
    def update_account(self, account_id: int, reqm: UpdateAccountReqM) -> UpdateAccountResM:
        pass

    @abstractmethod
    def account_id_exists(self, account_id: int) -> bool:
        pass
