from unittest import main, TestCase

from distances.entities import Address

class TestAddress(TestCase):
    def test_instance(self):
        street = "av miguel prisco"
        house_number = "122"
        city = "ribeirao pires"
        country = "brasil"

        a = Address(
            street=street,
            house_number=house_number,
            city=city,
            country=country
        )

        self.assertEqual(a.street, street)
        self.assertEqual(a.house_number, house_number)
        self.assertEqual(a.city, city)
        self.assertEqual(a.country, country)

if __name__ == "__main__":
    main()
