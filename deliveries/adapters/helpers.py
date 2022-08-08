from datetime import datetime
from typing import List
from deliveries.entities import Address, Distance
from deliveries.interfaces.external import SearchServiceInterface, SearchResult, DistanceServiceInterface
from deliveries.interfaces.data import DBDistancesInterface

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
                "added_at": str(added_at.strftime("%Y-%m-%d %H:%m:%S.%f"))
            }
        )
        return True

    def get_distances(self, account_id: int):
        return self.data["distances"][account_id]

def get_inmemdbd():
    return InMemoryDBDistances()
