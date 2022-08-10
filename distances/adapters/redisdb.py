from datetime import datetime
import os
from typing import List, Tuple
from distances.entities import Address, Distance
from distances.interfaces.data import DBDistancesInterface, DistanceResult
from distances.interfaces.external import SearchResult

from json import JSONEncoder, dumps, loads

import redis

class object_encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def address_encode(a: Address) -> str:
    return dumps(a, indent=2, cls=object_encoder)

def address_object_hook(obj) -> Address:
    return Address(
        street=obj["street"],
        house_number=obj["house_number"],
        city=obj["city"],
        country=obj["country"],
        latitude=obj["latitude"],
        longitude=obj["longitude"],
    )

def address_decode(ajson: str) -> Address:
    return loads(ajson, object_hook=address_object_hook)

def searchres_encode(sres: SearchResult):
    return dumps(sres, indent=2, cls=object_encoder)

def searchres_decode(sresjson: str) -> SearchResult:
    d = loads(sresjson)
    return SearchResult(result=d["result"], errmsg=d["errmsg"])

_datetime_format = "%Y-%m-%d %H:%M:%S.%f"

def datetime_encode(dt: datetime) -> str:
    return dt.strftime(_datetime_format)

def datetime_decode(dtstr: str) -> datetime:
    return datetime.strptime(dtstr, _datetime_format)

def distance_encode(d: Distance) -> str:
    return dumps(d, indent=2, cls=object_encoder)

def distance_object_hook(obj) -> Distance:
    return Distance(
        value=obj["value"],
        unit=obj["unit"],
    )

def distance_decode(djson: str) -> Distance:
    return loads(djson, object_hook=distance_object_hook)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

_k_distances = "distances"

def _n_distaccid(account_id: int) -> str:
    return f"{_k_distances}_{account_id}"

MAX_NUM_LAST_QUERIES = 10

class RedisDBDistances(DBDistancesInterface):
    def __init__(self, host: str = REDIS_HOST) -> None:
        self.rdb = redis.Redis(host=host, decode_responses=True)

    def _flush(self):
        self.rdb.flushall()

    def add_distance(self, account_id: int, orig: Address, origsres: SearchResult, dest: Address, destsres: SearchResult, dsres: List[Distance], added_at: datetime) -> bool:
        dist = {
            "account_id": account_id,
            "origin": address_encode(orig),
            "origin_search_result": searchres_encode(origsres),
            "destination": address_encode(dest),
            "destination_search_result": searchres_encode(destsres),
            "distances": [distance_encode(d) for d in dsres],
            "added_at": datetime_encode(added_at),
        }
        diststr = dumps(dist)
        self.rdb.lpush(_n_distaccid(account_id), diststr)
        self.rdb.save()
        return True

    def get_distances(self, account_id: int) -> Tuple[List[DistanceResult], bool]:
        res = []
        diststr_list = self.rdb.lrange(_n_distaccid(account_id), 0, MAX_NUM_LAST_QUERIES)

        for diststr in diststr_list:
            dist = loads(diststr)

            origin = address_decode(dist["origin"])
            destination = address_decode(dist["destination"])
            added_at = datetime_decode(dist["added_at"])

            distance = []
            for dstr in dist["distances"]:
                distance.append(distance_decode(dstr))

            res.append(DistanceResult(
                origin=origin,
                destination=destination,
                distance=distance,
                datetime=added_at
            ))

        return res, False

    def account_id_exists(self, account_id: int) -> bool:
        return self.rdb.exists(_n_distaccid(account_id))
