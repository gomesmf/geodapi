import json

from passlib.context import CryptContext

from accounts.adapters.redisdb import RedisDBAccounts

from accounts.adapters.helpers import fake_password_hash, fake_password_verify, get_inmemdba
from deliveries.adapters.helpers import FakeDistanceService, FakeSearchService, get_inmemdbd
from deliveries.adapters.nominatim import NominatimSearch
from deliveries.adapters.geo import GeopyDistanceService

def read_config():
    with open("config.json") as f:
        configd = json.load(f)
    return configd

def get_db_accounts(configd):
    dba = get_inmemdba()
    if configd.get("db_accounts") == "redis":
        print("using redis database for accounts")
        dba = RedisDBAccounts()
    return dba

def get_passwd_manager(configd):
    ph = fake_password_hash
    pv = fake_password_verify
    if configd.get("pwdhashing") == "passlib":
        print("using password hashing")
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        ph = pwd_context.hash
        pv = pwd_context.verify
    return ph, pv

def get_db_deliveries(configd):
    dbd = get_inmemdbd()
    if configd.get("db_deliveries") == "redis":
        print("using redis database for deliveries")
        pass
    return dbd

def get_search_service(configd):
    ss = FakeSearchService()
    if configd.get("search_service") == "nominatim":
        print("using nominatim search service")
        ss = NominatimSearch()
    return ss

def get_distance_service(configd):
    ds = FakeDistanceService()
    if configd.get("distance_service") == "geopy":
        print("using geopy distance service")
        ds = GeopyDistanceService()
    return ds

