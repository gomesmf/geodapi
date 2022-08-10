from datetime import datetime
import os
from unittest import main, TestCase, skipIf
from deliveries.adapters.redisdb import (
    RedisDBDistances,
    address_decode,
    address_encode,
    datetime_decode,
    datetime_encode,
    distance_decode,
    distance_encode,
    searchres_decode,
    searchres_encode
)
from deliveries.entities import Address, Distance
from deliveries.interfaces.data import DistanceResult
from deliveries.interfaces.external import SearchResult

@skipIf(os.getenv("SKIP_TEST_REDISDB") == None, "must have redis-server running")
class TestRedisDBDeliveries(TestCase):
    def test_address_encode(self):
        addr = Address(
            street="av miguel prisco",
            house_number=111,
            city="rib pires",
            country="Brazil",
            latitude="23.3456",
            longitude="23.3456"
        )

        addrjson = address_encode(addr)
        self.assertIsInstance(addrjson, str)

    def test_address_decode(self):
        addr = Address(
            street="av miguel prisco",
            house_number=111,
            city="rib pires",
            country="Brazil",
            latitude="23.3456",
            longitude="23.3456"
        )

        addrjson = address_encode(addr)
        self.assertIsInstance(addrjson, str)

        addrobj_got = address_decode(addrjson)

        self.assertIsInstance(addrobj_got, Address)
        self.assertEqual(addrobj_got.street, addr.street)
        self.assertEqual(addrobj_got.house_number, addr.house_number)
        self.assertEqual(addrobj_got.city, addr.city)
        self.assertEqual(addrobj_got.country, addr.country)
        self.assertEqual(addrobj_got.latitude, addr.latitude)
        self.assertEqual(addrobj_got.longitude, addr.longitude)

    def test_searchres_encode(self):
        sres = SearchResult(
            result={"key": "value"},
            errmsg="errmsg"
        )

        sresjson = searchres_encode(sres)
        self.assertIsInstance(sresjson, str)

    def test_searchres_decode(self):
        sres = SearchResult(
            result={"key": "value"},
            errmsg="errmsg"
        )

        sresjson = searchres_encode(sres)
        self.assertIsInstance(sresjson, str)

        sresobj_got = searchres_decode(sresjson)

        self.assertIsInstance(sresobj_got, SearchResult)
        self.assertEqual(sresobj_got.errmsg, sres.errmsg)

    def test_datetime_encode(self):
        dt = datetime(2022, 8, 9, 17, 42, 45, 753153)
        dtstr = datetime_encode(dt)
        self.assertEqual(dtstr, "2022-08-09 17:42:45.753153")

    def test_datetime_decode(self):
        dtstr = "2022-08-09 17:42:45.753153"
        dt = datetime_decode(dtstr)
        dt_expected = datetime(2022, 8, 9, 17, 42, 45, 753153)
        self.assertEqual(dt, dt_expected)

    def test_distance_encode(self):
        d = Distance(value=1.22, unit="km")
        dstr = distance_encode(d)
        self.assertIsInstance(dstr, str)

    def test_result_encode(self):
        d = Distance(value=1.22, unit="km")
        dstr = distance_encode(d)
        self.assertIsInstance(dstr, str)

        d_got = distance_decode(dstr)
        self.assertIsInstance(d_got, Distance)
        self.assertEqual(d_got.value, d.value)
        self.assertEqual(d_got.unit, d.unit)

    def test_add_distance(self):
        dbd = RedisDBDistances()
        dbd._flush()

        account_id = 11
        origaddr = Address(
            street="av miguel prisco",
            house_number=111,
            city="rib pires",
            country="Brazil",
            latitude="23.3456",
            longitude="23.3456"
        )
        destaddr = Address(
            street="av miguel prisco",
            house_number=222,
            city="maua",
            country="Brazil",
            latitude="12.3456",
            longitude="12.3456"
        )
        origsres = SearchResult(
            result={"lat": "12.3456", "lon": "12.3456"}
        )
        destsres = SearchResult(
            result={"lat": "12.3456", "lon": "12.3456"}
        )
        added_at = datetime(2022, 8, 9, 17, 42, 45, 753153)
        dsres = [
            Distance(value=16, unit="kilometers"),
            Distance(value=10, unit="miles"),
        ]

        dbd.add_distance(account_id, origaddr, origsres, destaddr, destsres, dsres, added_at)

    def test_get_distance(self):
        dbd = RedisDBDistances()
        dbd._flush()

        account_id = 11
        origaddr = Address(
            street="av miguel prisco",
            house_number=111,
            city="rib pires",
            country="Brazil",
            latitude="23.3456",
            longitude="23.3456"
        )
        destaddr = Address(
            street="av miguel prisco",
            house_number=222,
            city="maua",
            country="Brazil",
            latitude="12.3456",
            longitude="12.3456"
        )
        origsres = SearchResult(
            result={"lat": "12.3456", "lon": "12.3456"}
        )
        destsres = SearchResult(
            result={"lat": "12.3456", "lon": "12.3456"}
        )
        added_at = datetime(2022, 8, 9, 17, 42, 45, 753153)
        dsres = [
            Distance(value=16, unit="kilometers"),
            Distance(value=10, unit="miles"),
        ]

        dbd.add_distance(account_id, origaddr, origsres, destaddr, destsres, dsres, added_at)

        drlist, err = dbd.get_distances(account_id)
        self.assertFalse(err)
        self.assertEqual(len(drlist), 1)
        for dr in drlist:
            self.assertIsInstance(dr, DistanceResult)

    def test_account_id_exists(self):
        dbd = RedisDBDistances()
        dbd._flush()

        account_id = 11
        origaddr = Address(
            street="av miguel prisco",
            house_number=111,
            city="rib pires",
            country="Brazil",
            latitude="23.3456",
            longitude="23.3456"
        )
        destaddr = Address(
            street="av miguel prisco",
            house_number=222,
            city="maua",
            country="Brazil",
            latitude="12.3456",
            longitude="12.3456"
        )
        origsres = SearchResult(
            result={"lat": "12.3456", "lon": "12.3456"}
        )
        destsres = SearchResult(
            result={"lat": "12.3456", "lon": "12.3456"}
        )
        added_at = datetime(2022, 8, 9, 17, 42, 45, 753153)
        dsres = [
            Distance(value=16, unit="kilometers"),
            Distance(value=10, unit="miles"),
        ]

        dbd.add_distance(account_id, origaddr, origsres, destaddr, destsres, dsres, added_at)

        self.assertTrue(dbd.account_id_exists(account_id))

if __name__ == "__main__":
    main()
