from typing import Callable

from accounts.data import DBAccountsInterface
from .service import AccountsServiceInterface

from .CreateAccount.controller import CreateAccountReqM, create_account_controller
from .CreateAccount.interactor import create_account_interactor
from .CreateAccount.presenter import create_account_presenter
from .CreateAccount.view import CreateAccountResM, create_account_view

from .GetAccountTypes.interactor import get_account_types_interactor
from .GetAccountTypes.presenter import get_account_types_presenter
from .GetAccountTypes.view import GetAccountTypesResM, get_account_types_view

class AccountsService(AccountsServiceInterface):
    def create_account(self, dba: DBAccountsInterface, ph: Callable[[str], str], reqm: CreateAccountReqM) -> CreateAccountResM:
        ucin = create_account_controller(reqm)
        ucout = create_account_interactor(dba, ph, ucin)
        vm = create_account_presenter(ucout)
        resm = create_account_view(vm)
        return resm

    def get_account_types(self) -> GetAccountTypesResM:
        ucout = get_account_types_interactor()
        vm = get_account_types_presenter(ucout)
        resm = get_account_types_view(vm)
        return resm

