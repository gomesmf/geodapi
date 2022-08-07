import errno
from typing import List
from .presenter import ComputeDistanceVM
from pydantic import BaseModel


class DistanceResultM(BaseModel):
    value: float
    unit: str
    text: str

class ComputeDistanceResM(BaseModel):
    distances: List[DistanceResultM] = None
    errmsg: str = None
    # detail: str = None

def compute_distance_view(vm: ComputeDistanceVM) -> ComputeDistanceResM:
    resm = ComputeDistanceResM(errmsg=vm.errmsg)
    # resm.detail = vm.detail

    if vm.result != None:
        drmlist = []
        for vmr in vm.result:
            drmlist.append(DistanceResultM(
                value=vmr["value"],
                unit=vmr["unit"],
                text=vmr["text"]
            ))
        resm.distances = drmlist

    return  resm
