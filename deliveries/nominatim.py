from .entities import Address
from .external import SearchServiceInterface, SearchResult
import requests

SEARCH_ENDPOINT = "https://nominatim.openstreetmap.org/search"

def _search_params(street: str, city: str, country: str, format: str = None, addressdetails: str = None) -> str:
    params = {}

    if street:
        params["street"] = street
    if city:
        params["city"] = city
    if country:
        params["country"] = country
    if format:
        params["format"] = format
    if addressdetails:
        params["addressdetails"] = addressdetails

    return params

def _search(street: str, city: str, country: str, format: str = "jsonv2", addressdetails: bool = False):
    ad = None
    if addressdetails:
        ad = "1"

    params = _search_params(
        street=street,
        city=city,
        country=country,
        format=format,
        addressdetails=ad
    )

    r = requests.get(SEARCH_ENDPOINT, params=params)

    return r.json()

class NominatimSearch(SearchServiceInterface):
    def search(self, addr: Address):
        nsr = _search(
            street=f"{addr.street} {addr.house_number}",
            city=addr.city,
            country=addr.country,
            format="jsonv2",
            addressdetails=False
        )

        return SearchResult(result=nsr[0])
