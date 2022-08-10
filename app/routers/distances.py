from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from accounts.auth import AccountM

from distances.usecases.ComputeDistance.controller import ComputeDistanceReqM
from distances.usecases.ComputeDistance.view import ComputeDistanceResM
from distances.usecases.GetDistances.view import GetDistancesResM

from ..dependencies import get_current_account, geods

router = APIRouter(
    prefix="/distances",
    tags=["distances"],
)

@router.post("", response_model=ComputeDistanceResM)
def compute_distance(reqm: ComputeDistanceReqM, current_account: AccountM = Depends(get_current_account)):
    resm = geods.compute_distance(current_account.account_id, reqm)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm

@router.get("", response_model=GetDistancesResM)
def get_distances(current_account: AccountM = Depends(get_current_account)):
    resm = geods.get_distances(current_account.account_id)

    if resm.errmsg:
        return JSONResponse(status_code=400, content=resm.dict())

    return resm
