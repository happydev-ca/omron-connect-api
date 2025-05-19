import aiohttp


class OmronConnectAPIError(aiohttp.ClientResponseError):
    def __init__(self, error_response: aiohttp.ClientResponse):
        self.request_info = error_response.request_info
        self.history = error_response.history
        self.status = error_response.status
        self.message = error_response.reason
        self.headers = error_response.headers
