from unittest import main, TestCase
from unittest.mock import Mock
from accounts.controllers import CreateAccountRequestModel, create_account_controller

from accounts.interactors import (
    CreateAccountUCI,
    CreateAccountUCO,
    create_account_interactor
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
        rm = CreateAccountRequestModel(
            type="deliveryguy",
            name="matheus",
            email="matheus@email.com",
            password="secret"
        )

        ucin = create_account_controller(rm)

        self.assertIsInstance(ucin, CreateAccountUCI)
        self.assertEqual(ucin.type, rm.type)
        self.assertEqual(ucin.name, rm.name)
        self.assertEqual(ucin.email, rm.email)
        self.assertEqual(ucin.password, rm.password)


if __name__ == "__main__":
    main()
