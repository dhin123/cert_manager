class RequestBuilder:
    def __init__(self, url: str, http_method: str):
        self.url = url
        self.http_method = http_method
        self.headers = dict()
        self.params = dict()
        self.http_timeout = "HTTP_REQUESTS_TIMEOUT"
        self.body = None

    def with_url(self, url: str):
        self.url = url
        return self

    def with_headers(self, headers: dict):
        self.headers.update(headers)
        return self

    def with_body(self, body):
        self.body = body
        return self

    def with_http_timeout(self, http_timeout):
        self.http_timeout = http_timeout
        return self

    def build(self):
        return {
            'url': self.url,
            'method': self.http_method,
            'headers': self.headers,
            'params': self.params,
            'timeout': self.http_timeout,
            'body': self.body
        }
        # if self.http_method is None:
        #     raise ExceptionFactory(self).internal_server_error("HTTP Method not defined")



