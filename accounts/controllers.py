from pydantic import BaseModel
from accounts.interactors import CreateAccountUCI

class CreateAccountReqM(BaseModel):
    type: str
    name: str
    email: str
    password: str

def create_account_controller(reqm: CreateAccountReqM) -> CreateAccountUCI:
    ucin =  CreateAccountUCI(reqm.type, reqm.name, reqm.email, reqm.password)
    return ucin
