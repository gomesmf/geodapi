from abc import ABC, abstractmethod

from distances.usecases.ComputeDistance.controller import ComputeDistanceReqM
from distances.usecases.ComputeDistance.view import ComputeDistanceResM
from distances.usecases.GetDistances.view import GetDistancesResM


class GeodistanceServiceInterface(ABC):
    @abstractmethod
    def compute_distance(self, account_id: int, reqm: ComputeDistanceReqM) -> ComputeDistanceResM:
        pass

    @abstractmethod
    def get_distances(self, account_id: int) -> GetDistancesResM:
        pass
