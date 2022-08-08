from unittest import main, TestCase
from unittest.mock import Mock
from accounts.tests.utils import VLD_ACCTYPE, VLD_EMAIL, VLD_NAME, VLD_PASSWORD, VLD_USERNAME
from accounts.usecases.CreateAccount.controller import CreateAccountReqM
from accounts.usecases.CreateAccount.view import CreateAccountResM
from accounts.usecases.DeleteAccount.view import DeleteAccountResM
from accounts.usecases.GetAccountTypes.view import GetAccountTypesResM
from accounts.usecases.UpdateAccount.controller import UpdateAccountReqM
from accounts.usecases.UpdateAccount.view import UpdateAccountResM
from accounts.entities import MIN_LEN_PASSWORD, AccountType

from accounts.adapters.web import AccountsService

class TestCreateAccount(TestCase):
    def test_success(self):
        dba = Mock()
        ph = Mock()
        acs = AccountsService(dba, ph)

        reqm = CreateAccountReqM(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD
        )

        dba.email_exists.return_value = False
        dba.username_exists.return_value = False
        dba.create.return_value = True

        resm = acs.create_account(reqm)

        self.assertIsInstance(resm, CreateAccountResM)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.username_exists.call_count, 1)
        self.assertEqual(ph.call_count, 1)
        self.assertEqual(dba.create.call_count, 1)

class TestGetAccountTypes(TestCase):
    def test_success(self):
        dba = Mock()
        ph = Mock()
        acs = AccountsService(dba, ph)
        resm = acs.get_account_types()
        self.assertIsInstance(resm, GetAccountTypesResM)

class TestDeleteAccount(TestCase):
    def test_success(self):
        dba = Mock()
        ph = Mock()
        acs = AccountsService(dba, ph)
        account_id = 1

        resm = acs.delete_account(account_id=account_id)

        self.assertIsInstance(resm, DeleteAccountResM)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.delete.call_count, 1)

class TestUpdateAccount(TestCase):
    def test_success(self):
        dba = Mock()
        ph = Mock()
        acs = AccountsService(dba, ph)

        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False
        dba.update.return_value = True

        account_id = 1

        reqm = UpdateAccountReqM(
            email=VLD_EMAIL,
            name=VLD_NAME,
            password=VLD_PASSWORD,
            password_again=VLD_PASSWORD
        )

        resm = acs.update_account(account_id, reqm)

        self.assertIsInstance(resm, UpdateAccountResM)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.update.call_count, 1)

class TestAccountIdExists(TestCase):
    def test_success(self):
        dba = Mock()
        ph = Mock()
        acs = AccountsService(dba, ph)
        dba.account_id_exists.return_value = True

        account_id = 1

        aidexists = acs.account_id_exists(account_id)
        self.assertTrue(aidexists)

    def test_success(self):
        dba = Mock()
        ph = Mock()
        acs = AccountsService(dba, ph)
        dba.account_id_exists.return_value = False

        account_id = 1

        aidexists = acs.account_id_exists(account_id)
        self.assertFalse(aidexists)

if __name__ == "__main__":
    main()
