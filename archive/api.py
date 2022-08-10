from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from accounts.auth import (
    authenticate_account,
    authorize_account,
    create_account_id_access_token,
    AccountM
)
from accounts.usecases.DeleteAccount.view import DeleteAccountResM
from accounts.usecases.UpdateAccount.controller import UpdateAccountReqM
from accounts.usecases.UpdateAccount.view import UpdateAccountResM
from accounts.adapters.web import (
    AccountsService,
    CreateAccountReqM,
    CreateAccountResM
)
from distances.adapters.web import (
    GeodistanceService,
    ComputeDistanceReqM,
    ComputeDistanceResM
)
from distances.usecases.GetDistances.view import GetDistancesResM

from config import dba, dbd, ss, ds, ph, pv

app = FastAPI(description="Delivery Guy API")

acs = AccountsService(dba, ph)

geods = GeodistanceService(acs, ss, ds, dbd)

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

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    account = authenticate_account(dba, pv, form_data.username, form_data.password)
    if not account:
        raise credentials_exception
    account_id_token = create_account_id_access_token(account.id)
    return {"access_token": account_id_token, "token_type": "bearer"}

@app.get("/accounts/me")
def get_accounts(current_account: AccountM = Depends(get_current_account)):
    return current_account

# @app.get("/accounts/all")
# def get_accounts():
#     return dba.data

# @app.get("/accounts/new", response_model=GetAccountTypesResM)
# def get_accounts():
#     return acs.get_account_types()

@app.post("/accounts", response_model=CreateAccountResM)
def create_account(name: str = Form(), username: str = Form(), email: str = Form(), password: str = Form()):
    reqm = CreateAccountReqM(
        name=name,
        username=username,
        email=email,
        password=password,
    )
    resm = acs.create_account(reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.delete("/accounts/me", response_model=DeleteAccountResM)
def delete_account(current_account: AccountM = Depends(get_current_account)):
    resm = acs.delete_account(current_account.account_id)

    if resm.errmsg:
        return JSONResponse(status_code=404, content=resm.dict())

    return resm

@app.put("/accounts/me", response_model=UpdateAccountResM)
def update_account(reqm: UpdateAccountReqM, current_account: AccountM = Depends(get_current_account)):
    resm = acs.update_account(current_account.account_id, reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.post("/distances", response_model=ComputeDistanceResM)
def compute_distance(reqm: ComputeDistanceReqM, current_account: AccountM = Depends(get_current_account)):
    resm = geods.compute_distance(current_account.account_id, reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.get("/distances", response_model=GetDistancesResM)
def get_distances(current_account: AccountM = Depends(get_current_account)):
    resm = geods.get_distances(current_account.account_id)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm
