from abc import ABC, abstractmethod

from deliveries.usecases.ComputeDistance.controller import ComputeDistanceReqM
from deliveries.usecases.ComputeDistance.view import ComputeDistanceResM
from deliveries.usecases.GetDistances.view import GetDistancesResM


class DeliveriesServiceInterface(ABC):
    @abstractmethod
    def compute_distance(self, account_id: int, reqm: ComputeDistanceReqM) -> ComputeDistanceResM:
        pass

    @abstractmethod
    def get_distances(self, account_id: int) -> GetDistancesResM:
        pass
