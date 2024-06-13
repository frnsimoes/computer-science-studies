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
    BODY = auto()
    END = auto()


class HttpRequest:
    def __init__(self):
        self.headers = {}
        self.residual = b""
        self.state = HttpState.START
        self.body = b""

    def is_request_line_end(self, request_line):
        """
        the request line should end with "\r\n", so "\n" is the last item.
        if something is after the last character, it's a residual
        request-line   = method SP request-target SP HTTP-version
        = b'GET / HTTP/1.0\r\n'
        """

        if request_line[-1:] != b"\n":
            self.residual = request_line
            return True
        return False

    def check_headers(
        self,
    ):
        """
        https://www.rfc-editor.org/rfc/rfc9112#name-field-line-parsing

        In the context of HTTP, a field line refers to a single line in the header section of an HTTP message. Each field line consists of a field name and a field value, separated by a colon `:`. For example, `Content-Type: text/html` is a field line.

        HTTP headers are a collection of these field lines. They provide information about the request or response, or about the object sent in the message body. Headers are structured as pairs of field names and values.
        """
        pass

    def parse(self, data):
        bs = io.BytesIO(self.residual + data)

        if self.state is HttpState.START:
            request_line = bs.readline()
            if request_line[-1:] != b"\n":
                self.residual = request_line
                return

            self.method, self.uri, self.version = request_line.rstrip().split(b" ")
            self.state = HttpState.HEADERS

        if self.state is HttpState.HEADERS:
            while True:
                field_line = bs.readline()
                # check: headers()
                if not field_line:
                    break
                if field_line[-1:] != b"\n":
                    self.residual = field_line
                    break
                if field_line == b"\r\n" or field_line == b"\n":
                    print(self.method)
                    if self.method == b"GET":
                        self.state = HttpState.END
                    else:
                        self.state = HttpState.BODY
                    break

                field_name, field_value = field_line.rstrip().split(b":")
                self.headers[field_name.lower()] = field_value

        if self.state is HttpState.BODY:
            self.body += bs.read()


if __name__ == "__main__":
    req = HttpRequest()
    req.parse(b"GET / HTTP/1.0\r\nUser-agent:test\r\nFoo:bar\r\n\r\n")

    assert req.method == b"GET"
    assert req.uri == b"/"
    assert req.version == b"HTTP/1.0"
    assert req.headers[b"user-agent"] == b"test"
    assert len(req.headers) == 2

    post_req = HttpRequest()
    post_req.parse(b"POST / HTTP/1.0\r\n\r\nfoo")
    assert post_req.state == HttpState.BODY
    assert post_req.body == b"foo"

    # parse something else to check if it is appended to the body
    post_req.parse(b"bar")
    assert post_req.body == b"foobar"

    # if it's a GET, ignore the body
    get_req = HttpRequest()
    get_req.parse(b"GET / HTTP/1.0\r\n\r\nfoo")
    assert get_req.state == HttpState.END
    assert get_req.body == b""
