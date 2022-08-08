from abc import ABC, abstractmethod

from deliveries.usecases.ComputeDistance.controller import ComputeDistanceReqM
from deliveries.usecases.ComputeDistance.view import ComputeDistanceResM


class DeliveriesServiceInterface(ABC):
    @abstractmethod
    def compute_distance(account_id: int, reqm: ComputeDistanceReqM) -> ComputeDistanceResM:
        pass
