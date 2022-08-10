from pydantic import BaseModel

from distances.entities import Address

from .interactor import ComputeDistanceUCI

class AddressM(BaseModel):
    street: str
    house_number: int
    city: str
    country: str

class ComputeDistanceReqM(BaseModel):
    origin: AddressM
    destination: AddressM

def compute_distance_controller(account_id: int, reqm: ComputeDistanceReqM) -> ComputeDistanceUCI:
    ucin = ComputeDistanceUCI(
        account_id=account_id,
        origin=Address(
            street=reqm.origin.street,
            house_number=reqm.origin.house_number,
            city=reqm.origin.city,
            country=reqm.origin.country,
        ),
        destination=Address(
            street=reqm.destination.street,
            house_number=reqm.destination.house_number,
            city=reqm.destination.city,
            country=reqm.destination.country,
        )
    )
    return ucin
