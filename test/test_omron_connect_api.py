import unittest
from datetime import datetime, timedelta

import aiohttp

from omron_connect_api import OmronConnectAPIError, OmronConnectApi
from omron_connect_api.blood_pressure.blood_pressure_reading_response import BloodPressureReadingResponse
from test.omron_connect_server_for_test import OmronConnectServerForTest


class TestOmronConnectAPI(unittest.IsolatedAsyncioTestCase):
    email_address = 'user@gmail.com'
    password = 'password'

    async def test_authenticates_with_email_address_and_password(self):
        with OmronConnectServerForTest() as server:
            server.prepare_login_response({'success': True, 'accessToken': 'any-token', 'expiresIn': 3600})

            async with aiohttp.ClientSession() as session:
                api = OmronConnectApi(self.email_address, self.password, session)
                await api.async_authenticate()

                server.assert_called_with(url='/app/login',
                                          method='POST',
                                          headers={'Content-Type': 'application/json'},
                                          json={
                                              'app': 'OCM',
                                              'country': 'CA',
                                              'emailAddress': self.email_address,
                                              'password': self.password
                                          })

                self.assertEqual(api.headers.get('Authorization'), 'any-token')
                self.assertLess(datetime.now() + timedelta(seconds=3600) - api.expires_at, timedelta(seconds=1))

    async def test_reuse_valid_token(self):
        with OmronConnectServerForTest() as server:
            server.prepare_login_response({'success': True, 'accessToken': 'any-token', 'expiresIn': 3600})
            async with aiohttp.ClientSession() as session:
                api = OmronConnectApi(self.email_address, self.password, session)
                await api.async_authenticate()
                await api.async_authenticate()

                server.assert_called_once_with(url='/app/login',
                                               method='POST',
                                               headers={'Content-Type': 'application/json'},
                                               json={
                                                   'app': 'OCM',
                                                   'country': 'CA',
                                                   'emailAddress': self.email_address,
                                                   'password': self.password
                                               })

    async def test_authenticates_error(self):
        with OmronConnectServerForTest() as server:
            server.prepare_login_response({'success': False})

            async with aiohttp.ClientSession() as session:
                api = OmronConnectApi(self.email_address, self.password, session)

                with self.assertRaises(OmronConnectAPIError):
                    await api.async_authenticate()

    async def test_clear_headers_on_error(self):
        with OmronConnectServerForTest() as server:
            server.prepare_login_response({'success': False})

            async with aiohttp.ClientSession() as session:
                api = OmronConnectApi(self.email_address, self.password, session)
                api.headers['Authorization'] = 'any-token'

                with self.assertRaises(OmronConnectAPIError):
                    await api.async_authenticate()
                self.assertEqual(api.headers.get('Authorization'), None)
                self.assertLess(datetime.now() - api.TOKEN_EXPIRED - api.expires_at, timedelta(seconds=1))


    async def test_get_blood_pressure_readings(self):
        with OmronConnectServerForTest() as server:
            token = server.prepare_login_response()
            response = {
                'success': True,
                'lastSyncedTime': 1747615042001,
                'data': [
                    {
                        'measurementDate': '1747615042000',
                        'diastolic': 82,
                        'systolic': 103,
                        'pulse': 62,
                        'countIrregularHeartBeat': 2,
                        'movementDetect': 1
                    },
                    {
                        'measurementDate': '1747615062000',
                        'diastolic': 72,
                        'systolic': 100,
                        'pulse': 64,
                        'countIrregularHeartBeat': 0,
                        'movementDetect': 0
                    }
                ]
            }
            server.prepare_blood_pressure_readings_response(0, response)
            async with aiohttp.ClientSession() as session:
                api = OmronConnectApi(self.email_address, self.password, session)
                readings = await api.async_get_blood_pressure_readings()

                server.assert_called_with(
                    url='/app/v2/sync/bp?nextpaginationKey=0&lastSyncedTime=0&phoneIdentifier=',
                    method='GET',
                    headers={'Content-Type': 'application/json', 'Authorization': token})

                expected_readings = [BloodPressureReadingResponse.from_json(reading) for reading in response['data']]
                self.assertEqual(readings, expected_readings)
                self.assertEqual(api.last_synced_time, 1747615042001)

    async def test_get_blood_pressure_readings_from_last_synced_time(self):
        with OmronConnectServerForTest() as server:
            token = server.prepare_login_response()
            server.prepare_blood_pressure_readings_response(last_synced_time=1747615042001)

            async with aiohttp.ClientSession() as session:
                api = OmronConnectApi(self.email_address, self.password, session)
                api.last_synced_time = 1747615042001
                await api.async_get_blood_pressure_readings()

                server.assert_called_with(
                    url='/app/v2/sync/bp?nextpaginationKey=0&lastSyncedTime=1747615042001&phoneIdentifier=',
                    method='GET',
                    headers={'Content-Type': 'application/json', 'Authorization': token})