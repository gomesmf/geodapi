from unittest import main, TestCase

from deliveries.entities import Address, Distance

class TestAddress(TestCase):
    def test_instance(self):
        street = "av miguel prisco"
        house_number = "122"
        city = "ribeirao pires"
        country = "brasil"
        latitude = "12.3233"
        longitude = "12.3233"

        a = Address(
            street=street,
            house_number=house_number,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude
        )

        self.assertEqual(a.street, street)
        self.assertEqual(a.house_number, house_number)
        self.assertEqual(a.city, city)
        self.assertEqual(a.country, country)
        self.assertEqual(a.latitude, latitude)
        self.assertEqual(a.longitude, longitude)

    def test_to_string(self):
        street = "av miguel prisco"
        house_number = "122"
        city = "ribeirao pires"
        country = "brasil"
        latitude = "12.3233"
        longitude = "12.3233"

        a = Address(
            street=street,
            house_number=house_number,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude
        )

        self.assertEqual(a.to_string(), f"{street.title()}, {house_number.title()}, {city.title()}, {country.title()} ({latitude}, {longitude})")

    def test_to_dict(self):
        street = "av miguel prisco"
        house_number = "122"
        city = "ribeirao pires"
        country = "brasil"
        latitude = "12.3233"
        longitude = "12.3233"

        a = Address(
            street=street,
            house_number=house_number,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude
        )

        self.assertDictEqual(a.to_dict(), {
            "street": street,
            "house_number": house_number,
            "city": city,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
        })

class TestDistance(TestCase):
    def test_instance(self):
        unit = "km"
        value = 10.2

        d = Distance(value, unit)

        self.assertEqual(d.unit, unit)
        self.assertEqual(d.value, value)

if __name__ == "__main__":
    main()
