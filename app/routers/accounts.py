from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse

from accounts.auth import AccountM

from accounts.adapters.web import (
    DeleteAccountResM,
    UpdateAccountReqM,
    UpdateAccountResM
)
from accounts.usecases.CreateAccount.controller import CreateAccountReqM
from accounts.usecases.CreateAccount.view import CreateAccountResM

from app.dependencies import get_current_account, acs

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

@router.get("/me")
def get_my_account(current_account: AccountM = Depends(get_current_account)):
    return current_account

@router.delete("/me", response_model=DeleteAccountResM)
def delete_my_account(current_account: AccountM = Depends(get_current_account)):
    resm = acs.delete_account(current_account.account_id)

    if resm.errmsg:
        return JSONResponse(status_code=404, content=resm.dict())

    return resm

@router.put("/me", response_model=UpdateAccountResM)
def update_my_account(reqm: UpdateAccountReqM, current_account: AccountM = Depends(get_current_account)):
    resm = acs.update_account(current_account.account_id, reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@router.post("", response_model=CreateAccountResM)
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
