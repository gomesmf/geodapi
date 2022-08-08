from typing import Dict, List
from deliveries.entities import Address, Distance

from .interactor import ComputeDistanceUCO

from deliveries.usecases.common import dist_between_text

class ComputeDistanceVM:
    def __init__(self, result: List[Dict] = None, errmsg: str = None, detail: str = None) -> None:
        self.result = result
        self.errmsg = errmsg
        self.detail = detail

def compute_distance_presenter(ucout: ComputeDistanceUCO) -> ComputeDistanceVM:
    vm = ComputeDistanceVM(errmsg=ucout.errmsg, detail=ucout.detail)

    if ucout.result != None:
        vmrlist = []
        for d in ucout.result:
            vmrlist.append({
                "value": d.value,
                "unit": d.unit,
                "text": dist_between_text(ucout.origin, ucout.destination, d)
            })
        vm.result = vmrlist

    return vm
