import json

from passlib.context import CryptContext

from accounts.adapters.helpers import fake_password_hash, fake_password_verify, get_inmemdba
from distances.adapters.helpers import FakeDistanceService, FakeSearchService, get_inmemdbd
from distances.adapters.nominatim import NominatimSearch
from distances.adapters.geo import GeopyDistanceService

with open("config.json") as f:
    configd = json.load(f)

print("config", configd)

dba = get_inmemdba()
dbd = get_inmemdbd()
ph = fake_password_hash
pv = fake_password_verify
ss = FakeSearchService()
ds = FakeDistanceService()

if configd.get("db_accounts") == "redis":
    print("using redis database for accounts")
    pass

if configd.get("pwdhashing") == "passlib":
    print("using password hashing")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ph = pwd_context.hash
    pv = pwd_context.verify

if configd.get("db_distances") == "redis":
    print("using redis database for distances")
    pass

if configd.get("search_service") == "nominatim":
    print("using nominatim search service")
    ss = NominatimSearch()

if configd.get("distance_service") == "geopy":
    print("using geopy distance service")
    ds = GeopyDistanceService()
