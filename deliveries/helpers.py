from typing import List
from .entities import Address, Distance
from .external import SearchServiceInterface, SearchResult, DistanceServiceInterface
from .data import DBDistancesInterface

class FakeSearchService(SearchServiceInterface):
    def search(self, addr: Address) -> SearchResult:
        return SearchResult(result={
            "lat": "12.3456",
            "lon": "65.4321"
        })

class FakeDistanceService(DistanceServiceInterface):
    def compute(self, origlat: float, origlon: float, destlat: float, destlon: float) -> List[Distance]:
        return [
            Distance(value=10.0, unit="km"),
            Distance(value=5.0, unit="miles")
        ]

class InMemoryDBDistances(DBDistancesInterface):
    def __init__(self) -> None:
        self.data = []

    def add_distance(self, account_id: int, orig: Address, origsres: SearchResult, dest: Address, destsres: SearchResult, dsres: List[Distance]) -> bool:
        self.data.append(
            {
                "account_id": account_id,
                "origin": orig,
                "origin_search_result": origsres,
                "destination": dest,
                "destination_search_result": destsres,
                "distance": dsres
            }
        )
        return True
