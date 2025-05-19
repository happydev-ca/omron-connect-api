from datetime import datetime, timedelta
from logging import getLogger, Logger
from typing import List

import aiohttp

from . import OmronConnectAPIError, BloodPressureReading
from .blood_pressure.blood_pressure_reading_response import BloodPressureReadingResponse

LOGGER: Logger = getLogger(__package__)


class OmronConnectApi:
    base_url = 'https://oi-api.ohiomron.com'
    TOKEN_EXPIRED = timedelta(seconds=1)

    def __init__(self, email_address: str, password: str, session: aiohttp.ClientSession):
        self.email_address = email_address
        self.password = password
        self.session = session
        self.headers = {'Content-Type': 'application/json'}
        self.expires_at = datetime.now() - self.TOKEN_EXPIRED
        self.last_synced_time = 0

    async def async_authenticate(self) -> None:
        if datetime.now() < self.expires_at:
            return

        url = '/app/login'
        json = {'app': 'OCM', 'country': 'CA', 'emailAddress': self.email_address, 'password': self.password}
        async with await self._post(url, json) as response:
            body = await response.json()
            self.headers['Authorization'] = body['accessToken']
            self.expires_at = datetime.now() + timedelta(seconds=body['expiresIn'])

    async def async_get_blood_pressure_readings(self) -> List[BloodPressureReading]:
        await self.async_authenticate()

        url = f'/app/v2/sync/bp?nextpaginationKey=0&lastSyncedTime={self.last_synced_time}&phoneIdentifier='
        async with await self._get(url) as response:
            json = await response.json()
            self.last_synced_time = int(json['lastSyncedTime'])
            return [BloodPressureReadingResponse.from_json(reading) for reading in json['data']]

    async def _post(self, url: str, json: dict) -> aiohttp.ClientResponse:
        response = await self.session.post(url=f'{self.base_url}{url}', headers=self.headers, json=json)
        await self._log(url, response, self.headers, json)
        await self._raise_on_error(response)
        return response

    async def _get(self, url: str) -> aiohttp.ClientResponse:
        response = await self.session.get(f'{self.base_url}{url}', headers=self.headers)
        await self._log(url, response, self.headers)
        await self._raise_on_error(response)
        return response

    async def _raise_on_error(self, response: aiohttp.ClientResponse) -> None:
        body = await response.json()
        if body['success']:
            return
        self.expires_at = datetime.now() - self.TOKEN_EXPIRED
        self.headers.pop('Authorization', None)
        raise OmronConnectAPIError(response)

    @staticmethod
    async def _log(url: str, response: aiohttp.ClientResponse, headers: dict, json: dict = None) -> None:
        LOGGER.debug(
            f"{url} : Request[[ headers=[{headers}] json=[{json}] ]] - Response[[ status=[{response.status}] headers=[{dict(response.headers)}] body=[{await response.text()}] ]]")
