from unittest import main, TestCase
from accounts.entities import MIN_LEN_PASSWORD, Account
from accounts.tests.utils import VLD_ACCTYPE, VLD_EMAIL, VLD_NAME, VLD_PASSWORD, VLD_USERNAME

class TestAccountEntity(TestCase):
    def test_success(self):
        type = VLD_ACCTYPE
        name = VLD_NAME
        email = VLD_EMAIL
        username = VLD_USERNAME
        password_hashed = VLD_PASSWORD

        a = Account(type=type, name=name, email=email, username=username, password_hashed=password_hashed)

        self.assertEqual(a.type, type)
        self.assertEqual(a.name, name)
        self.assertEqual(a.email, email)
        self.assertEqual(a.username, username)
        self.assertEqual(a.password_hashed, password_hashed)

if __name__ == "__main__":
    main()
