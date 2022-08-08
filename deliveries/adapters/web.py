from accounts.interfaces.service import AccountsServiceInterface

from deliveries.interfaces.data import DBDistancesInterface
from deliveries.interfaces.external import DistanceServiceInterface, SearchServiceInterface
from deliveries.interfaces.service import DeliveriesServiceInterface

from deliveries.usecases.ComputeDistance.controller import ComputeDistanceReqM, compute_distance_controller
from deliveries.usecases.ComputeDistance.interactor import compute_distance_interactor
from deliveries.usecases.ComputeDistance.presenter import compute_distance_presenter
from deliveries.usecases.ComputeDistance.view import ComputeDistanceResM, compute_distance_view


from deliveries.usecases.GetDistances.controller import get_distances_controller
from deliveries.usecases.GetDistances.interactor import get_distances_interactor
from deliveries.usecases.GetDistances.presenter import get_distances_presenter
from deliveries.usecases.GetDistances.view import GetDistancesResM, get_distances_view


class DeliveriesService(DeliveriesServiceInterface):
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

    def get_distances(self, account_id: int) -> GetDistancesResM:
        ucin = get_distances_controller(account_id)
        ucout = get_distances_interactor(self.dbd, ucin)
        vm = get_distances_presenter(ucout)
        resm = get_distances_view(vm)
        return resm
