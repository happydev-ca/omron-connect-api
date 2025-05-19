import aiohttp
import asyncio
import os

from omron_connect_api import OmronConnectApi


async def run():
    async with aiohttp.ClientSession() as session:
        api = OmronConnectApi(os.environ['EMAIL'], os.environ['PASSWORD'], os.environ['COUNTRY_CODE'], session)
        blood_pressure_readings = await api.async_get_blood_pressure_readings()
        print(blood_pressure_readings)


asyncio.run(run())
