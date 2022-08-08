import os
from unittest import main, TestCase

from deliveries.adapters.nominatim import _search, _search_params

def avoid_heavy_use():
    return os.environ.get("SKIP_NOMINATIM_REQUEST") == "1"

class TestSearch(TestCase):
    def test_params(self):
        street = "rua turquia, 218"
        city = "ribeirao pires"
        country = "brasil"
        format = "jsonv2"
        addressdetails = "1"

        params_expected = {
            "street": street,
            "city": city,
            "country": country,
            "format": format,
            "addressdetails": addressdetails,
        }
        params_got = _search_params(street, city, country, format, addressdetails)

        self.assertDictEqual(params_got, params_expected)

    def test_search(self):
        if avoid_heavy_use():
            self.skipTest("avoid heavy use (Nominatim Usage Policy)")

        street = "rua turquia, 218"
        city = "ribeirao pires"
        country = "brasil"
        format = "jsonv2"
        addressdetails = False
        search_got = _search(street, city, country, format, addressdetails)
        search_expected = [
            {
                "place_id": 146430545,
                "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                "osm_type": "way",
                "osm_id": 172716033,
                "boundingbox": [
                "-23.7021573",
                "-23.6997948",
                "-46.4148147",
                "-46.4140582"
                ],
                "lat": "-23.7010955",
                "lon": "-46.4144766",
                "display_name": "Rua Turquia, Jardim Itacolomy, Ribeirão Pires, Região Imediata de São Paulo, Região Metropolitana de São Paulo, Região Geográfica Intermediária de São Paulo, São Paulo, Região Sudeste, 09402-060, Brasil",
                "place_rank": 26,
                "category": "highway",
                "type": "residential",
                "importance": 0.5
            }
        ]

        for i in range(len(search_expected)):
            d_expected = search_expected[i]
            d_got = search_got[i]
            self.assertDictEqual(d_got, d_expected)


if __name__ == "__main__":
    main()
