from unittest import main, TestCase

from distances.adapters.geo import GeopyDistanceService

class TestGeopyDistanceService(TestCase):
    def test_compute(self):
        ds = GeopyDistanceService()
        lat1 = "41.49008"
        lon1 = "-71.312796"
        lat2 = "41.499498"
        lon2 = "-81.695391"
        d = ds.compute(lat1, lon1, lat2, lon2)[0]
        self.assertAlmostEqual(round(866.4554329098687, 2), d.value)

        lat1 = "-23.7010955"
        lon1 = "-46.4144766"
        lat2 = "-23.6395801"
        lon2 = "-46.5139575"
        d = ds.compute(lat1, lon1, lat2, lon2)[0]
        self.assertAlmostEqual(round(12.222887706959588, 2), d.value)

if __name__ == '__main__':
    main()
