from unittest import main, TestCase
from accounts.entities import MIN_LEN_PASSWORD, Account

_vld_acctype = "deliveryguy"
_vld_name = "matheus"
_vld_email = "matheus@email.com"
_vld_password = "p"*MIN_LEN_PASSWORD

class TestAccountEntity(TestCase):
    def test_success(self):
        type = _vld_acctype
        name = _vld_name
        email = _vld_email
        password_hashed = _vld_password

        a = Account(type=type, name=name, email=email, password_hashed=password_hashed)

        self.assertEqual(a.type, type)
        self.assertEqual(a.name, name)
        self.assertEqual(a.email, email)
        self.assertEqual(a.password_hashed, password_hashed)

if __name__ == "__main__":
    main()
