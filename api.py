from fastapi import FastAPI
from fastapi.responses import JSONResponse

from accounts.DeleteAccount.view import DeleteAccountResM
from accounts.UpdateAccount.controller import UpdateAccountReqM
from accounts.UpdateAccount.view import UpdateAccountResM
from accounts.web import (
    AccountsService,
    CreateAccountReqM,
    CreateAccountResM,
    GetAccountTypesResM
)
from accounts.helpers import fake_password_hash, get_inmemdba

from deliveries.ComputeDistance.controller import ComputeDistanceReqM
from deliveries.ComputeDistance.view import ComputeDistanceResM
from deliveries.helpers import FakeDistanceService, FakeSearchService, get_inmemdbd
from deliveries.web import DelieveriesService

app = FastAPI(description="Delivery Guy API")

dba = get_inmemdba()

ph = fake_password_hash

acs = AccountsService(dba, ph)

dbd = get_inmemdbd()

ss = FakeSearchService()

ds = FakeDistanceService()

delis = DelieveriesService(acs, ss, ds, dbd)

@app.get("/accounts")
def get_accounts():
    return dba.data

@app.get("/accounts/new", response_model=GetAccountTypesResM)
def get_accounts():
    return acs.get_account_types()

@app.post("/accounts", response_model=CreateAccountResM)
def create_account(reqm: CreateAccountReqM):
    resm = acs.create_account(reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.delete("/accounts/{account_id}", response_model=DeleteAccountResM)
def delete_account(account_id: int):
    resm = acs.delete_account(account_id)

    if resm.errmsg:
        return JSONResponse(status_code=404, content=resm.dict())

    return resm

@app.put("/accounts/{account_id}", response_model=UpdateAccountResM)
def update_account(account_id: int, reqm: UpdateAccountReqM):
    resm = acs.update_account(account_id, reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.post("/distances/compute", response_model=ComputeDistanceResM)
def compute_distance(account_id: int, reqm: ComputeDistanceReqM):
    resm = delis.compute_distance(account_id, reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@app.get("/distances")
def get_queries():
    return dbd.data
