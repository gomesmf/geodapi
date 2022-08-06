from pydantic import BaseModel

from accounts.UpdateAccount.interactor import UpdateAccountUCI


class UpdateAccountReqM(BaseModel):
    account_id: int
    email: str = None
    name: str = None
    password: str = None
    password_again: str = None

def update_account_controller(reqm: UpdateAccountReqM) -> UpdateAccountUCI:
    ucin = UpdateAccountUCI(
        account_id=reqm.account_id,
        email=reqm.email,
        name=reqm.name,
        password=reqm.password,
        password_again=reqm.password_again,
    )
    return ucin
