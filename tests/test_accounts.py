from unittest import main, TestCase
from unittest.mock import Mock
from accounts.controllers import (
    CreateAccountReqM,
    create_account_controller
)
from accounts.interactors import (
    ERRMSG_INVALID_EMAIL,
    ERRMSG_INVALID_NAME,
    ERRMSG_INVALID_PASSWORD,
    MIN_LEN_PASSWORD,
    CreateAccountUCI,
    CreateAccountUCO,
    create_account_interactor
)
from accounts.presenters import (
    CreateAccountVM,
    create_account_presenter
)
from accounts.views import (
    CreateAccountResM,
    create_account_view
)

_valid_name = "matheus"
_valid_email = "matheus@email.com"
_valid_password = "p"*MIN_LEN_PASSWORD
_invalid_name = ""
_invalid_email = "matheus"
_invalid_password = "1"*(MIN_LEN_PASSWORD-1)

class TestCreateAccountInteractor(TestCase):
    def test_success(self):
        ucin = CreateAccountUCI(
            type="deliveryguy",
            name="matheus",
            email="matheus@email.com",
            password="secret",
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(dba.create.call_count, 1)
        self.assertEqual(ph.call_count, 1)

    def test_invalid_password(self):
        ucin = CreateAccountUCI(
            type="deliveryguy",
            name=_valid_name,
            email=_valid_email,
            password=_invalid_password
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_PASSWORD)

    def test_invalid_name(self):
        ucin = CreateAccountUCI(
            type="deliveryguy",
            name=_invalid_name,
            email=_valid_email,
            password=_valid_password
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)
        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_NAME)

    def test_invalid_email(self):
        ucin = CreateAccountUCI(
            type="deliveryguy",
            name=_valid_name,
            email=_invalid_email,
            password=_valid_password
        )
        dba = Mock()
        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)
        self.assertIsInstance(ucout, CreateAccountUCO)
        self.assertEqual(ucout.errmsg, ERRMSG_INVALID_EMAIL)

class TestCreateAccountController(TestCase):
    def test_success(self):
        reqm = CreateAccountReqM(
            type="deliveryguy",
            name=_valid_name,
            email=_valid_email,
            password=_valid_password
        )

        ucin = create_account_controller(reqm)

        self.assertIsInstance(ucin, CreateAccountUCI)
        self.assertEqual(ucin.type, reqm.type)
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
