"""Helper classes as mocks for requests objects.
"""

from io import BytesIO


class FakeStream(object):

    def __init__(self, contents):
        self._io = BytesIO(contents)

    def read(self, size, decode_content=None):
        return self._io.read(size)

    def stream(self, size, decode_content=None):
        yield self._io.read(size)

    def release_conn(self):
        pass


class MockResponse(object):

    def __init__(self, contents):
        self.raw = FakeStream(contents)
        self.content = contents
        self.request = None
        self.status_code = 200
        self.connection = None
        self.url = None
        self.headers = {'Content-Length': len(contents)}
        self.history = []

    def raise_for_status(self):
        pass


class MockConnection(object):

    def _send(self, req, **kwargs):
        raise NotImplementedError("_send must be overridden for tests")

    def send(self, req, **kwargs):
        resp = self._send(req, **kwargs)
        for cb in req.hooks.get("response", []):
            cb(resp)
        return resp


class MockRequest(object):

    def __init__(self, url):
        self.url = url
        self.headers = {}
        self.hooks = {}

    def register_hook(self, event_name, callback):
        self.hooks.setdefault(event_name, []).append(callback)
