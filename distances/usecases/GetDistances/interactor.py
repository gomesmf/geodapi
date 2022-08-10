from typing import List
from distances.interfaces.data import DBDistancesInterface, DistanceResult

class GetDistancesUCI:
    def __init__(self, account_id: int) -> None:
        self.account_id = account_id

class GetDistancesUCO:
    def __init__(self, result: List[DistanceResult] = None, errmsg: str = None):
        self.result = result
        self.errmsg = errmsg

ERRMSG_ACCOUNT_NOT_FOUND = "Account not found"
ERRMSG_CANNOT_GET_DISTANCES = "Cannot get distances from database"

def get_distances_interactor(dbd: DBDistancesInterface, ucin: GetDistancesUCI) -> GetDistancesUCO:
    if not dbd.account_id_exists(ucin.account_id):
        return GetDistancesUCO(result=[])

    dres, err = dbd.get_distances(ucin.account_id)
    if err:
        return GetDistancesUCO(errmsg=ERRMSG_CANNOT_GET_DISTANCES)

    return GetDistancesUCO(result=dres)
