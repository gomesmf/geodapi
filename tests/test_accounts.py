from unittest import main, TestCase
from unittest.mock import Mock

from accounts.interactors import (
    CreateAccountUseCaseInput,
    CreateAccountUseCaseOutput,
    create_account_interactor
)

class TestCreateAccountInteractor(TestCase):
    def test_success(self):
        ucin = CreateAccountUseCaseInput(
            atype = "deliveryguy",
            name = "matheus",
            email = "matheus@email.com",
            password = "secret",
        )

        dba = Mock()

        ph = Mock()

        ucout = create_account_interactor(dba, ph, ucin)

        self.assertIsInstance(ucout, CreateAccountUseCaseOutput)
        self.assertEqual(dba.create.call_count, 1)
        self.assertEqual(ph.hash.call_count, 1)

if __name__ == "__main__":
    main()
