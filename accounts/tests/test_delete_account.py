from unittest import main, TestCase
from unittest.mock import Mock

from accounts.usecases.DeleteAccount.controller import delete_account_controller
from accounts.usecases.DeleteAccount.interactor import (
    ERRMSG_ACCOUNT_NOT_FOUND,
    ERRMSG_CANNOT_DELETE_ACCOUNT,
    DeleteAccountUCI,
    DeleteAccountUCO,
    delete_account_interactor
)
from accounts.usecases.DeleteAccount.presenter import DeleteAccountVM, delete_account_presenter
from accounts.usecases.DeleteAccount.view import DeleteAccountResM, delete_account_view

class TestController(TestCase):
    def test_success(self):
        account_id = 1
        ucin = delete_account_controller(account_id)
        self.assertIsInstance(ucin, DeleteAccountUCI)
        self.assertEqual(ucin.account_id, account_id)

class TestInteractor(TestCase):
    def test_success(self):
        account_id = 1
        ucin = DeleteAccountUCI(account_id=account_id)

        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.delete.return_value = True

        ucout = delete_account_interactor(dba, ucin)

        self.assertIsInstance(ucout, DeleteAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.delete.call_count, 1)
        self.assertEqual(ucout.account_id, ucin.account_id)
        self.assertIsNone(ucout.errmsg)

    def test_account_not_found(self):
        account_id = 1
        ucin = DeleteAccountUCI(account_id=account_id)

        dba = Mock()
        dba.account_id_exists.return_value = False

        ucout = delete_account_interactor(dba, ucin)

        self.assertIsInstance(ucout, DeleteAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(ucout.account_id, ucin.account_id)
        self.assertEqual(ucout.errmsg, ERRMSG_ACCOUNT_NOT_FOUND)

    def test_cannot_delete_account(self):
        account_id = 1
        ucin = DeleteAccountUCI(account_id=account_id)

        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.delete.return_value = False

        ucout = delete_account_interactor(dba, ucin)

        self.assertIsInstance(ucout, DeleteAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(ucout.account_id, ucin.account_id)
        self.assertEqual(ucout.errmsg, ERRMSG_CANNOT_DELETE_ACCOUNT)


class TestPresenter(TestCase):
    def test_success(self):
        ucout = DeleteAccountUCO(account_id=1, errmsg="errmsg")

        vm = delete_account_presenter(ucout)

        self.assertIsInstance(vm, DeleteAccountVM)
        self.assertEqual(vm.account_id, ucout.account_id)
        self.assertEqual(vm.errmsg, ucout.errmsg)

class TestView(TestCase):
    def test_success(self):
        vm = DeleteAccountVM(account_id=1)

        resm = delete_account_view(vm)

        self.assertIsInstance(resm, DeleteAccountResM)

if __name__ == "__main__":
    main()
