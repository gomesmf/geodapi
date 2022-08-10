from accounts.interfaces.service import AccountsServiceInterface

from distances.interfaces.data import DBDistancesInterface
from distances.interfaces.external import DistanceServiceInterface, SearchServiceInterface
from distances.interfaces.service import GeodistanceServiceInterface

from distances.usecases.ComputeDistance.controller import ComputeDistanceReqM, compute_distance_controller
from distances.usecases.ComputeDistance.interactor import compute_distance_interactor
from distances.usecases.ComputeDistance.presenter import compute_distance_presenter
from distances.usecases.ComputeDistance.view import ComputeDistanceResM, compute_distance_view


from distances.usecases.GetDistances.controller import get_distances_controller
from distances.usecases.GetDistances.interactor import get_distances_interactor
from distances.usecases.GetDistances.presenter import get_distances_presenter
from distances.usecases.GetDistances.view import GetDistancesResM, get_distances_view


class GeodistanceService(GeodistanceServiceInterface):
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
