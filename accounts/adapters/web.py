from typing import Callable

from accounts.interfaces.data import DBAccountsInterface
from accounts.interfaces.service import AccountsServiceInterface
from accounts.usecases.DeleteAccount.controller import delete_account_controller
from accounts.usecases.DeleteAccount.interactor import delete_account_interactor
from accounts.usecases.DeleteAccount.presenter import delete_account_presenter
from accounts.usecases.DeleteAccount.view import DeleteAccountResM, delete_account_view
from accounts.usecases.UpdateAccount.controller import UpdateAccountReqM, update_account_controller
from accounts.usecases.UpdateAccount.interactor import update_account_interactor
from accounts.usecases.UpdateAccount.presenter import update_account_presenter
from accounts.usecases.UpdateAccount.view import UpdateAccountResM, update_account_view
from accounts.usecases.CreateAccount.controller import CreateAccountReqM, create_account_controller
from accounts.usecases.CreateAccount.interactor import create_account_interactor
from accounts.usecases.CreateAccount.presenter import create_account_presenter
from accounts.usecases.CreateAccount.view import CreateAccountResM, create_account_view
from accounts.usecases.GetAccountTypes.interactor import get_account_types_interactor
from accounts.usecases.GetAccountTypes.presenter import get_account_types_presenter
from accounts.usecases.GetAccountTypes.view import GetAccountTypesResM, get_account_types_view

class AccountsService(AccountsServiceInterface):
    def __init__(self, dba: DBAccountsInterface, ph: Callable[[str], str]) -> None:
        self.dba = dba
        self.ph = ph

    def create_account(self, reqm: CreateAccountReqM) -> CreateAccountResM:
        ucin = create_account_controller(reqm)
        ucout = create_account_interactor(self.dba, self.ph, ucin)
        vm = create_account_presenter(ucout)
        resm = create_account_view(vm)
        return resm

    def get_account_types(self) -> GetAccountTypesResM:
        ucout = get_account_types_interactor()
        vm = get_account_types_presenter(ucout)
        resm = get_account_types_view(vm)
        return resm

    def delete_account(self, account_id: int) -> DeleteAccountResM:
        ucin = delete_account_controller(account_id)
        ucout = delete_account_interactor(self.dba, ucin)
        vm = delete_account_presenter(ucout)
        resm = delete_account_view(vm)
        return resm

    def update_account(self, account_id: int, reqm: UpdateAccountReqM) -> UpdateAccountResM:
        ucin = update_account_controller(account_id, reqm)
        ucout = update_account_interactor(self.dba, self.ph, ucin)
        vm = update_account_presenter(ucout)
        resm = update_account_view(vm)
        return resm

    def account_id_exists(self, account_id: int) -> bool:
        return self.dba.account_id_exists(account_id)
