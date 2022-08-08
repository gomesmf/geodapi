from pydantic import BaseModel

from .interactor import UpdateAccountUCI


class UpdateAccountReqM(BaseModel):
    email: str = None
    name: str = None
    password: str = None
    password_again: str = None

def update_account_controller(account_id: int, reqm: UpdateAccountReqM) -> UpdateAccountUCI:
    ucin = UpdateAccountUCI(
        account_id=account_id,
        email=reqm.email,
        name=reqm.name,
        password=reqm.password,
        password_again=reqm.password_again,
    )
    return ucin
