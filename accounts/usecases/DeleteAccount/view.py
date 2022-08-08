from typing import Optional
from pydantic import BaseModel

from .presenter import DeleteAccountVM


class DeleteAccountResM(BaseModel):
    account_id: Optional[int] = None
    errmsg: Optional[str] = None

def delete_account_view(vm: DeleteAccountVM) -> DeleteAccountResM:
    return DeleteAccountResM(account_id=vm.account_id, errmsg=vm.errmsg)
