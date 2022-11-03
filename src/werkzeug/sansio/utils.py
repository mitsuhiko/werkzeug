import typing as t
import re
from .._internal import _encode_idna
from ..exceptions import SecurityError
from ..urls import uri_to_iri
from ..urls import url_quote


def host_is_trusted(hostname: str, trusted_list: t.Iterable[str]) -> bool:
    """Check if a host matches a list of trusted names.

    :param hostname: The name to check.
    :param trusted_list: A list of valid names to match. If a name
        starts with a dot it will match all subdomains.

    .. versionadded:: 0.9
    """
    if not hostname:
        return False

    if isinstance(trusted_list, str):
        trusted_list = [trusted_list]

    def _normalize(hostname: str) -> bytes:
        if ":" in hostname:
            hostname = hostname.rsplit(":", 1)[0]

        return _encode_idna(hostname)

    try:
        hostname_bytes = _normalize(hostname)
    except UnicodeError:
        return False

    for ref in trusted_list:
        if ref.startswith("."):
            ref = ref[1:]
            suffix_match = True
        else:
            suffix_match = False

        try:
            ref_bytes = _normalize(ref)
        except UnicodeError:
            return False

        if ref_bytes == hostname_bytes:
            return True

        if suffix_match and hostname_bytes.endswith(b"." + ref_bytes):
            return True

    return False


def get_host(
    scheme: str,
    host_header: t.Optional[str],
    server: t.Optional[t.Tuple[str, t.Optional[int]]] = None,
    trusted_hosts: t.Optional[t.Iterable[str]] = None,
) -> str:
    """Return the host for the given parameters.

    This first checks the ``host_header``. If it's not present, then
    ``server`` is used. The host will only contain the port if it is
    different than the standard port for the protocol.
    
    Validate host value according to RFC 1034/1035.
    More info:
        https://www.rfc-editor.org/rfc/rfc1034.html
        https://www.rfc-editor.org/rfc/rfc1035.html

    Optionally, verify that the host is trusted using
    :func:`host_is_trusted` and raise a
    :exc:`~werkzeug.exceptions.SecurityError` if it is not.

    :param scheme: The protocol the request used, like ``"https"``.
    :param host_header: The ``Host`` header value.
    :param server: Address of the server. ``(host, port)``, or
        ``(path, None)`` for unix sockets.
    :param trusted_hosts: A list of trusted host names.

    :return: Host, with port if necessary.
    :raise ~werkzeug.exceptions.SecurityError: If the host is not
        trusted.
    """
    host_validation_re = re.compile(r"^([A-Za-z0-9.-]+|\[[a-f0-9]*:[a-f0-9\.:]+\])(:[0-9]+)?$")
    host = ""

    if host_header is not None:
        host = host_header
    elif server is not None:
        host = server[0]

        if server[1] is not None:
            host = f"{host}:{server[1]}"

    if scheme in {"http", "ws"} and host.endswith(":80"):
        host = host[:-3]
    elif scheme in {"https", "wss"} and host.endswith(":443"):
        host = host[:-4]
    
    if host_validation_re.match(host) is None:
        raise SecurityError(f"Host {host!r} is not valid according to RFC 1034/1035")

    if trusted_hosts is not None:
        if not host_is_trusted(host, trusted_hosts):
            raise SecurityError(f"Host {host!r} is not trusted.")
    return host


def get_current_url(
    scheme: str,
    host: str,
    root_path: t.Optional[str] = None,
    path: t.Optional[str] = None,
    query_string: t.Optional[bytes] = None,
) -> str:
    """Recreate the URL for a request. If an optional part isn't
    provided, it and subsequent parts are not included in the URL.

    The URL is an IRI, not a URI, so it may contain Unicode characters.
    Use :func:`~werkzeug.urls.iri_to_uri` to convert it to ASCII.

    :param scheme: The protocol the request used, like ``"https"``.
    :param host: The host the request was made to. See :func:`get_host`.
    :param root_path: Prefix that the application is mounted under. This
        is prepended to ``path``.
    :param path: The path part of the URL after ``root_path``.
    :param query_string: The portion of the URL after the "?".
    """
    url = [scheme, "://", host]

    if root_path is None:
        url.append("/")
        return uri_to_iri("".join(url))

    url.append(url_quote(root_path.rstrip("/")))
    url.append("/")

    if path is None:
        return uri_to_iri("".join(url))

    url.append(url_quote(path.lstrip("/")))

    if query_string:
        url.append("?")
        url.append(url_quote(query_string, safe=":&%=+$!*'(),"))

    return uri_to_iri("".join(url))


def get_content_length(
    http_content_length: t.Union[str, None] = None,
    http_transfer_encoding: t.Union[str, None] = "",
) -> t.Optional[int]:
    """Returns the content length as an integer or ``None`` if
    unavailable or chunked transfer encoding is used.

    :param http_content_length: The Content-Length HTTP header.
    :param http_transfer_encoding: The Transfer-Encoding HTTP header.

    .. versionadded:: 2.2
    """
    if http_transfer_encoding == "chunked":
        return None

    if http_content_length is not None:
        try:
            return max(0, int(http_content_length))
        except (ValueError, TypeError):
            pass
    return None
