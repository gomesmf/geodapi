from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from .external import SearchResult
from deliveries.entities import Address, Distance

class DBDistancesInterface(ABC):
    @abstractmethod
    def add_distance(self, account_id: int, orig: Address, origsres: SearchResult, dest: Address, destsres: SearchResult, dsres: List[Distance], added_at: datetime) -> bool:
        pass
