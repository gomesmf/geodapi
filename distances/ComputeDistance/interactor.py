from typing import Dict, List, Tuple
from accounts.service import AccountsServiceInterface
from distances.entities import Address
from distances.data import DBDistancesInterface
from distances.external import SearchResult, SearchServiceInterface, DistanceServiceInterface

class ComputeDistanceUCI:
    def __init__(self, account_id: int, orig: Address, dest: Address) -> None:
        self.account_id = account_id
        self.orig = orig
        self.dest = dest

class ComputeDistanceUCO:
    def __init__(self, result: List[Dict] = None, errmsg: str = None, detail: str = None) -> None:
        self.result = result
        self.errmsg = errmsg
        self.detail = detail

def _get_latlon(sres: SearchResult) -> Tuple[float, float]:
    lat = sres.result.get("lat")
    lon = sres.result.get("lon")
    return lat, lon

ERRMSG_ACCOUNT_NOT_FOUND = "Account not found"
ERRMSG_ORIGIN_NOT_FOUND = "Origin address not found"
ERRMSG_DEST_NOT_FOUND = "Destination address not found"
ERRMSG_ORIGIN_COORDINATES_NOT_FOUND = "Origin coordinates not found"
ERRMSG_DEST_COORDINATES_NOT_FOUND = "Destination coordinates not found"
ERRMSG_COULDNT_COMPUTE_DISTANCE = "Distance service could not compute distance between origin and destination"
ERRMSG_COULDNT_SAVE_RESULT = "Could not save result to database"

def compute_distance_interactor(
    acs: AccountsServiceInterface,
    ss: SearchServiceInterface,
    ds: DistanceServiceInterface,
    dbd: DBDistancesInterface,
    ucin: ComputeDistanceUCI) -> ComputeDistanceUCO:
    if not acs.account_id_exists(ucin.account_id):
        return ComputeDistanceUCO(errmsg=ERRMSG_ACCOUNT_NOT_FOUND)

    origsres = ss.search(ucin.orig)
    if origsres.errmsg:
        return ComputeDistanceUCO(errmsg=ERRMSG_ORIGIN_NOT_FOUND, detail=origsres.errmsg)

    origlat, origlon = _get_latlon(origsres)
    if origlat == None or origlon == None:
        return ComputeDistanceUCO(errmsg=ERRMSG_ORIGIN_COORDINATES_NOT_FOUND)

    destsres = ss.search(ucin.dest)
    if destsres.errmsg:
        return ComputeDistanceUCO(errmsg=ERRMSG_DEST_NOT_FOUND, detail=destsres.errmsg)

    destlat, destlon = _get_latlon(destsres)
    if destlat == None or destlon == None:
        return ComputeDistanceUCO(errmsg=ERRMSG_DEST_COORDINATES_NOT_FOUND)

    dsres = ds.compute(origlat, origlon, destlat, destlon)
    if not dsres:
        return ComputeDistanceUCO(errmsg=ERRMSG_COULDNT_COMPUTE_DISTANCE)

    if not dbd.add_distance(ucin.account_id, ucin.orig, origsres, ucin.dest, destsres):
        return ComputeDistanceUCO(errmsg=ERRMSG_COULDNT_SAVE_RESULT)

    return ComputeDistanceUCO(result=dsres)
