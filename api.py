from fastapi import FastAPI
from accounts.CreateAccount.controller import CreateAccountReqM, create_account_controller
from accounts.CreateAccount.interactor import create_account_interactor
from accounts.CreateAccount.presenter import create_account_presenter
from accounts.CreateAccount.view import create_account_view
from accounts.GetAccountTypes.controller import get_account_types_controller
from accounts.GetAccountTypes.presenter import get_account_types_presenter
from accounts.GetAccountTypes.view import get_account_types_view

from accounts.inmemdb import get_dba

from fake import fake_password_hash

dba = get_dba()

ph = fake_password_hash

app = FastAPI(description="Delivery Guy API")

@app.get("/accounts")
def get_accounts():
    return dba.data

@app.get("/accounts/new")
def get_accounts():
    ucout = get_account_types_controller()
    vm = get_account_types_presenter(ucout)
    resm = get_account_types_view(vm)
    return resm

@app.post("/accounts")
def create_account(reqm: CreateAccountReqM):
    ucin = create_account_controller(reqm)
    ucout = create_account_interactor(dba, ph, ucin)
    vm = create_account_presenter(ucout)
    resm = create_account_view(vm)
    return resm
