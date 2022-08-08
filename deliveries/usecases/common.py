from datetime import datetime
from deliveries.entities import Address, Distance

def dist_between_text(orig: Address, dest: Address, dist: Distance):
    return f"The geodesic distance between '{orig.to_string()}' and '{dest.to_string()}' is {dist.value} {dist.unit}"

def datetime_formated(d: datetime) -> str:
    return d.strftime("%Y-%m-%d %H:%m:%S.%f")
