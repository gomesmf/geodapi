from fastapi import FastAPI
from fastapi.responses import JSONResponse

from accounts.usecases.DeleteAccount.view import DeleteAccountResM
from accounts.usecases.UpdateAccount.controller import UpdateAccountReqM
from accounts.usecases.UpdateAccount.view import UpdateAccountResM
from accounts.adapters.web import (
    AccountsService,
    CreateAccountReqM,
    CreateAccountResM,
    GetAccountTypesResM
)
from accounts.adapters.helpers import fake_password_hash, get_inmemdba

from deliveries.adapters.geo import GeopyDistanceService
from deliveries.adapters.helpers import (
    FakeDistanceService,
    FakeSearchService,
    get_inmemdbd
)
from deliveries.adapters.nominatim import NominatimSearch
from deliveries.adapters.web import (
    DeliveriesService,
    ComputeDistanceReqM,
    ComputeDistanceResM
)
from deliveries.usecases.GetDistances.view import GetDistancesResM

app = FastAPI(description="Delivery Guy API")

dba = get_inmemdba()

ph = fake_password_hash

acs = AccountsService(dba, ph)

dbd = get_inmemdbd()

# ss = FakeSearchService()
ss = NominatimSearch()

# ds = FakeDistanceService()
ds = GeopyDistanceService()

delis = DeliveriesService(acs, ss, ds, dbd)

@app.get("/accounts")
def get_accounts():
    return dba.get_accounts()

# @app.get("/accounts/new", response_model=GetAccountTypesResM)
# def get_accounts():
#     return acs.get_account_types()

@app.post("/accounts", response_model=CreateAccountResM)
def create_account(reqm: CreateAccountReqM):
    resm = acs.create_account(reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.delete("/accounts/me", response_model=DeleteAccountResM)
def delete_account(account_id: int):
    resm = acs.delete_account(account_id)

    if resm.errmsg:
        return JSONResponse(status_code=404, content=resm.dict())

    return resm

@app.put("/accounts/me", response_model=UpdateAccountResM)
def update_account(account_id: int, reqm: UpdateAccountReqM):
    resm = acs.update_account(account_id, reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.post("/distances", response_model=ComputeDistanceResM)
def compute_distance(account_id: int, reqm: ComputeDistanceReqM):
    resm = delis.compute_distance(account_id, reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.get("/distances", response_model=GetDistancesResM)
def get_distances(account_id: int):
    resm = delis.get_distances(account_id)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm
