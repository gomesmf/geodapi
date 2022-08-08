from accounts.service import AccountsServiceInterface

from deliveries.interfaces.data import DBDistancesInterface
from deliveries.interfaces.external import DistanceServiceInterface, SearchServiceInterface
from deliveries.interfaces.service import DeliveriesServiceInterface

from deliveries.usecases.ComputeDistance.controller import ComputeDistanceReqM, compute_distance_controller
from deliveries.usecases.ComputeDistance.interactor import compute_distance_interactor
from deliveries.usecases.ComputeDistance.presenter import compute_distance_presenter
from deliveries.usecases.ComputeDistance.view import ComputeDistanceResM, compute_distance_view


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
