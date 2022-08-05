from fastapi import FastAPI
from accounts.controllers import CreateAccountReqM, create_account_controller
from accounts.interactors import create_account_interactor
from accounts.presenters import create_account_presenter
from accounts.views import create_account_view

from fake import get_dba, fake_password_hash

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
