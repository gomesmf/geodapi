from datetime import datetime
from unittest import main, TestCase
from unittest.mock import Mock

from distances.adapters.web import GeodistanceService, ComputeDistanceReqM, ComputeDistanceResM
from distances.entities import Distance, Address
from distances.interfaces.data import DistanceResult
from distances.interfaces.external import SearchResult
from distances.usecases.ComputeDistance.controller import AddressM
from distances.usecases.GetDistances.view import GetDistancesResM

class TestComputeDistance(TestCase):
    def test_success(self):
        acs = Mock()
        acs.account_id_exists.return_value = True

        ss = Mock()
        ss.search.return_value = SearchResult(
            result={"lat": 0.0, "lon": 0.0}
        )

        ds = Mock()
        ds.compute.return_value = [
            Distance(value=1, unit="km"),
            Distance(value=2, unit="mi"),
        ]

        dbd = Mock()
        dbd.add_distance.return_value = True

        geods = GeodistanceService(acs, ss, ds, dbd)

        account_id = 1
        reqm = ComputeDistanceReqM(
            origin=AddressM(
                street="origin_street",
                house_number=111,
                city="origin_city",
                country="origin_country"
            ),
            destination=AddressM(
                street="destination_street",
                house_number=111,
                city="destination_city",
                country="destination_country"
            )
        )

        resm = geods.compute_distance(account_id, reqm)

        self.assertIsInstance(resm, ComputeDistanceResM)

class TestGetDistance(TestCase):
    def test_success(self):
        acs = Mock()
        ss = Mock()
        ds = Mock()

        dbd = Mock()
        dbd.account_id_exists.return_value = True
        dbd.get_distances.return_value = ([DistanceResult(
            origin=Address(
                street="origin_street",
                house_number=111,
                city="origin_city",
                country="origin_country",
                latitude="11.1111",
                longitude="22.2222"
            ),
            destination=Address(
                street="origin_street",
                house_number=111,
                city="origin_city",
                country="origin_country",
                latitude="33.3333",
                longitude="44.4444"
            ),
            distance=[Distance(value=1, unit="km")],
            datetime=datetime.now()
        )], False)

        geods = GeodistanceService(acs, ss, ds, dbd)

        account_id = 1
        resm = geods.get_distances(account_id)

        self.assertIsInstance(resm, GetDistancesResM)

if __name__ == "__main__":
    main()
