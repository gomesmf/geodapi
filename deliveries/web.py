from accounts.service import AccountsServiceInterface

from .data import DBDistancesInterface
from .external import DistanceServiceInterface, SearchServiceInterface
from .service import DeliveriesServiceInterface

from .ComputeDistance.controller import ComputeDistanceReqM, compute_distance_controller
from .ComputeDistance.interactor import compute_distance_interactor
from .ComputeDistance.presenter import compute_distance_presenter
from .ComputeDistance.view import ComputeDistanceResM, compute_distance_view


class DelieveriesService(DeliveriesServiceInterface):
    def __init__(self, acs: AccountsServiceInterface, ss: SearchServiceInterface, ds: DistanceServiceInterface, dbd: DBDistancesInterface) -> None:
        self.acs = acs
        self.ss = ss
        self.ds = ds
        self.dbd = dbd

    def compute_distance(self, account_id: int, reqm: ComputeDistanceReqM) -> ComputeDistanceResM:
        ucin = compute_distance_controller(account_id, reqm)
        ucout = compute_distance_interactor(self.acs, self.ss, self.ds, self.dbd, ucin)
        vm = compute_distance_presenter(ucout)
        resm = compute_distance_view(vm)
        return resm
