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
from distances.ComputeDistance.controller import ComputeDistanceReqM, compute_distance_controller
from distances.ComputeDistance.interactor import compute_distance_interactor
from distances.ComputeDistance.presenter import compute_distance_presenter
from distances.ComputeDistance.view import compute_distance_view
from distances.helpers import FakeDistanceService, FakeSearchService, InMemoryDBDistances


dba = get_inmemdba()

ph = fake_password_hash

app = FastAPI(description="Delivery Guy API")

acs = AccountsService(dba, ph)

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

dbd = InMemoryDBDistances()
ss = FakeSearchService()
ds = FakeDistanceService()

@app.post("/distances/compute")
def compute_distance(account_id: int, reqm: ComputeDistanceReqM):
    ucin = compute_distance_controller(account_id, reqm)
    ucout = compute_distance_interactor(acs, ss, ds, dbd, ucin)
    vm = compute_distance_presenter(ucout)
    resm = compute_distance_view(vm)
    return resm

@app.get("/distances")
def get_queries():
    return dbd.data
