from datetime import datetime, timedelta
from typing import Callable, Dict, Union
from accounts.entities import Account
from accounts.interfaces.data import DBAccountsInterface

from jose import jwt, JWTError

from json import loads, dumps

from pydantic import BaseModel

def authenticate_account(dba: DBAccountsInterface, pv: Callable[[str, str], bool], username: str, password: str) -> Union[bool, Account]:
    if not dba.username_exists(username):
        return False

    acc = dba.get_account_by_username(username)

    if not pv(password, acc.password_hashed):
        return False

    return acc

ACCESS_TOKEN_EXPIRE_MINUTES = 60
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "d47f5c1b2ae5a46f43454faf435a6e990221e1a00a5e886ed83da5370ee9b250"
ALGORITHM = "HS256"

def create_access_token(data: Dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_access_token(token: str) -> Dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def create_account_id_access_token(account_id: int, expires_delta: timedelta = None) -> str:
    subd = {"account_id": account_id}
    sub = dumps(subd)
    data = {"sub": sub}
    return create_access_token(data, expires_delta=expires_delta)

def decode_account_id_access_token(token: str) -> int:
    payload = decode_access_token(token)
    sub = payload["sub"]
    subd = loads(sub)
    account_id = subd["account_id"]
    return int(account_id)

class AccountM(BaseModel):
    account_id: int
    name: str
    username: str
    email: str

def authorize_account(dba: DBAccountsInterface, token: str) -> Union[Account, bool]:
    try:
        account_id = decode_account_id_access_token(token)
    except JWTError:
        return False

    if not dba.account_id_exists(account_id):
        return False

    acc = dba.get_account_by_id(account_id)
    if not acc:
        return False

    return AccountM(
        account_id=acc.id,
        name=acc.name,
        username=acc.username,
        email=acc.email
    )
