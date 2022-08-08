from deliveries.entities import Distance
from deliveries.interfaces.external import DistanceServiceInterface

from geopy import distance

class GeopyDistanceService(DistanceServiceInterface):
    def compute(self, lat1: str, lon1: str, lat2: str, lon2: str):
        point1 = (float(lat1), float(lon1))
        point2 = (float(lat2), float(lon2))

        geo_dist = distance.distance(point1, point2)

        res = [
            # Distance(round(geo_dist.meters, 2), "meters"),
            Distance(round(geo_dist.kilometers, 2), "kilometers"),
            Distance(round(geo_dist.miles, 2), "miles"),
        ]

        return res
