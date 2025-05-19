[![Build, test and publish](https://github.com/happydev-ca/omron-connect-api/actions/workflows/publish.yml/badge.svg)](https://github.com/happydev-ca/omron-connect-api/actions/workflows/publish.yml)

# omron-connect-api

Library to communicate with OMRON connect API.

## Usage

```python
import aiohttp
import asyncio
import os

from omron_connect_api import OmronConnectApi


async def run():
    async with aiohttp.ClientSession() as session:
        api = OmronConnectApi(os.environ['EMAIL'], os.environ['PASSWORD'], session)
        blood_pressure_readings = await api.async_get_blood_pressure_readings()
        print(blood_pressure_readings)


asyncio.run(run())
```

### Build and test locally

```shell
make venv
source .venv/bin/activate
make test
make build
```

### Release version

```shell
make release bump=patch|minor|major
```