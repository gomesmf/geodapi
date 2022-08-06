from fastapi import FastAPI
from fastapi.responses import JSONResponse
from accounts.DeleteAccount.view import DeleteAccountResM

from accounts.web import (
    AccountsService,
    CreateAccountReqM,
    CreateAccountResM,
    GetAccountTypesResM
)
from accounts.inmemdb import get_dba

from fake import fake_password_hash

dba = get_dba()

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
        return JSONResponse(status_code=400, content=resm.dict())

    return resm
