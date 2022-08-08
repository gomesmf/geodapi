from unittest import main, TestCase
from unittest.mock import Mock
from accounts.entities import MIN_LEN_PASSWORD, AccountType
from accounts.usecases.CreateAccount.controller import (
    CreateAccountReqM,
    create_account_controller
)
from accounts.usecases.CreateAccount.interactor import (
    ERRMSG_CANNOT_CREATE_ACCOUNT,
    ERRMSG_EMAIL_EXISTS,
    ERRMSG_INVALID_ACCTYPE,
    ERRMSG_INVALID_EMAIL,
    ERRMSG_INVALID_NAME,
    ERRMSG_INVALID_PASSWORD,
    CreateAccountUCI,
    CreateAccountUCO,
    create_account_interactor
)
from accounts.usecases.CreateAccount.presenter import (
    CreateAccountVM,
    create_account_presenter
)
from accounts.usecases.CreateAccount.view import (
    CreateAccountResM,
    create_account_view
)

_vld_acctype = AccountType.DELIVERYGUY.value
_vld_name = "matheus"
_vld_email = "matheus@email.com"
_vld_password = "p"*MIN_LEN_PASSWORD
_invld_acctype = "wrongtype"
_invld_name = ""
_invld_email = "matheus"
_invld_password = "1"*(MIN_LEN_PASSWORD-1)

class TestCreateAccountInteractor(TestCase):
    def test_success(self):
        ucin = CreateAccountUCI(
            type=_vld_acctype,
            name=_vld_name,
            email=_vld_email,
            password=_vld_password,
        )
        dba = Mock()
        dba.email_exists.return_value = False

        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(dba.create.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(ph.call_count, 1)

    def test_cannot_create(self):
        ucin = CreateAccountUCI(
            type=_vld_acctype,
            name=_vld_name,
            email=_vld_email,
            password=_vld_password,
        )
        dba = Mock()
        dba.email_exists.return_value = False
        dba.create.return_value = False

        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.create.call_count, 1)
        self.assertEqual(ph.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_CANNOT_CREATE_ACCOUNT)

    def test_invld_acctype(self):
        ucin = CreateAccountUCI(
            type=_invld_acctype,
            name=_vld_name,
            email=_vld_email,
            password=_vld_password
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_ACCTYPE)

    def test_invld_password(self):
        ucin = CreateAccountUCI(
            type=_vld_acctype,
            name=_vld_name,
            email=_vld_email,
            password=_invld_password
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_PASSWORD)

    def test_invld_name(self):
        ucin = CreateAccountUCI(
            type=_vld_acctype,
            name=_invld_name,
            email=_vld_email,
            password=_vld_password
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)
        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_NAME)

    def test_invld_email(self):
        ucin = CreateAccountUCI(
            type=_vld_acctype,
            name=_vld_name,
            email=_invld_email,
            password=_vld_password
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)
        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_EMAIL)

    def test_email_already_exist(self):
        ucin = CreateAccountUCI(
            type=_vld_acctype,
            name=_vld_name,
            email=_vld_email,
            password=_vld_password,
        )
        dba = Mock()
        dba.email_exists.return_value = True

        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_EMAIL_EXISTS)

class TestCreateAccountController(TestCase):
    def test_success(self):
        reqm = CreateAccountReqM(
            type=_vld_acctype,
            name=_vld_name,
            email=_vld_email,
            password=_vld_password
        )

        ucin = create_account_controller(reqm)

        self.assertIsInstance(ucin, CreateAccountUCI)
        # self.assertEqual(ucin.type, reqm.type)
        self.assertEqual(ucin.name, reqm.name)
        self.assertEqual(ucin.email, reqm.email)
        self.assertEqual(ucin.password, reqm.password)

class TestCreateAccountPresenter(TestCase):
    def test_success(self):
        ucout = CreateAccountUCO(id=1)

        vm = create_account_presenter(ucout)

        self.assertIsInstance(vm, CreateAccountVM)
        self.assertEqual(vm.id, ucout.id)

class TestCreateAccountView(TestCase):
    def test_success(self):
        vm = CreateAccountVM(id=1)

        resm = create_account_view(vm)

        self.assertIsInstance(resm, CreateAccountResM)
        self.assertEqual(resm.id, vm.id)
        self.assertIsNone(resm.errmsg)

    def test_errmsg(self):
        vm = CreateAccountVM(errmsg="errormsg")
        resm = create_account_view(vm)
        self.assertIsInstance(resm, CreateAccountResM)
        self.assertEqual(resm.errmsg, vm.errmsg)

if __name__ == "__main__":
    main()
