"""
https://www.rfc-editor.org/rfc/rfc9112#name-message-format
HTTP-message   = start-line CRLF
                 *( field-line CRLF )
                 CRLF
                 [ message-body ]
"""

import io
from enum import Enum, auto


class HttpState(Enum):
    START = auto()
    HEADERS = auto()

class HttpRequest:
    def __init__(self):
        self.headers = {}

    def parse(self, data):
        bs = io.BytesIO(data)

        request_line = bs.readline()
        self.method, self.uri, self.version = request_line.rstrip().split(b' ')

        while True:
            field_line = bs.readline()
            print(field_line)
            if field_line == b'\r\n':
                break

            field_name, field_value = field_line.rstrip().split(b':')
            self.headers[field_name.lower()] = field_value

            


if __name__ == '__main__':
    req = HttpRequest()

    req.parse(b'GET / HTTP/1.0\r\nUser-agent:test\r\nFoo:bar\r\n\r\n')
    assert req.method == b'GET'
    assert req.uri == b'/'
    assert req.version == b'HTTP/1.0'
    assert req.headers[b'user-agent'] == b'test'
    assert len(req.headers) == 2
    print('ok')
