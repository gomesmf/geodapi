from datetime import datetime
from typing import List, Tuple
from deliveries.entities import Address, Distance
from deliveries.interfaces.external import SearchServiceInterface, SearchResult, DistanceServiceInterface
from deliveries.interfaces.data import DBDistancesInterface, DistanceResult

class FakeSearchService(SearchServiceInterface):
    def search(self, addr: Address) -> SearchResult:
        return SearchResult(result={
            "lat": "12.3456",
            "lon": "65.4321"
        })

class FakeDistanceService(DistanceServiceInterface):
    def compute(self, origlat: float, origlon: float, destlat: float, destlon: float) -> List[Distance]:
        return [
            Distance(value=10.0, unit="kilometers"),
            Distance(value=5.0, unit="miles")
        ]

class InMemoryDBDistances(DBDistancesInterface):
    def __init__(self) -> None:
        self.data = {"distances": {}}

    def add_distance(self, account_id: int, orig: Address, origsres: SearchResult, dest: Address, destsres: SearchResult, dsres: List[Distance], added_at: datetime) -> bool:
        if account_id not in self.data["distances"]:
            self.data["distances"][account_id] = []
        self.data["distances"][account_id].append(
            {
                "account_id": account_id,
                "origin": orig,
                "origin_search_result": origsres,
                "destination": dest,
                "destination_search_result": destsres,
                "distance": dsres,
                "added_at_timestamp": str(added_at.timestamp()),
                "added_at": added_at,
            }
        )
        return True

    def get_distances(self, account_id: int) -> Tuple[List[DistanceResult], bool]:
        drlist = []
        for r in self.data["distances"][account_id]:
            drlist.append(DistanceResult(
                origin=r["origin"],
                destination=r["destination"],
                distance=r["distance"],
                datetime=r["added_at"]
            ))

        return drlist, False

    def account_id_exists(self, account_id: int) -> bool:
        return account_id in self.data["distances"]

def get_inmemdbd():
    return InMemoryDBDistances()
