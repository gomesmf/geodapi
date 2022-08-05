from fastapi import FastAPI

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

@app.get("/accounts")
def get_accounts():
    return dba.data

@app.get("/accounts/new", response_model=GetAccountTypesResM)
def get_accounts():
    acs = AccountsService()
    return acs.get_account_types()

@app.post("/accounts", response_model=CreateAccountResM)
def create_account(reqm: CreateAccountReqM):
    acs = AccountsService()
    resm = acs.create_account(dba, ph, reqm)
    return resm
