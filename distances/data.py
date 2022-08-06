from abc import ABC, abstractmethod
from .entities import Address

class DBDistancesInterface(ABC):
    @abstractmethod
    def add_distance(self, account_id: int, orig: Address, dest: Address) -> bool:
        pass
