from pydantic import BaseModel
from accounts.interactors import CreateAccountUCI

class CreateAccountRequestModel(BaseModel):
    type: str
    name: str
    email: str
    password: str

def create_account_controller(rm: CreateAccountRequestModel) -> CreateAccountUCI:
    ucin =  CreateAccountUCI(rm.type, rm.name, rm.email, rm.password)
    return ucin
