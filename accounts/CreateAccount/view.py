from typing import Optional
from pydantic import BaseModel

from .presenter import CreateAccountVM

class CreateAccountResM(BaseModel):
    id: Optional[int]
    errmsg: Optional[str]

def create_account_view(vm: CreateAccountVM):
    resm = CreateAccountResM()
    if vm.errmsg:
        resm.errmsg = vm.errmsg
    if vm.id:
        resm.id = vm.id
    return resm
