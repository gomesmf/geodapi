from unittest import main, TestCase
from unittest.mock import Mock

from datetime import datetime

from deliveries.entities import Address, Distance
from deliveries.usecases.GetDistances.controller import get_distances_controller
from deliveries.usecases.GetDistances.interactor import (
    ERRMSG_CANNOT_GET_DISTANCES,
    DistanceResult,
    GetDistancesUCI,
    GetDistancesUCO,
    get_distances_interactor
)
from deliveries.usecases.GetDistances.presenter import GetDistancesVM, get_distances_presenter
from deliveries.usecases.GetDistances.view import AddressCompletM, GetDistancesResM, ResultM, get_distances_view
from deliveries.usecases.common import datetime_formated, dist_between_text

class TestInteractor(TestCase):
    def test_success(self):
        ucin = GetDistancesUCI(account_id=1)

        dbd = Mock()
        dbd.account_id_exists.return_value = True
        dbd.get_distances.return_value = (
            [DistanceResult(
                origin=Address(),
                destination=Address(),
                distance=[Distance(value=1, unit="km")],
                datetime=datetime.now()
            )],
            False
        )
        ucout = get_distances_interactor(dbd, ucin)

        self.assertIsInstance(ucout, GetDistancesUCO)
        self.assertEqual(dbd.account_id_exists.call_count, 1)
        self.assertEqual(dbd.get_distances.call_count, 1)

    def test_account_not_found(self):
        ucin = GetDistancesUCI(account_id=1)

        dbd = Mock()
        dbd.account_id_exists.return_value = False
        ucout = get_distances_interactor(dbd, ucin)

        self.assertIsInstance(ucout, GetDistancesUCO)
        self.assertEqual(dbd.account_id_exists.call_count, 1)
        self.assertEqual(ucout.result, [])
        self.assertEqual(dbd.get_distances.call_count, 0)

    def test_success(self):
        ucin = GetDistancesUCI(account_id=1)

        dbd = Mock()
        dbd.account_id_exists.return_value = True
        dbd.get_distances.return_value = (
            [DistanceResult(
                origin=Address(),
                destination=Address(),
                distance=[Distance(value=1, unit="km")],
                datetime=datetime.now()
            )],
            True
        )
        ucout = get_distances_interactor(dbd, ucin)

        self.assertIsInstance(ucout, GetDistancesUCO)
        self.assertEqual(dbd.account_id_exists.call_count, 1)
        self.assertEqual(dbd.get_distances.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_CANNOT_GET_DISTANCES)

class TestController(TestCase):
    def test_success(self):
        ucin = get_distances_controller(account_id=1)

        self.assertIsInstance(ucin, GetDistancesUCI)

def _ucout(errmsg = None):
    result =[
        DistanceResult(
            origin=Address(
                street="turquia",
                house_number=111,
                city="ribeirao pires",
                country="brasil",
                latitude="11.1111",
                longitude="22.2222"
            ),
            destination=Address(
                street="siria",
                house_number=222,
                city="maua",
                country="italia",
                latitude="33.3333",
                longitude="44.4444"
            ),
            distance=[Distance(value=1, unit="km")],
            datetime=datetime(2022, 8, 5, 10, 0, 0, 0))
    ]

    if errmsg != None:
        return GetDistancesUCO(errmsg=errmsg)

    return GetDistancesUCO(result=result)

class TestPresenter(TestCase):
    def test_success(self):
        ucout = _ucout()

        vm = get_distances_presenter(ucout)

        self.assertIsInstance(vm, GetDistancesVM)
        self.assertEqual(len(vm.result), len(ucout.result))
        for i in range(len(vm.result)):
            vmr = vm.result[i]
            ucoutr = ucout.result[i]

            self.assertDictEqual(vmr["origin"], {
                "street": ucoutr.origin.street,
                "house_number": ucoutr.origin.house_number,
                "city": ucoutr.origin.city,
                "country": ucoutr.origin.country,
                "latitude": ucoutr.origin.latitude,
                "longitude": ucoutr.origin.longitude,
            })
            self.assertDictEqual(vmr["destination"], {
                "street": ucoutr.destination.street,
                "house_number": ucoutr.destination.house_number,
                "city": ucoutr.destination.city,
                "country": ucoutr.destination.country,
                "latitude": ucoutr.destination.latitude,
                "longitude": ucoutr.destination.longitude,
            })
            self.assertEqual(vmr["created_at"], datetime_formated(ucoutr.datetime))

            self.assertEqual(len(vmr["distance"]), len(ucoutr.distance))
            for j in range(len(vmr["distance"])):
                vmrdj = vmr["distance"][j]
                ucoutrdj = ucoutr.distance[j]
                self.assertDictEqual(vmrdj, {
                    "value": ucoutrdj.value,
                    "unit": ucoutrdj.unit,
                    "text": dist_between_text(ucoutr.origin, ucoutr.destination, ucoutrdj)
                })

    def test_errmsg(self):
        ucout = _ucout("errmsg")

        vm = get_distances_presenter(ucout)

        self.assertIsInstance(vm, GetDistancesVM)
        self.assertEqual(vm.errmsg, ucout.errmsg)
        self.assertIsNone(vm.result)

class TestView(TestCase):
    def test_success(self):
        vm = GetDistancesVM(result=[{
            "origin": {
                "street": "origin_street",
                "house_number": 111,
                "city": "origin_city",
                "country": "origin_country",
                "latitude": "origin_latitude",
                "longitude": "origin_longitude",
            },
            "destination": {
                "street": "destination_street",
                "house_number": 222,
                "city": "destination_city",
                "country": "destination_country",
                "latitude": "destination_latitude",
                "longitude": "destination_longitude",
            },
            "created_at": "2022-05-10 12:52:33.222222",
            "distance": [
                {
                    "value": 1,
                    "unit": "km",
                    "text": "the distance..."
                }
            ]
        }])

        resm = get_distances_view(vm)

        self.assertIsInstance(resm, GetDistancesResM)
        self.assertEqual(len(resm.result), len(vm.result))

        for i in range(len(resm.result)):
            resmri = resm.result[i]
            self.assertIsInstance(resmri, ResultM)

    def test_errmsg(self):
        vm = GetDistancesVM(errmsg="errmsg")

        resm = get_distances_view(vm)

        self.assertIsInstance(resm, GetDistancesResM)
        self.assertEqual(resm.errmsg, vm.errmsg)
        self.assertIsNone(resm.result)

if __name__ == "__main__":
    main()
