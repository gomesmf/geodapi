import os

from passlib.context import CryptContext

from accounts.adapters.redisdb import RedisDBAccounts

from accounts.adapters.helpers import fake_password_hash, fake_password_verify, get_inmemdba

from deliveries.adapters.helpers import FakeDistanceService, FakeSearchService, get_inmemdbd
from deliveries.adapters.nominatim import NominatimSearch
from deliveries.adapters.geo import GeopyDistanceService
from deliveries.adapters.redisdb import RedisDBDistances

DB_REDIS = "redis"
PWD_HASHING_PASSLIB = "passlib"
SEARCH_SERVICE_NOMINATIM = "nominatim"
DISTANCE_SERVICE_GEOPY = "geopy"

def get_db_accounts():
    dba = get_inmemdba()
    if os.getenv("DB_ACCOUNTS") == DB_REDIS:
        print("accounts database: redis")
        dba = RedisDBAccounts()
    return dba

def get_passwd_manager():
    ph = fake_password_hash
    pv = fake_password_verify
    if os.getenv("PWD_HASHING") == PWD_HASHING_PASSLIB:
        print("password hashing: passlib")
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        ph = pwd_context.hash
        pv = pwd_context.verify
    return ph, pv

def get_db_deliveries():
    dbd = get_inmemdbd()
    if os.getenv("DB_DISTANCES") == "redis":
        print("distances database: redis")
        dbd = RedisDBDistances()
    return dbd

def get_search_service():
    ss = FakeSearchService()
    if os.getenv("SEARCH_SERVICE") == SEARCH_SERVICE_NOMINATIM:
        print("search service: nominatim")
        ss = NominatimSearch()
    return ss

def get_distance_service():
    ds = FakeDistanceService()
    if os.getenv("DISTANCE_SERVICE") == DISTANCE_SERVICE_GEOPY:
        print("distance service: geopy")
        ds = GeopyDistanceService()
    return ds

