from unittest import main, TestCase
from unittest.mock import Mock
from distances.ComputeDistance.interactor import (
    ERRMSG_ACCOUNT_NOT_FOUND,
    ERRMSG_COULDNT_COMPUTE_DISTANCE,
    ERRMSG_COULDNT_SAVE_RESULT,
    ERRMSG_ORIGIN_COORDINATES_NOT_FOUND,
    ERRMSG_ORIGIN_NOT_FOUND,
    ComputeDistanceUCI,
    ComputeDistanceUCO,
    SearchResult,
    compute_distance_interactor
)

class TestController(TestCase):
    pass

class TestInteractor(TestCase):
    def test_success(self):
        account_id = 1
        origaddr = Mock()
        destaddr = Mock()

        ucin = ComputeDistanceUCI(
            account_id=account_id,
            orig=origaddr,
            dest=destaddr
        )

        acs = Mock()
        acs.account_id_exists.return_value = True

        ss = Mock()
        ss.search.return_value = SearchResult(
            result={"lat": 0.0, "lon": 0.0}
        )

        ds = Mock()
        ds.compute.return_value = [
            {"unit": "kilometers", "value": 0.0},
            {"unit": "miles", "value": 0.0}
        ]

        dbd = Mock()
        dbd.add_distance.return_value = True

        ucout = compute_distance_interactor(acs, ss, ds, dbd, ucin)

        self.assertIsInstance(ucout, ComputeDistanceUCO)
        self.assertIsNotNone(ucout.result)
        self.assertEqual(acs.account_id_exists.call_count, 1)
        self.assertEqual(ss.search.call_count, 2)
        self.assertEqual(ds.compute.call_count, 1)
        self.assertEqual(dbd.add_distance.call_count, 1)

    def test_orig_not_found(self):
        account_id = 1
        origaddr = Mock()
        destaddr = Mock()

        ucin = ComputeDistanceUCI(
            account_id=account_id,
            orig=origaddr,
            dest=destaddr
        )

        acs = Mock()
        acs.account_id_exists.return_value = True

        ss = Mock()
        SRES_ERRMSG = "sres_errmsg"
        ss.search.return_value = SearchResult(
            errmsg=SRES_ERRMSG
        )

        ds = Mock()
        ds.compute.return_value = [
            {"unit": "kilometers", "value": 0.0},
            {"unit": "miles", "value": 0.0}
        ]

        dbd = Mock()
        dbd.add_distance.return_value = True

        ucout = compute_distance_interactor(acs, ss, ds, dbd, ucin)

        self.assertIsInstance(ucout, ComputeDistanceUCO)
        self.assertEqual(acs.account_id_exists.call_count, 1)
        self.assertEqual(ss.search.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_ORIGIN_NOT_FOUND)
        self.assertEqual(ucout.detail, SRES_ERRMSG)
        self.assertEqual(ds.compute.call_count, 0)
        self.assertEqual(dbd.add_distance.call_count, 0)

    def test_dest_not_found(self):
        pass

    def test_orig_latlon_not_found(self):
        account_id = 1
        origaddr = Mock()
        destaddr = Mock()

        ucin = ComputeDistanceUCI(
            account_id=account_id,
            orig=origaddr,
            dest=destaddr
        )

        acs = Mock()
        acs.account_id_exists.return_value = True

        ss = Mock()
        ss.search.return_value = SearchResult(
            result={}
        )

        ds = Mock()
        ds.compute.return_value = [
            {"unit": "kilometers", "value": 0.0},
            {"unit": "miles", "value": 0.0}
        ]

        dbd = Mock()
        dbd.add_distance.return_value = True

        ucout = compute_distance_interactor(acs, ss, ds, dbd, ucin)

        self.assertIsInstance(ucout, ComputeDistanceUCO)
        self.assertEqual(acs.account_id_exists.call_count, 1)
        self.assertEqual(ss.search.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_ORIGIN_COORDINATES_NOT_FOUND)
        self.assertEqual(ds.compute.call_count, 0)
        self.assertEqual(dbd.add_distance.call_count, 0)

    def test_dest_latlon_not_found(self):
        pass

    def test_cannot_compute_distance(self):
        account_id = 1
        origaddr = Mock()
        destaddr = Mock()

        ucin = ComputeDistanceUCI(
            account_id=account_id,
            orig=origaddr,
            dest=destaddr
        )

        acs = Mock()
        acs.account_id_exists.return_value = True

        ss = Mock()
        ss.search.return_value = SearchResult(
            result={"lat": 0.0, "lon": 0.0}
        )

        ds = Mock()
        ds.compute.return_value = []

        dbd = Mock()
        dbd.add_distance.return_value = True

        ucout = compute_distance_interactor(acs, ss, ds, dbd, ucin)

        self.assertIsInstance(ucout, ComputeDistanceUCO)
        self.assertEqual(acs.account_id_exists.call_count, 1)
        self.assertEqual(ss.search.call_count, 2)
        self.assertEqual(ds.compute.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_COULDNT_COMPUTE_DISTANCE)
        self.assertEqual(dbd.add_distance.call_count, 0)

    def test_cannot_add_distance(self):
        account_id = 1
        origaddr = Mock()
        destaddr = Mock()

        ucin = ComputeDistanceUCI(
            account_id=account_id,
            orig=origaddr,
            dest=destaddr
        )

        acs = Mock()
        acs.account_id_exists.return_value = True

        ss = Mock()
        ss.search.return_value = SearchResult(
            result={"lat": 0.0, "lon": 0.0}
        )

        ds = Mock()
        ds.compute.return_value = [
            {"unit": "kilometers", "value": 0.0},
            {"unit": "miles", "value": 0.0}
        ]

        dbd = Mock()
        dbd.add_distance.return_value = False

        ucout = compute_distance_interactor(acs, ss, ds, dbd, ucin)

        self.assertIsInstance(ucout, ComputeDistanceUCO)
        self.assertEqual(acs.account_id_exists.call_count, 1)
        self.assertEqual(ss.search.call_count, 2)
        self.assertEqual(ds.compute.call_count, 1)
        self.assertEqual(dbd.add_distance.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_COULDNT_SAVE_RESULT)

    def test_account_id_not_exist(self):
        account_id = 1
        origaddr = Mock()
        destaddr = Mock()

        ucin = ComputeDistanceUCI(
            account_id=account_id,
            orig=origaddr,
            dest=destaddr
        )

        acs = Mock()
        acs.account_id_exists.return_value = False

        ss = Mock()
        ss.search.return_value = SearchResult(
            result={"lat": 0.0, "lon": 0.0}
        )

        ds = Mock()
        ds.compute.return_value = [
            {"unit": "kilometers", "value": 0.0},
            {"unit": "miles", "value": 0.0}
        ]

        dbd = Mock()
        dbd.add_distance.return_value = True

        ucout = compute_distance_interactor(acs, ss, ds, dbd, ucin)

        self.assertIsInstance(ucout, ComputeDistanceUCO)
        self.assertEqual(acs.account_id_exists.call_count, 1)
        self.assertEqual(ucout.errmsg, ERRMSG_ACCOUNT_NOT_FOUND)
        self.assertEqual(ss.search.call_count, 0)
        self.assertEqual(ds.compute.call_count, 0)
        self.assertEqual(dbd.add_distance.call_count, 0)

class TestPresenter(TestCase):
    pass

class TestView(TestCase):
    pass

if __name__ == "__main__":
    main()
