from pydantic import BaseModel
from .interactor import CreateAccountUCI

class CreateAccountReqM(BaseModel):
    # type: str
    name: str
    username: str
    email: str
    password: str

def create_account_controller(reqm: CreateAccountReqM) -> CreateAccountUCI:
    ucin =  CreateAccountUCI(type="DELIVERYGUY", name=reqm.name, email=reqm.email, password=reqm.password, username=reqm.username)
    return ucin
