from abc import ABC, abstractmethod

from deliveries.ComputeDistance.controller import ComputeDistanceReqM
from deliveries.ComputeDistance.view import ComputeDistanceResM


class DeliveriesServiceInterface(ABC):
    @abstractmethod
    def compute_distance(account_id: int, reqm: ComputeDistanceReqM) -> ComputeDistanceResM:
        pass
