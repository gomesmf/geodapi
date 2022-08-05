from pydantic import BaseModel
from .interactor import CreateAccountUCI

class CreateAccountReqM(BaseModel):
    type: str
    name: str
    email: str
    password: str

def create_account_controller(reqm: CreateAccountReqM) -> CreateAccountUCI:
    ucin =  CreateAccountUCI(type=reqm.type, name=reqm.name, email=reqm.email, password=reqm.password)
    return ucin
