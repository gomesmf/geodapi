from pydantic import BaseModel
from .presenter import UpdateAccountVM


class UpdateAccountResM(BaseModel):
    errmsg: str = None

def update_account_view(vm: UpdateAccountVM) -> UpdateAccountResM:
    return UpdateAccountResM(errmsg=vm.errmsg)

