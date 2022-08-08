from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple

from .external import SearchResult
from deliveries.entities import Address, Distance

class DistanceResult:
    def __init__(self, origin: Address, destination: Address, distance: List[Distance], datetime: datetime) -> None:
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.datetime = datetime

class DBDistancesInterface(ABC):
    @abstractmethod
    def add_distance(self, account_id: int, orig: Address, origsres: SearchResult, dest: Address, destsres: SearchResult, dsres: List[Distance], added_at: datetime) -> bool:
        pass

    @abstractmethod
    def get_distances(self, account_id: int) -> Tuple[List[DistanceResult], bool]:
        pass

    @abstractmethod
    def account_id_exists(self, account_id: int) -> bool:
        pass
