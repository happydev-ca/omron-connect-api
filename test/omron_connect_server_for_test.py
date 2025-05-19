from http import HTTPStatus

from aioresponses import aioresponses


class OmronConnectServerForTest:
    base_url = 'https://oi-api.ohiomron.com'

    def __init__(self):
        self.server = aioresponses()

    def __enter__(self):
        self.server.__enter__()
        return self

    def __exit__(self, *args):
        self.server.__exit__(*args)

    def prepare_login_response(self, body: dict = None, repeat: bool = True) -> str:
        if body is None:
            body = {'success': True, 'accessToken': 'token', 'expiresIn': 3600}
        self.server.post(f'{self.base_url}/app/login', status=HTTPStatus.OK, payload=body, repeat=repeat)
        return body.get('accessToken')

    def prepare_blood_pressure_readings_response(self, last_synced_time: int = 0, body: dict = None, repeat: bool = True):
        if body is None:
            body = {'success': True, 'data': [], 'lastSyncedTime': 0}
        url = f'/app/v2/sync/bp?nextpaginationKey=0&lastSyncedTime={last_synced_time}&phoneIdentifier='
        self.server.get(f'{self.base_url}{url}', status=HTTPStatus.OK, payload=body, repeat=repeat)

    def assert_called_with(self, url, method, *args, **kwargs):
        self.server.assert_called_with(f'{self.base_url}{url}', method, *args, **kwargs)

    def assert_called_once_with(self, url, method, *args, **kwargs):
        self.server.assert_called_once_with(f'{self.base_url}{url}', method, *args, **kwargs)
