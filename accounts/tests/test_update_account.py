from unittest import main, TestCase
from unittest.mock import Mock
from accounts.usecases.UpdateAccount.controller import (
    UpdateAccountReqM,
    update_account_controller
)
from accounts.usecases.common import (
    ERRMSG_ACCOUNT_NOT_FOUND,
    ERRMSG_CANNOT_UPDATE_ACCOUNT,
    ERRMSG_EMAIL_EXISTS,
    ERRMSG_INVALID_EMAIL,
    ERRMSG_INVALID_NAME,
    ERRMSG_INVALID_PASSWORD,
    ERRMSG_INVALID_USERNAME,
    ERRMSG_TWO_PASSWD_MUST_MATCH,
    ERRMSG_USERNAME_EXISTS
)
from accounts.usecases.UpdateAccount.interactor import (
    UpdateAccountUCI,
    UpdateAccountUCO,
    update_account_interactor
)
from accounts.usecases.UpdateAccount.presenter import (
    UpdateAccountVM,
    update_account_presenter
)
from accounts.usecases.UpdateAccount.view import (
    UpdateAccountResM,
    update_account_view
)
from accounts.tests.utils import (
    INVLD_EMAIL,
    INVLD_NAME,
    INVLD_PASSWORD,
    INVLD_USERNAME,
    VLD_EMAIL,
    VLD_NAME,
    VLD_PASSWORD,
    VLD_USERNAME
)

def _update_account_reqm():
    return UpdateAccountReqM(
        email=VLD_EMAIL,
        name=VLD_NAME,
        username=VLD_USERNAME,
        password=VLD_PASSWORD,
        password_again=VLD_PASSWORD,
    )

def _update_account_ucin():
    return UpdateAccountUCI(
        account_id=1,
        email=VLD_EMAIL,
        name=VLD_NAME,
        username=VLD_USERNAME,
        password=VLD_PASSWORD,
        password_again=VLD_PASSWORD,
    )

class TestController(TestCase):
    def test_success(self):
        reqm = _update_account_reqm()

        account_id = 1
        ucin = update_account_controller(account_id, reqm)

        self.assertIsInstance(ucin, UpdateAccountUCI)
        self.assertEqual(ucin.account_id, account_id)
        self.assertEqual(ucin.email, reqm.email)
        self.assertEqual(ucin.name, reqm.name)
        self.assertEqual(ucin.username, reqm.username)
        self.assertEqual(ucin.password, reqm.password)
        self.assertEqual(ucin.password_again, reqm.password_again)

class TestInteractor(TestCase):
    def test_success(self):
        ucin = _update_account_ucin()
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False
        dba.username_exists.return_value = False
        dba.update.return_value = True

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.username_exists.call_count, 1)
        self.assertEqual(dba.update.call_count, 1)
        self.assertEqual(ph.call_count, 1)

    def test_account_not_found(self):
        ucin = _update_account_ucin()
        dba = Mock()
        dba.account_id_exists.return_value = False

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)
        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_ACCOUNT_NOT_FOUND)

    def test_email_already_exists(self):
        ucin = _update_account_ucin()
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = True

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_EMAIL_EXISTS)

    def test_invalid_email(self):
        ucin = _update_account_ucin()
        ucin.email = INVLD_EMAIL
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_EMAIL)

    def test_invalid_username(self):
        ucin = _update_account_ucin()
        ucin.username = INVLD_USERNAME
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False
        dba.username_exists.return_value = False

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.username_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_USERNAME)

    def test_username_already_exists(self):
        ucin = _update_account_ucin()
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False
        dba.username_exists.return_value = True

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.username_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_USERNAME_EXISTS)

    def test_invalid_name(self):
        ucin = _update_account_ucin()
        ucin.name = INVLD_NAME
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False
        dba.username_exists.return_value = False

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.username_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_NAME)

    def test_passwd_must_match(self):
        ucin = _update_account_ucin()
        ucin.password = VLD_PASSWORD
        ucin.password_again = VLD_PASSWORD + "again"
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_TWO_PASSWD_MUST_MATCH)

    def test_passwd_must_match(self):
        ucin = _update_account_ucin()
        ucin.password = INVLD_PASSWORD
        ucin.password_again = INVLD_PASSWORD
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_PASSWORD)

    def test_passwd_must_match(self):
        ucin = _update_account_ucin()
        dba = Mock()
        dba.account_id_exists.return_value = True
        dba.email_exists.return_value = False
        dba.username_exists.return_value = False
        dba.update.return_value = False

        ph = Mock()

        ucout = update_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, UpdateAccountUCO)
        self.assertEqual(dba.account_id_exists.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.update.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_CANNOT_UPDATE_ACCOUNT)

class TestPresenter(TestCase):
    def test_success(self):
        ucout = UpdateAccountUCO()

        vm = update_account_presenter(ucout)

        self.assertIsInstance(vm, UpdateAccountVM)

class TestView(TestCase):
    def test_success(self):
        vm = UpdateAccountVM()

        resm = update_account_view(vm)

        self.assertIsInstance(resm, UpdateAccountResM)

if __name__ == "__main__":
    main()
