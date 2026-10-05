from .omron_connect_api_errors import CountryCodeNotSupportedError

NORTH_AMERICA_BASE_URL = 'https://oi-api.ohiomron.com'

_BASE_URL_BY_COUNTRY_CODE = {
    'CA': NORTH_AMERICA_BASE_URL,
    'US': NORTH_AMERICA_BASE_URL,
}


def base_url_for(country_code: str) -> str:
    try:
        return _BASE_URL_BY_COUNTRY_CODE[country_code]
    except KeyError:
        raise CountryCodeNotSupportedError(country_code) from None
