from typing import List
from pydantic import BaseModel

from distances.usecases.GetDistances.presenter import GetDistancesVM
from distances.usecases.common import DistanceResultM

class AddressCompletM(BaseModel):
    street: str
    house_number: int
    city: str
    country: str
    latitude: str
    longitude: str

class ResultM(BaseModel):
    origin: AddressCompletM
    destination: AddressCompletM
    created_at: str
    distance: List[DistanceResultM]

class GetDistancesResM(BaseModel):
    result: List[ResultM] = None
    errmsg: str = None

def get_distances_view(vm: GetDistancesVM) -> GetDistancesResM:
    if vm.errmsg != None:
        return GetDistancesResM(errmsg=vm.errmsg)

    rmlist = []
    for vmr in vm.result:
        drmlist = []
        for d in vmr["distance"]:
            drmlist.append(
                DistanceResultM(
                    value=d["value"],
                    unit=d["unit"],
                    text=d["text"],
                )
            )

        rmlist.append(
            ResultM(
                origin=AddressCompletM(
                    street=vmr["origin"]["street"],
                    house_number=vmr["origin"]["house_number"],
                    city=vmr["origin"]["city"],
                    country=vmr["origin"]["country"],
                    latitude=vmr["origin"]["latitude"],
                    longitude=vmr["origin"]["longitude"],
                ),
                destination=AddressCompletM(
                    street=vmr["destination"]["street"],
                    house_number=vmr["destination"]["house_number"],
                    city=vmr["destination"]["city"],
                    country=vmr["destination"]["country"],
                    latitude=vmr["destination"]["latitude"],
                    longitude=vmr["destination"]["longitude"],
                ),
                created_at=vmr["created_at"],
                distance=drmlist
            )
        )

    return GetDistancesResM(result=rmlist)
