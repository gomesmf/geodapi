from abc import ABC, abstractmethod

from typing import Dict, List

from deliveries.entities import Address, Distance

class SearchResult:
    def __init__(self, result: Dict = None, errmsg: str = None) -> None:
        self.result = result
        self.errmsg = errmsg

class SearchServiceInterface(ABC):
    @abstractmethod
    def search(self, addr: Address) -> SearchResult:
        pass

class DistanceServiceInterface(ABC):
    @abstractmethod
    def compute(self, origlat: float, origlon: float, destlat: float, destlon: float) -> List[Distance]:
        pass
