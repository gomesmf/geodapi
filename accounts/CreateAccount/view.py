from typing import Optional
from pydantic import BaseModel

from .presenter import CreateAccountVM

class CreateAccountResM(BaseModel):
    id: Optional[int]
    errmsg: Optional[str]

def create_account_view(vm: CreateAccountVM) -> CreateAccountResM:
    return CreateAccountResM(id=vm.id, errmsg=vm.errmsg)

