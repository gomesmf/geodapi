from datetime import datetime
from distances.entities import Address, Distance
from pydantic import BaseModel

def dist_between_text(orig: Address, dest: Address, dist: Distance):
    return f"The geodesic distance between '{orig.to_string()}' and '{dest.to_string()}' is {dist.value} {dist.unit}"

def datetime_formated(d: datetime) -> str:
    return d.strftime("%Y-%m-%d %H:%M:%S.%f")

class DistanceResultM(BaseModel):
    value: float
    unit: str
    text: str
