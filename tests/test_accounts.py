from unittest import main, TestCase
from unittest.mock import Mock
from accounts.controllers import (
    CreateAccountReqM,
    create_account_controller
)
from accounts.interactors import (
    CreateAccountUCI,
    CreateAccountUCO,
    create_account_interactor
)
from accounts.presenters import (
    CreateAccountVM,
    create_account_presenter
)

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

class TestCreateAccountController(TestCase):
    def test_success(self):
        reqm = CreateAccountReqM(
            type="deliveryguy",
            name="matheus",
            email="matheus@email.com",
            password="secret"
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

if __name__ == "__main__":
    main()
