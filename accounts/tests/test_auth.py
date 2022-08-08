from datetime import timedelta
from unittest import main, TestCase
from unittest.mock import Mock
from accounts.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_account,
    create_access_token,
    create_account_id_access_token,
    decode_access_token,
    decode_account_id_access_token
)
from accounts.entities import Account

class TestAuthenticate(TestCase):
    def test_success(self):
        pv = Mock()
        pv.return_value = True

        dba = Mock()
        dba.username_exists.return_value = True

        acc = Account()
        dba.get_account_by_username.return_value = acc

        username = "gomesmf"
        password = "secret"

        r = authenticate_account(dba, pv, username, password)

        self.assertIsInstance(r, Account)
        self.assertEqual(dba.username_exists.call_count, 1)
        self.assertEqual(dba.get_account_by_username.call_count, 1)
        self.assertEqual(pv.call_count, 1)

class TestJWT(TestCase):
    def test_success(self):
        account_id = 1
        data = {"account_id": account_id}
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        encoded_jwt = create_access_token(data, expires_delta)

        self.assertIsInstance(encoded_jwt, str)

    def test_decode_jwt(self):
        data = {"sub": "account_id:123"}
        token = create_access_token(data)
        payload = decode_access_token(token)
        self.assertEqual(payload["sub"], data["sub"])

    def test_create_account_id_access_token(self):
        account_id = 1
        encoded_jwt = create_account_id_access_token(account_id)
        self.assertIsInstance(encoded_jwt, str)

    def test_decode_account_id_access_token(self):
        account_id = 1
        encoded_jwt = create_account_id_access_token(account_id)
        account_id_got = decode_account_id_access_token(encoded_jwt)
        self.assertEqual(account_id_got, account_id)


if __name__ == "__main__":
    main()
