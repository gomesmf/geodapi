from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from accounts.adapters.web import AccountsService
from accounts.auth import authorize_account
from distances.adapters.web import GeodistanceService

from app.config import (
    get_db_accounts,
    get_db_distances,
    get_passwd_manager,
    get_search_service,
    get_distance_service,
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

dba = get_db_accounts()
dbd = get_db_distances()
ph, pv = get_passwd_manager()
ss = get_search_service()
ds = get_distance_service()

acs = AccountsService(dba, ph)
geods = GeodistanceService(acs, ss, ds, dbd)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
