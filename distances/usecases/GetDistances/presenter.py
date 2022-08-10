from typing import Dict, List
from distances.usecases.GetDistances.interactor import GetDistancesUCO

from distances.usecases.common import datetime_formated, dist_between_text

class GetDistancesVM:
    def __init__(self, result: List[Dict] = None, errmsg = None) -> None:
        self.result = result
        self.errmsg = errmsg

def get_distances_presenter(ucout: GetDistancesUCO) -> GetDistancesVM:
    if ucout.errmsg != None:
        return GetDistancesVM(errmsg=ucout.errmsg)

    vm = GetDistancesVM(result=[])

    for ucoutr in ucout.result:
        vmr = {}
        vmr["origin"] = ucoutr.origin.to_dict()
        vmr["destination"] = ucoutr.destination.to_dict()
        vmr["created_at"] = datetime_formated(ucoutr.datetime)

        vmr["distance"] = []
        for ucoutd in ucoutr.distance:
            vmr["distance"].append({
                "value": ucoutd.value,
                "unit": ucoutd.unit,
                "text": dist_between_text(ucoutr.origin, ucoutr.destination, ucoutd)
            })

        vm.result.append(vmr)

    return vm
