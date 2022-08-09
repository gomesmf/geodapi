from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from accounts.adapters.web import AccountsService
from accounts.auth import authorize_account
from deliveries.adapters.web import DeliveriesService

from .config import (
    get_db_accounts,
    get_db_deliveries,
    get_passwd_manager,
    get_search_service,
    get_distance_service,
    read_config,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=400,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"}
)

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

async def get_current_account(token: str = Depends(oauth2_scheme)):
    acc = authorize_account(dba, token)
    if not acc:
        raise unauthorized_exception
    return acc

configd = read_config()
dba = get_db_accounts(configd)
dbd = get_db_deliveries(configd)
ph, pv = get_passwd_manager(configd)
ss = get_search_service(configd)
ds = get_distance_service(configd)

acs = AccountsService(dba, ph)
delis = DeliveriesService(acs, ss, ds, dbd)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
