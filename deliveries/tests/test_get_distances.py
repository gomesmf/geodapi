from datetime import datetime
from unittest import main, TestCase
from unittest.mock import Mock

from deliveries.entities import Address, Distance
from deliveries.usecases.GetDistances.interactor import (
    ERRMSG_ACCOUNT_NOT_FOUND,
    ERRMSG_CANNOT_GET_DISTANCES,
    DistanceResult,
    GetDistancesUCI,
    GetDistancesUCO,
    get_distances_interactor
)

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
        self.assertEqual(ucout.errmsg, ERRMSG_ACCOUNT_NOT_FOUND)
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


if __name__ == "__main__":
    main()
