from abc import ABC, abstractmethod
from typing import List

from deliveries.external import SearchResult
from .entities import Address, Distance

class DBDistancesInterface(ABC):
    @abstractmethod
    def add_distance(self, account_id: int, orig: Address, origsres: SearchResult, dest: Address, destsres: SearchResult, dsres: List[Distance]) -> bool:
        pass