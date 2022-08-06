from unittest import main, TestCase
from unittest.mock import Mock
from accounts.CreateAccount.controller import CreateAccountReqM
from accounts.CreateAccount.view import CreateAccountResM
from accounts.DeleteAccount.view import DeleteAccountResM
from accounts.GetAccountTypes.view import GetAccountTypesResM
from accounts.entities import MIN_LEN_PASSWORD, AccountType

from accounts.web import AccountsService

_vld_acctype = AccountType.DELIVERYGUY.value
_vld_name = "matheus"
_vld_email = "matheus@email.com"
_vld_password = "p"*MIN_LEN_PASSWORD

class TestCreateAccount(TestCase):
    def test_success(self):
        dba = Mock()
        ph = Mock()
        acs = AccountsService(dba, ph)

        reqm = CreateAccountReqM(
            type=_vld_acctype,
            name=_vld_name,
            email=_vld_email,
            password=_vld_password
        )

        dba.email_exists.return_value = False
        dba.create.return_value = True

        resm = acs.create_account(reqm)

        self.assertIsInstance(resm, CreateAccountResM)
        self.assertEqual(dba.email_exists.call_count, 1)
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

if __name__ == "__main__":
    main()
