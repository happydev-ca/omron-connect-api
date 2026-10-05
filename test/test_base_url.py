import unittest

from omron_connect_api import CountryCodeNotSupportedError
from omron_connect_api.base_url import base_url_for, NORTH_AMERICA_BASE_URL


class TestBaseUrl(unittest.TestCase):
    def test_north_america_country_codes_map_to_north_america_base_url(self):
        for country_code in ['CA', 'US']:
            with self.subTest(country_code=country_code):
                self.assertEqual(base_url_for(country_code), NORTH_AMERICA_BASE_URL)

    def test_unsupported_country_code_raises(self):
        with self.assertRaises(CountryCodeNotSupportedError) as context:
            base_url_for('FR')

        self.assertEqual(context.exception.country_code, 'FR')
