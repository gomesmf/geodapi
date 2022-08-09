from unittest import main, TestCase
from accounts.adapters.redisdb import RedisDBAccounts, accound_decode, account_encode
from accounts.entities import Account
from accounts.tests.utils import VLD_ACCTYPE, VLD_EMAIL, VLD_NAME, VLD_PASSWORD, VLD_USERNAME

class TestAccountEntity(TestCase):
    def test_encode(self):
        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )

        ajson = account_encode(a)

        # print(ajson)
        self.assertIsInstance(ajson, str)

    def test_decode(self):
        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )

        ajson = account_encode(a)
        self.assertIsInstance(ajson, str)

        aobj = accound_decode(ajson)
        self.assertIsInstance(aobj, Account)

    def test_create_account(self):
        dba = RedisDBAccounts()
        dba._flush()

        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )
        r = dba.create(a)
        self.assertTrue(r)

    def test_account_id_exists(self):
        dba = RedisDBAccounts()
        dba._flush()

        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )
        self.assertTrue(dba.create(a))

        self.assertTrue(dba.account_id_exists(a.id))
        self.assertFalse(dba.account_id_exists(123232))

    def test_email_exists(self):
        dba = RedisDBAccounts()
        dba._flush()

        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )
        self.assertTrue(dba.create(a))

        self.assertTrue(dba.email_exists(a.email))
        self.assertFalse(dba.email_exists("ggfg@gdfgd"))

    def test_username_exists(self):
        dba = RedisDBAccounts()
        dba._flush()

        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )
        self.assertTrue(dba.create(a))

        self.assertTrue(dba.username_exists(a.username))
        self.assertFalse(dba.username_exists("dsfdf"))

    def test_get_account_by_id(self):
        dba = RedisDBAccounts()
        dba._flush()

        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )
        self.assertTrue(dba.create(a))

        a_got = dba.get_account_by_id(a.id)

        self.assertIsInstance(a_got, Account)
        self.assertEqual(a.type, a_got.type)
        self.assertEqual(a.name, a_got.name)
        self.assertEqual(a.email, a_got.email)
        self.assertEqual(a.username, a_got.username)
        self.assertEqual(a.password_hashed, a_got.password_hashed)

    def test_get_account_by_username(self):
        dba = RedisDBAccounts()
        dba._flush()

        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )
        self.assertTrue(dba.create(a))

        a_got = dba.get_account_by_username(a.username)

        self.assertIsInstance(a_got, Account)
        self.assertEqual(a.type, a_got.type)
        self.assertEqual(a.name, a_got.name)
        self.assertEqual(a.email, a_got.email)
        self.assertEqual(a.username, a_got.username)
        self.assertEqual(a.password_hashed, a_got.password_hashed)

    def test_delete(self):
        dba = RedisDBAccounts()
        dba._flush()

        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )
        self.assertTrue(dba.create(a))

        dba.delete(a.id)

        self.assertFalse(dba.account_id_exists(a.id))

    def test_update(self):
        dba = RedisDBAccounts()
        dba._flush()

        a = Account(
            type=VLD_ACCTYPE,
            name=VLD_NAME,
            email=VLD_EMAIL,
            username=VLD_USERNAME,
            password_hashed=VLD_PASSWORD
        )
        self.assertTrue(dba.create(a))

        new_name = "matheus"
        new_email = "gomes@gmail.com"
        new_username = "gomesmf"
        new_password_hashed = "fdsfsdfs"

        self.assertTrue(dba.update(a.id, new_email, new_name, new_username, new_password_hashed))

        a_got = dba.get_account_by_id(a.id)

        self.assertIsInstance(a_got, Account)
        self.assertEqual(a_got.name, new_name)
        self.assertEqual(a_got.email, new_email)
        self.assertEqual(a_got.username, new_username)
        self.assertEqual(a_got.password_hashed, new_password_hashed)


if __name__ == "__main__":
    main()
