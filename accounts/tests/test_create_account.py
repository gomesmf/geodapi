from unittest import main, TestCase
from unittest.mock import Mock
from accounts.tests.utils import (
    INVLD_EMAIL,
    INVLD_NAME,
    INVLD_PASSWORD,
    INVLD_USERNAME,
    VLD_ACCTYPE,
    VLD_EMAIL,
    VLD_NAME,
    VLD_PASSWORD,
    VLD_USERNAME
)
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
    ERRMSG_INVALID_USERNAME,
    ERRMSG_USERNAME_EXISTS,
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

class TestCreateAccountInteractor(TestCase):
    def test_success(self):
        ucin = CreateAccountUCI(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD,
        )
        dba = Mock()
        dba.email_exists.return_value = False
        dba.username_exists.return_value = False

        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(dba.create.call_count, 1)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.username_exists.call_count, 1)
        self.assertEqual(ph.call_count, 1)

    def test_cannot_create(self):
        ucin = CreateAccountUCI(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD,
        )
        dba = Mock()
        dba.email_exists.return_value = False
        dba.username_exists.return_value = False
        dba.create.return_value = False

        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(dba.username_exists.call_count, 1)
        self.assertEqual(dba.create.call_count, 1)
        self.assertEqual(ph.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_CANNOT_CREATE_ACCOUNT)

    def test_invld_acctype(self):
        ucin = CreateAccountUCI(
            type=INVLD_PASSWORD,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_ACCTYPE)

    def test_invld_password(self):
        ucin = CreateAccountUCI(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=INVLD_PASSWORD
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_PASSWORD)

    def test_invld_name(self):
        ucin = CreateAccountUCI(
            type=VLD_ACCTYPE,
            name=INVLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)
        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_NAME)

    def test_invld_name(self):
        ucin = CreateAccountUCI(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=INVLD_USERNAME,
            password=VLD_PASSWORD
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)
        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_USERNAME)

    def test_invld_email(self):
        ucin = CreateAccountUCI(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=INVLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)
        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_EMAIL)

    def test_email_already_exist(self):
        ucin = CreateAccountUCI(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD,
        )
        dba = Mock()
        dba.email_exists.return_value = True

        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_EMAIL_EXISTS)

    def test_username_already_exist(self):
        ucin = CreateAccountUCI(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD,
        )
        dba = Mock()
        dba.email_exists.return_value = False
        dba.username_exists.return_value = True

        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(dba.email_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_USERNAME_EXISTS)

class TestCreateAccountController(TestCase):
    def test_success(self):
        reqm = CreateAccountReqM(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password=VLD_PASSWORD
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
