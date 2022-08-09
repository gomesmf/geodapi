from json import JSONEncoder, dumps, loads
from accounts.entities import Account
from accounts.interfaces.data import DBAccountsInterface

import redis

class object_encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def account_encode(a: Account):
    return dumps(a, indent=2, cls=object_encoder)

def account_object_hook(obj):
    return Account(
        id=obj["id"],
        type=obj["type"],
        name=obj["name"],
        email=obj["email"],
        username=obj["username"],
        password_hashed=obj["password_hashed"],
    )

def accound_decode(ajson: str):
    return loads(ajson, object_hook=account_object_hook)

DEFAULT_REDIS_HOST = "localhost"

_k_last_user_id = "last_user_id"
_n_accounts = "accounts"
_n_username_id = "username_id"
_n_email_id = "email_id"

class RedisDBAccounts(DBAccountsInterface):
    def __init__(self, host: str = DEFAULT_REDIS_HOST) -> None:
        self.rdb = redis.Redis(host=host, decode_responses=True)

        if not self.rdb.exists(_k_last_user_id):
            self._set_last_user_id(0)

    def _flush(self):
        self.rdb.flushall()

    def _set_last_user_id(self, v: int = 0):
        self.rdb.set(_k_last_user_id, v)
        self.rdb.save()

    def account_id_exists(self, account_id: int) -> bool:
        return self.rdb.hexists(_n_accounts, account_id)

    def create(self, a: Account) -> bool:
        self.rdb.incr(_k_last_user_id, 1)
        aid = self.rdb.get(_k_last_user_id)
        a.id = aid
        ajson = account_encode(a)

        self.rdb.hset(_n_accounts, aid, ajson)
        self.rdb.hset(_n_username_id, a.username, aid)
        self.rdb.hset(_n_email_id, a.email, aid)

        self.rdb.save()

        return True

    def email_exists(self, email: str) -> bool:
        return self.rdb.hexists(_n_email_id, email)

    def delete(self, account_id: int) -> bool:
        aobj = self.get_account_by_id(account_id)
        self.rdb.hdel(_n_accounts, account_id)
        self.rdb.hdel(_n_email_id, aobj.email)
        self.rdb.hdel(_n_username_id, aobj.username)
        return True

    def update(self, account_id: int, email: str = None, name: str = None, username: str = None, password_hashed: str = None) -> bool:
        aobj = self.get_account_by_id(account_id)

        self.delete(account_id)

        if email != None:
            aobj.email = email
        if name != None:
            aobj.name = name
        if username != None:
            aobj.username = username
        if password_hashed != None:
            aobj.password_hashed = password_hashed

        ajson = account_encode(aobj)

        self.rdb.hset(_n_accounts, aobj.id, ajson)
        self.rdb.hset(_n_username_id, aobj.username, aobj.id)
        self.rdb.hset(_n_email_id, aobj.email, aobj.id)

        return True

    def username_exists(self, username: str) -> bool:
        return self.rdb.hexists(_n_username_id, username)

    def get_account_by_username(self, username: str) -> Account:
        account_id = self.rdb.hget(_n_username_id, username)
        return self.get_account_by_id(account_id)

    def get_account_by_id(self, account_id: int) -> Account:
        ajson = self.rdb.hget(_n_accounts, account_id)
        aobj = accound_decode(ajson)
        return aobj
