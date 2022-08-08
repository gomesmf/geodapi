class Address:
    def __init__(self, street: str = None, house_number: int = None, city: str = None, country: str = None, latitude: str = None, longitude: str = None) -> None:
        self.street = street
        self.house_number = house_number
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    def to_string(self):
        return f"{self.street.title()}, {self.house_number}, {self.city.title()}, {self.country.title()} ({self.latitude}, {self.longitude})"

class Distance:
    def __init__(self, value: float, unit: str) -> None:
        self.value = value
        self.unit = unit
