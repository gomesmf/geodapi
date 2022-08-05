from fastapi import FastAPI
from accounts.CreateAccount.controller import CreateAccountReqM, create_account_controller
from accounts.CreateAccount.interactor import create_account_interactor
from accounts.CreateAccount.presenter import create_account_presenter
from accounts.CreateAccount.view import create_account_view

from accounts.inmemdb import get_dba

from fake import fake_password_hash

dba = get_dba()

ph = fake_password_hash

app = FastAPI(description="Delivery Guy API")

@app.get("/accounts")
def get_accounts():
    return dba.data

@app.post("/accounts")
def create_account(reqm: CreateAccountReqM):
    ucin = create_account_controller(reqm)
    ucout = create_account_interactor(dba, ph, ucin)
    vm = create_account_presenter(ucout)
    resm = create_account_view(vm)
    return resm
