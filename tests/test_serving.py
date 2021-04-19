import http.client
import json
import os
import shutil
import socket
import ssl
import sys
from io import BytesIO
from pathlib import Path

import pytest

from werkzeug import run_simple
from werkzeug._reloader import _find_stat_paths
from werkzeug._reloader import _find_watchdog_paths
from werkzeug._reloader import _get_args_for_reloading
from werkzeug.datastructures import FileStorage
from werkzeug.serving import make_ssl_devcert
from werkzeug.test import stream_encode_multipart


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({}, id="http"),
        pytest.param({"ssl_context": "adhoc"}, id="https"),
        pytest.param({"use_reloader": True}, id="reloader"),
        pytest.param(
            {"hostname": "unix"},
            id="unix socket",
            marks=pytest.mark.skipif(
                not hasattr(socket, "AF_UNIX"), reason="requires unix socket support"
            ),
        ),
    ],
)
def test_server(tmp_path, dev_server, kwargs: dict):
    if kwargs.get("hostname") == "unix":
        kwargs["hostname"] = f"unix://{tmp_path / 'test.sock'}"

    client = dev_server(**kwargs)
    r = client.request()
    assert r.status == 200
    assert r.json["PATH_INFO"] == "/"


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_untrusted_host(standard_app):
    r = standard_app.request(
        "http://missing.test:1337/index.html#ignore",
        headers={"x-base-url": standard_app.url},
    )
    assert r.json["HTTP_HOST"] == "missing.test:1337"
    assert r.json["PATH_INFO"] == "/index.html"
    host, _, port = r.json["HTTP_X_BASE_URL"].rpartition(":")
    assert r.json["SERVER_NAME"] == host.partition("http://")[2]
    assert r.json["SERVER_PORT"] == port


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_double_slash_path(standard_app):
    r = standard_app.request("//double-slash")
    assert "double-slash" not in r.json["HTTP_HOST"]
    assert r.json["PATH_INFO"] == "/double-slash"


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_500_error(standard_app):
    r = standard_app.request("/crash")
    assert r.status == 500
    assert b"Internal Server Error" in r.data


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_ssl_dev_cert(tmp_path, dev_server):
    client = dev_server(ssl_context=make_ssl_devcert(tmp_path))
    r = client.request()
    assert r.json["wsgi.url_scheme"] == "https"


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_ssl_object(dev_server):
    client = dev_server(ssl_context="custom")
    r = client.request()
    assert r.json["wsgi.url_scheme"] == "https"


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.parametrize("reloader_type", ["stat", "watchdog"])
@pytest.mark.skipif(
    os.name == "nt" and "CI" in os.environ, reason="unreliable on Windows during CI"
)
def test_reloader_sys_path(tmp_path, dev_server, reloader_type):
    """This tests the general behavior of the reloader. It also tests
    that fixing an import error triggers a reload, not just Python
    retrying the failed import.
    """
    real_path = tmp_path / "real_app.py"
    real_path.write_text("syntax error causes import error")

    client = dev_server("reloader", reloader_type=reloader_type)
    assert client.request().status == 500

    shutil.copyfile(Path(__file__).parent / "live_apps" / "standard_app.py", real_path)
    client.wait_for_log(f" * Detected change in {str(real_path)!r}, reloading")
    client.wait_for_reload()
    assert client.request().status == 200


def test_windows_get_args_for_reloading(monkeypatch, tmp_path):
    argv = [str(tmp_path / "test.exe"), "run"]
    monkeypatch.setattr("sys.executable", str(tmp_path / "python.exe"))
    monkeypatch.setattr("sys.argv", argv)
    monkeypatch.setattr("__main__.__package__", None)
    monkeypatch.setattr("os.name", "nt")
    rv = _get_args_for_reloading()
    assert rv == argv


@pytest.mark.parametrize("find", [_find_stat_paths, _find_watchdog_paths])
def test_exclude_patterns(find):
    # Imported paths under sys.prefix will be included by default.
    paths = find(set(), set())
    assert any(p.startswith(sys.prefix) for p in paths)
    # Those paths should be excluded due to the pattern.
    paths = find(set(), {f"{sys.prefix}*"})
    assert not any(p.startswith(sys.prefix) for p in paths)


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_wrong_protocol(standard_app):
    """An HTTPS request to an HTTP server doesn't show a traceback.
    https://github.com/pallets/werkzeug/pull/838
    """
    conn = http.client.HTTPSConnection(standard_app.addr)

    with pytest.raises(ssl.SSLError):
        conn.request("GET", f"https://{standard_app.addr}")

    assert "Traceback" not in standard_app.log.read()


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_content_type_and_length(standard_app):
    r = standard_app.request()
    assert "CONTENT_TYPE" not in r.json
    assert "CONTENT_LENGTH" not in r.json

    r = standard_app.request(body=b"{}", headers={"content-type": "application/json"})
    assert r.json["CONTENT_TYPE"] == "application/json"
    assert r.json["CONTENT_LENGTH"] == "2"


def test_port_is_int():
    with pytest.raises(TypeError, match="port must be an integer"):
        run_simple("127.0.0.1", "5000", None)


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.parametrize("send_length", [False, True])
@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires Python >= 3.7")
def test_chunked_request(monkeypatch, dev_server, send_length):
    stream, length, boundary = stream_encode_multipart(
        {
            "value": "this is text",
            "file": FileStorage(
                BytesIO(b"this is a file"),
                filename="test.txt",
                content_type="text/plain",
            ),
        }
    )
    client = dev_server("data")
    # Small block size to produce multiple chunks.
    conn = client.connect(blocksize=128)
    conn.putrequest("POST", "/")
    conn.putheader("Transfer-Encoding", "chunked")
    conn.putheader("Content-Type", f"multipart/form-data; boundary={boundary}")

    # Sending the content-length header with chunked is invalid, but if
    # a client does send it the server should ignore it. Previously the
    # multipart parser would crash. Python's higher-level functions
    # won't send the header, which is why we use conn.put in this test.
    if send_length:
        conn.putheader("Content-Length", "invalid")
        expect_content_len = "invalid"
    else:
        expect_content_len = None

    conn.endheaders(stream, encode_chunked=True)
    r = conn.getresponse()
    data = json.load(r)
    r.close()
    assert data["form"]["value"] == "this is text"
    assert data["files"]["file"] == "this is a file"
    environ = data["environ"]
    assert environ["HTTP_TRANSFER_ENCODING"] == "chunked"
    assert environ.get("CONTENT_LENGTH") == expect_content_len
    assert environ["wsgi.input_terminated"]


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_multiple_headers_concatenated(standard_app):
    """A header key can be sent multiple times. The server will join all
    the values with commas.

    https://tools.ietf.org/html/rfc3875#section-4.1.18
    """
    # conn.request doesn't support multiple values.
    conn = standard_app.connect()
    conn.putrequest("GET", "/")
    conn.putheader("XYZ", "a ")  # trailing space is preserved
    conn.putheader("X-Ignore-1", "ignore value")
    conn.putheader("XYZ", " b")  # leading space is collapsed
    conn.putheader("X-Ignore-2", "ignore value")
    conn.putheader("XYZ", "c ")
    conn.putheader("X-Ignore-3", "ignore value")
    conn.putheader("XYZ", "d")
    conn.endheaders()
    r = conn.getresponse()
    data = json.load(r)
    r.close()
    assert data["HTTP_XYZ"] == "a ,b,c ,d"


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_multiline_header_folding(standard_app):
    """A header value can be split over multiple lines with a leading
    tab. The server will remove the newlines and preserve the tabs.

    https://tools.ietf.org/html/rfc2616#section-2.2
    """
    # conn.request doesn't support multiline values.
    conn = standard_app.connect()
    conn.putrequest("GET", "/")
    conn.putheader("XYZ", "first", "second", "third")
    conn.endheaders()
    r = conn.getresponse()
    data = json.load(r)
    r.close()
    assert data["HTTP_XYZ"] == "first\tsecond\tthird"


@pytest.mark.parametrize("endpoint", ["", "crash"])
def test_streaming_nonchunked_response(dev_server, endpoint):
    """When using HTTP/1.0, chunked encoding cannot be supported, fall back to
    Connection: close, but this allows no reliable way to distinguish between
    complete and truncated response."""

    r = dev_server("streaming").request("/" + endpoint)
    assert r.getheader("connection") == "close"
    assert r.data == "".join(str(x) + "\n" for x in range(5)).encode()


def test_streaming_chunked_response(dev_server):
    """When using HTTP/1.1, chunked encoding is preferable over
    `Connection: close`, due to better support to avoid truncation of content

    https://tools.ietf.org/html/rfc2616#section-3.6.1
    """

    r = dev_server("streaming", request_handler="HTTP/1.1").request("/")
    assert r.getheader("transfer-encoding") == "chunked"
    assert r.data == "".join(str(x) + "\n" for x in range(5)).encode()


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_streaming_chunked_truncation(dev_server):
    """When using HTTP/1.1, chunked encoding allows the client to detect
    content truncated by prematurely closed connection.
    """

    with pytest.raises(http.client.IncompleteRead):
        dev_server("streaming", request_handler="HTTP/1.1").request("/crash")
