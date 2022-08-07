from typing import List, Tuple
from accounts.service import AccountsServiceInterface
from distances.entities import Address, Distance
from distances.data import DBDistancesInterface
from distances.external import SearchResult, SearchServiceInterface, DistanceServiceInterface

class ComputeDistanceUCI:
    def __init__(self, account_id: int, origin: Address, destination: Address) -> None:
        self.account_id = account_id
        self.origin = origin
        self.destination = destination

class ComputeDistanceUCO:
    def __init__(self, origin: Address = None, destination: Address = None, result: List[Distance] = None, errmsg: str = None, detail: str = None) -> None:
        self.origin = origin
        self.destination = destination
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

    origsres = ss.search(ucin.origin)
    if origsres.errmsg:
        return ComputeDistanceUCO(errmsg=ERRMSG_ORIGIN_NOT_FOUND, detail=origsres.errmsg)

    origlat, origlon = _get_latlon(origsres)
    if origlat == None or origlon == None:
        return ComputeDistanceUCO(errmsg=ERRMSG_ORIGIN_COORDINATES_NOT_FOUND)

    ucin.origin.latitude = origlat
    ucin.origin.longitude = origlon

    destsres = ss.search(ucin.destination)
    if destsres.errmsg:
        return ComputeDistanceUCO(errmsg=ERRMSG_DEST_NOT_FOUND, detail=destsres.errmsg)

    destlat, destlon = _get_latlon(destsres)
    if destlat == None or destlon == None:
        return ComputeDistanceUCO(errmsg=ERRMSG_DEST_COORDINATES_NOT_FOUND)

    ucin.destination.latitude = destlat
    ucin.destination.longitude = destlon

    dsres = ds.compute(origlat, origlon, destlat, destlon)
    if not dsres:
        return ComputeDistanceUCO(errmsg=ERRMSG_COULDNT_COMPUTE_DISTANCE)

    if not dbd.add_distance(ucin.account_id, ucin.origin, origsres, ucin.destination, destsres, dsres):
        return ComputeDistanceUCO(errmsg=ERRMSG_COULDNT_SAVE_RESULT)

    return ComputeDistanceUCO(origin=ucin.origin, destination=ucin.destination, result=dsres)
