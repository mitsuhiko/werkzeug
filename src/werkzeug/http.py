import base64
import re
import warnings
from datetime import datetime
from datetime import timedelta
from email.utils import parsedate_tz
from hashlib import md5
from time import gmtime
from time import struct_time
from time import time
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import overload
from typing import Tuple
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union
from urllib.parse import unquote_to_bytes as _unquote
from urllib.request import parse_http_list as _parse_list_header

from ._internal import _cookie_parse_impl
from ._internal import _cookie_quote
from ._internal import _make_cookie_domain
from ._internal import _to_bytes
from ._internal import _to_str
from .types import T
from .types import WSGIEnvironment

if TYPE_CHECKING:
    from .datastructures import (  # noqa: F401
        CallbackDict,
        CharsetAccept,
        LanguageAccept,
        MIMEAccept,
    )
    from .datastructures import AnyHeaders

_cookie_charset = "latin1"
_basic_auth_charset = "utf-8"
# for explanation of "media-range", etc. see Sections 5.3.{1,2} of RFC 7231
_accept_re = re.compile(
    r"""
    (                       # media-range capturing-parenthesis
      [^\s;,]+              # type/subtype
      (?:[ \t]*;[ \t]*      # ";"
        (?:                 # parameter non-capturing-parenthesis
          [^\s;,q][^\s;,]*  # token that doesn't start with "q"
        |                   # or
          q[^\s;,=][^\s;,]* # token that is more than just "q"
        )
      )*                    # zero or more parameters
    )                       # end of media-range
    (?:[ \t]*;[ \t]*q=      # weight is a "q" parameter
      (\d*(?:\.\d+)?)       # qvalue capturing-parentheses
      [^,]*                 # "extension" accept params: who cares?
    )?                      # accept params are optional
    """,
    re.VERBOSE,
)
_token_chars = frozenset(
    "!#$%&'*+-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ^_`abcdefghijklmnopqrstuvwxyz|~"
)
_etag_re = re.compile(r'([Ww]/)?(?:"(.*?)"|(.*?))(?:\s*,\s*|$)')
_unsafe_header_chars = set('()<>@,;:"/[]?={} \t')
_option_header_piece_re = re.compile(
    r"""
    ;\s*,?\s*  # newlines were replaced with commas
    (?P<key>
        "[^"\\]*(?:\\.[^"\\]*)*"  # quoted string
    |
        [^\s;,=*]+  # token
    )
    (?:\*(?P<count>\d+))?  # *1, optional continuation index
    \s*
    (?:  # optionally followed by =value
        (?:  # equals sign, possibly with encoding
            \*\s*=\s*  # * indicates extended notation
            (?:  # optional encoding
                (?P<encoding>[^\s]+?)
                '(?P<language>[^\s]*?)'
            )?
        |
            =\s*  # basic notation
        )
        (?P<value>
            "[^"\\]*(?:\\.[^"\\]*)*"  # quoted string
        |
            [^;,]+  # token
        )?
    )?
    \s*
    """,
    flags=re.VERBOSE,
)
_option_header_start_mime_type = re.compile(r",\s*([^;,\s]+)([;,]\s*.+)?")

_entity_headers = frozenset(
    [
        "allow",
        "content-encoding",
        "content-language",
        "content-length",
        "content-location",
        "content-md5",
        "content-range",
        "content-type",
        "expires",
        "last-modified",
    ]
)
_hop_by_hop_headers = frozenset(
    [
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
    ]
)


HTTP_STATUS_CODES = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",  # see RFC 8297
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi Status",
    208: "Already Reported",  # see RFC 5842
    226: "IM Used",  # see RFC 3229
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",  # unused
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",  # unused
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",  # see RFC 2324
    421: "Misdirected Request",  # see RFC 7540
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",  # see RFC 8470
    426: "Upgrade Required",
    428: "Precondition Required",  # see RFC 6585
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    449: "Retry With",  # proprietary MS extension
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",  # see RFC 2295
    507: "Insufficient Storage",
    508: "Loop Detected",  # see RFC 5842
    510: "Not Extended",
    511: "Network Authentication Failed",  # see RFC 6585
}


def wsgi_to_bytes(data: Union[str, bytes]) -> bytes:
    """If data is not bytes, encode it as latin1 for WSGI."""
    if isinstance(data, bytes):
        return data
    return data.encode("latin1")  # XXX: utf8 fallback?


def bytes_to_wsgi(data: bytes) -> str:
    assert isinstance(data, bytes), "data must be bytes"
    if isinstance(data, str):
        return data
    else:
        return data.decode("latin1")


def quote_header_value(
    value: Union[str, int], extra_chars: str = "", allow_token: bool = True
) -> str:
    """Quote a header value if necessary.

    .. versionadded:: 0.5

    :param value: the value to quote.
    :param extra_chars: a list of extra characters to skip quoting.
    :param allow_token: if this is enabled token values are returned
                        unchanged.
    """
    if isinstance(value, bytes):
        value = bytes_to_wsgi(value)
    value = str(value)
    if allow_token:
        token_chars = _token_chars | set(extra_chars)
        if set(value).issubset(token_chars):
            return value
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'


def unquote_header_value(value: str, is_filename: bool = False) -> str:
    r"""Unquotes a header value.  (Reversal of :func:`quote_header_value`).
    This does not use the real unquoting but what browsers are actually
    using for quoting.

    .. versionadded:: 0.5

    :param value: the header value to unquote.
    :param is_filename: The value represents a filename or path.
    """
    if value and value[0] == value[-1] == '"':
        # this is not the real unquoting, but fixing this so that the
        # RFC is met will result in bugs with internet explorer and
        # probably some other browsers as well.  IE for example is
        # uploading files with "C:\foo\bar.txt" as filename
        value = value[1:-1]

        # if this is a filename and the starting characters look like
        # a UNC path, then just return the value without quotes.  Using the
        # replace sequence below on a UNC path has the effect of turning
        # the leading double slash into a single slash and then
        # _fix_ie_filename() doesn't work correctly.  See #458.
        if not is_filename or value[:2] != "\\\\":
            return value.replace("\\\\", "\\").replace('\\"', '"')
    return value


def dump_options_header(
    header: str,
    options: Union[
        Dict[str, Optional[int]], "CallbackDict", Dict[str, int], Dict[str, str]
    ],
) -> str:
    """The reverse function to :func:`parse_options_header`.

    :param header: the header to dump
    :param options: a dict of options to append.
    """
    segments = []
    if header is not None:
        segments.append(header)
    for key, value in options.items():
        if value is None:
            segments.append(key)
        else:
            segments.append(f"{key}={quote_header_value(value)}")
    return "; ".join(segments)


def dump_header(iterable: Iterable, allow_token: bool = True) -> str:
    """Dump an HTTP header again.  This is the reversal of
    :func:`parse_list_header`, :func:`parse_set_header` and
    :func:`parse_dict_header`.  This also quotes strings that include an
    equals sign unless you pass it as dict of key, value pairs.

    >>> dump_header({'foo': 'bar baz'})
    'foo="bar baz"'
    >>> dump_header(('foo', 'bar baz'))
    'foo, "bar baz"'

    :param iterable: the iterable or dict of values to quote.
    :param allow_token: if set to `False` tokens as values are disallowed.
                        See :func:`quote_header_value` for more details.
    """
    if isinstance(iterable, dict):
        items = []
        for key, value in iterable.items():
            if value is None:
                items.append(key)
            else:
                items.append(
                    f"{key}={quote_header_value(value, allow_token=allow_token)}"
                )
    else:
        items = [quote_header_value(x, allow_token=allow_token) for x in iterable]
    return ", ".join(items)


def dump_csp_header(header: "ContentSecurityPolicy") -> str:
    """Dump a Content Security Policy header.

    These are structured into policies such as "default-src 'self';
    script-src 'self'".

    .. versionadded:: 1.0.0
       Support for Content Security Policy headers was added.

    """
    return "; ".join(f"{key} {value}" for key, value in header.items())


def parse_list_header(value: str) -> List[str]:
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    """
    result = []
    for item in _parse_list_header(value):
        if item[:1] == item[-1:] == '"':
            item = unquote_header_value(item[1:-1])
        result.append(item)
    return result


def parse_dict_header(
    value: Union[str, bytes], cls: Type[dict] = dict
) -> Dict[str, Optional[str]]:
    """Parse lists of key, value pairs as described by RFC 2068 Section 2 and
    convert them into a python dict (or any other mapping object created from
    the type with a dict like interface provided by the `cls` argument):

    >>> d = parse_dict_header('foo="is a fish", bar="as well"')
    >>> type(d) is dict
    True
    >>> sorted(d.items())
    [('bar', 'as well'), ('foo', 'is a fish')]

    If there is no value for a key it will be `None`:

    >>> parse_dict_header('key_without_value')
    {'key_without_value': None}

    To create a header from the :class:`dict` again, use the
    :func:`dump_header` function.

    .. versionchanged:: 0.9
       Added support for `cls` argument.

    :param value: a string with a dict header.
    :param cls: callable to use for storage of parsed results.
    :return: an instance of `cls`
    """
    result = cls()
    if not isinstance(value, str):
        # XXX: validate
        value = bytes_to_wsgi(value)
    for item in _parse_list_header(value):
        if "=" not in item:
            result[item] = None
            continue
        name, value = item.split("=", 1)
        if value[:1] == value[-1:] == '"':
            value = unquote_header_value(value[1:-1])
        result[name] = value
    return result


def parse_options_header(value: Optional[str], multiple: bool = False) -> Any:
    """Parse a ``Content-Type`` like header into a tuple with the content
    type and the options:

    >>> parse_options_header('text/html; charset=utf8')
    ('text/html', {'charset': 'utf8'})

    This should not be used to parse ``Cache-Control`` like headers that use
    a slightly different format.  For these headers use the
    :func:`parse_dict_header` function.

    .. versionchanged:: 0.15
        :rfc:`2231` parameter continuations are handled.

    .. versionadded:: 0.5

    :param value: the header to parse.
    :param multiple: Whether try to parse and return multiple MIME types
    :return: (mimetype, options) or (mimetype, options, mimetype, options, …)
             if multiple=True
    """
    if not value:
        return "", {}

    result = []

    value = "," + value.replace("\n", ",")
    while value:
        match = _option_header_start_mime_type.match(value)
        if not match:
            break
        result.append(match.group(1))  # mimetype
        options = {}  # type: ignore
        # Parse options
        rest = match.group(2)
        continued_encoding = None
        while rest:
            optmatch = _option_header_piece_re.match(rest)
            if not optmatch:
                break
            option, count, encoding, language, option_value = optmatch.groups()
            # Continuations don't have to supply the encoding after the
            # first line. If we're in a continuation, track the current
            # encoding to use for subsequent lines. Reset it when the
            # continuation ends.
            if not count:
                continued_encoding = None
            else:
                if not encoding:
                    encoding = continued_encoding
                continued_encoding = encoding
            option = unquote_header_value(option)
            if option_value is not None:
                option_value = unquote_header_value(option_value, option == "filename")
                if encoding is not None:
                    option_value = _unquote(option_value).decode(encoding)
            if count:
                # Continuations append to the existing value. For
                # simplicity, this ignores the possibility of
                # out-of-order indices, which shouldn't happen anyway.
                options[option] = options.get(option, "") + option_value
            else:
                options[option] = option_value
            rest = rest[optmatch.end() :]
        result.append(options)  # type: ignore
        if multiple is False:
            return tuple(result)
        value = rest

    return tuple(result) if result else ("", {})


AcceptClass = TypeVar(
    "AcceptClass", "Accept", "CharsetAccept", "LanguageAccept", "MIMEAccept"
)


@overload
def parse_accept_header(value: str, cls: None,) -> "Accept":
    ...


@overload
def parse_accept_header(value: str, cls: Type[AcceptClass],) -> AcceptClass:
    ...


def parse_accept_header(value, cls=None):
    """Parses an HTTP Accept-* header.  This does not implement a complete
    valid algorithm but one that supports at least value and quality
    extraction.

    Returns a new :class:`Accept` object (basically a list of ``(value, quality)``
    tuples sorted by the quality with some additional accessor methods).

    The second parameter can be a subclass of :class:`Accept` that is created
    with the parsed values and returned.

    :param value: the accept header string to be parsed.
    :param cls: the wrapper class for the return value (can be
                         :class:`Accept` or a subclass thereof)
    :return: an instance of `cls`.
    """
    if cls is None:
        cls = Accept

    if not value:
        return cls(None)

    result = []
    for match in _accept_re.finditer(value):
        quality_match = match.group(2)
        if not quality_match:
            quality: Union[int, float] = 1
        else:
            quality = max(min(float(quality_match), 1), 0)
        result.append((match.group(1), quality))
    return cls(result)


@overload
def parse_cache_control_header(
    value: Optional[str], on_update: Optional[Callable], cls: None,
) -> "RequestCacheControl":
    ...


@overload
def parse_cache_control_header(
    value: Optional[str], on_update: Optional[Callable], cls: Type[T],
) -> T:
    ...


def parse_cache_control_header(value, on_update=None, cls=None):
    """Parse a cache control header.  The RFC differs between response and
    request cache control, this method does not.  It's your responsibility
    to not use the wrong control statements.

    .. versionadded:: 0.5
       The `cls` was added.  If not specified an immutable
       :class:`~werkzeug.datastructures.RequestCacheControl` is returned.

    :param value: a cache control header to be parsed.
    :param on_update: an optional callable that is called every time a value
                      on the :class:`~werkzeug.datastructures.CacheControl`
                      object is changed.
    :param cls: the class for the returned object.  By default
                :class:`~werkzeug.datastructures.RequestCacheControl` is used.
    :return: a `cls` object.
    """
    if cls is None:
        cls = RequestCacheControl
    if not value:
        return cls(None, on_update)
    return cls(parse_dict_header(value), on_update)


@overload
def parse_csp_header(
    value: Optional[str], on_update: Callable, cls: None,
) -> "ContentSecurityPolicy":
    ...


@overload
def parse_csp_header(value: Optional[str], on_update: Callable, cls: Type[T]) -> T:
    ...


def parse_csp_header(value, on_update=None, cls=None):
    """Parse a Content Security Policy header.

    .. versionadded:: 1.0.0
       Support for Content Security Policy headers was added.

    :param value: a csp header to be parsed.
    :param on_update: an optional callable that is called every time a value
                      on the object is changed.
    :param cls: the class for the returned object.  By default
                :class:`~werkzeug.datastructures.ContentSecurityPolicy` is used.
    :return: a `cls` object.
    """

    if cls is None:
        cls = ContentSecurityPolicy
    if value is None:
        return cls(None, on_update)
    items = []
    for policy in value.split(";"):
        policy = policy.strip()
        # Ignore badly formatted policies (no space)
        if " " in policy:
            directive, value = policy.strip().split(" ", 1)
            items.append((directive.strip(), value.strip()))
    return cls(items, on_update)


def parse_set_header(
    value: Optional[str], on_update: Optional[Callable] = None
) -> "HeaderSet":
    """Parse a set-like header and return a
    :class:`~werkzeug.datastructures.HeaderSet` object:

    >>> hs = parse_set_header('token, "quoted value"')

    The return value is an object that treats the items case-insensitively
    and keeps the order of the items:

    >>> 'TOKEN' in hs
    True
    >>> hs.index('quoted value')
    1
    >>> hs
    HeaderSet(['token', 'quoted value'])

    To create a header from the :class:`HeaderSet` again, use the
    :func:`dump_header` function.

    :param value: a set header to be parsed.
    :param on_update: an optional callable that is called every time a
                      value on the :class:`~werkzeug.datastructures.HeaderSet`
                      object is changed.
    :return: a :class:`~werkzeug.datastructures.HeaderSet`
    """
    if not value:
        return HeaderSet(None, on_update)
    return HeaderSet(parse_list_header(value), on_update)


def parse_authorization_header(value: Optional[str],) -> Optional["Authorization"]:
    """Parse an HTTP basic/digest authorization header transmitted by the web
    browser.  The return value is either `None` if the header was invalid or
    not given, otherwise an :class:`~werkzeug.datastructures.Authorization`
    object.

    :param value: the authorization header to parse.
    :return: a :class:`~werkzeug.datastructures.Authorization` object or `None`.
    """
    if not value:
        return None
    value = wsgi_to_bytes(value)
    try:
        auth_type, auth_info = value.split(None, 1)
        auth_type = auth_type.lower()
    except ValueError:
        return None
    if auth_type == b"basic":
        try:
            username, password = base64.b64decode(auth_info).split(b":", 1)
        except Exception:
            return None
        try:
            return Authorization(
                "basic",
                {
                    "username": _to_str(username, _basic_auth_charset),
                    "password": _to_str(password, _basic_auth_charset),
                },
            )
        except UnicodeDecodeError:
            return None
    elif auth_type == b"digest":
        auth_map = parse_dict_header(auth_info)
        for key in "username", "realm", "nonce", "uri", "response":
            if key not in auth_map:
                return None
        if "qop" in auth_map:
            if not auth_map.get("nc") or not auth_map.get("cnonce"):
                return None
        return Authorization("digest", auth_map)
    return None


def parse_www_authenticate_header(
    value: Optional[str], on_update: Optional[Callable] = None
) -> "WWWAuthenticate":
    """Parse an HTTP WWW-Authenticate header into a
    :class:`~werkzeug.datastructures.WWWAuthenticate` object.

    :param value: a WWW-Authenticate header to parse.
    :param on_update: an optional callable that is called every time a value
                      on the :class:`~werkzeug.datastructures.WWWAuthenticate`
                      object is changed.
    :return: a :class:`~werkzeug.datastructures.WWWAuthenticate` object.
    """
    if not value:
        return WWWAuthenticate(on_update=on_update)
    try:
        auth_type, auth_info = value.split(None, 1)
        auth_type = auth_type.lower()
    except (ValueError, AttributeError):
        return WWWAuthenticate(value.strip().lower(), on_update=on_update)
    return WWWAuthenticate(auth_type, parse_dict_header(auth_info), on_update)


def parse_if_range_header(value: Optional[str]) -> "IfRange":
    """Parses an if-range header which can be an etag or a date.  Returns
    a :class:`~werkzeug.datastructures.IfRange` object.

    .. versionadded:: 0.7
    """
    if not value:
        return IfRange()
    date = parse_date(value)
    if date is not None:
        return IfRange(date=date)
    # drop weakness information
    return IfRange(unquote_etag(value)[0])


def parse_range_header(
    value: Optional[str], make_inclusive: bool = True
) -> Optional["Range"]:
    """Parses a range header into a :class:`~werkzeug.datastructures.Range`
    object.  If the header is missing or malformed `None` is returned.
    `ranges` is a list of ``(start, stop)`` tuples where the ranges are
    non-inclusive.

    .. versionadded:: 0.7
    """
    if not value or "=" not in value:
        return None

    ranges = []
    last_end = 0
    units, rng = value.split("=", 1)
    units = units.strip().lower()

    for item in rng.split(","):
        item = item.strip()
        if "-" not in item:
            return None
        if item.startswith("-"):
            if last_end < 0:
                return None
            try:
                begin = int(item)
            except ValueError:
                return None
            end = None
            last_end = -1
        elif "-" in item:
            begin, end = item.split("-", 1)  # type: ignore
            begin = begin.strip()  # type: ignore
            end = end.strip()
            if not begin.isdigit():  # type: ignore
                return None
            begin = int(begin)
            if begin < last_end or last_end < 0:
                return None
            if end:
                if not end.isdigit():
                    return None
                end = int(end) + 1  # type: ignore
                if begin >= end:  # type: ignore
                    return None
            else:
                end = None
            last_end = end  # type: ignore
        ranges.append((begin, end))

    return Range(units, ranges)  # type: ignore


def parse_content_range_header(
    value: str, on_update: Optional[Callable] = None
) -> Optional["ContentRange"]:
    """Parses a range header into a
    :class:`~werkzeug.datastructures.ContentRange` object or `None` if
    parsing is not possible.

    .. versionadded:: 0.7

    :param value: a content range header to be parsed.
    :param on_update: an optional callable that is called every time a value
                      on the :class:`~werkzeug.datastructures.ContentRange`
                      object is changed.
    """
    if value is None:
        return None
    try:
        units, rangedef = (value or "").strip().split(None, 1)
    except ValueError:
        return None

    if "/" not in rangedef:
        return None
    rng, length = rangedef.split("/", 1)
    if length == "*":
        length = None
    elif length.isdigit():
        length = int(length)  # type: ignore
    else:
        return None

    if rng == "*":
        return ContentRange(
            units, None, None, length, on_update=on_update  # type: ignore
        )
    elif "-" not in rng:
        return None

    start, stop = rng.split("-", 1)
    try:
        start = int(start)  # type: ignore
        stop = int(stop) + 1  # type: ignore
    except ValueError:
        return None

    if is_byte_range_valid(start, stop, length):  # type: ignore
        return ContentRange(
            units, start, stop, length, on_update=on_update  # type: ignore
        )

    return None


def quote_etag(etag: str, weak: bool = False) -> str:
    """Quote an etag.

    :param etag: the etag to quote.
    :param weak: set to `True` to tag it "weak".
    """
    if '"' in etag:
        raise ValueError("invalid etag")
    etag = f'"{etag}"'
    if weak:
        etag = f"W/{etag}"
    return etag


def unquote_etag(etag: Optional[str],) -> Union[Tuple[str, bool], Tuple[None, None]]:
    """Unquote a single etag:

    >>> unquote_etag('W/"bar"')
    ('bar', True)
    >>> unquote_etag('"bar"')
    ('bar', False)

    :param etag: the etag identifier to unquote.
    :return: a ``(etag, weak)`` tuple.
    """
    if not etag:
        return None, None
    etag = etag.strip()
    weak = False
    if etag.startswith(("W/", "w/")):
        weak = True
        etag = etag[2:]
    if etag[:1] == etag[-1:] == '"':
        etag = etag[1:-1]
    return etag, weak


def parse_etags(value: Optional[str]) -> "ETags":
    """Parse an etag header.

    :param value: the tag header to parse
    :return: an :class:`~werkzeug.datastructures.ETags` object.
    """
    if not value:
        return ETags()
    strong = []
    weak = []
    end = len(value)
    pos = 0
    while pos < end:
        match = _etag_re.match(value, pos)
        if match is None:
            break
        is_weak, quoted, raw = match.groups()
        if raw == "*":
            return ETags(star_tag=True)
        elif quoted:
            raw = quoted
        if is_weak:
            weak.append(raw)
        else:
            strong.append(raw)
        pos = match.end()
    return ETags(strong, weak)


def generate_etag(data: bytes) -> str:
    """Generate an etag for some data."""
    return md5(data).hexdigest()


def parse_date(value: Optional[str]) -> Optional[datetime]:
    """Parse one of the following date formats into a datetime object:

    .. sourcecode:: text

        Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
        Sunday, 06-Nov-94 08:49:37 GMT ; RFC 850, obsoleted by RFC 1036
        Sun Nov  6 08:49:37 1994       ; ANSI C's asctime() format

    If parsing fails the return value is `None`.

    :param value: a string with a supported date format.
    :return: a :class:`datetime.datetime` object.
    """
    if value:
        t = parsedate_tz(value.strip())
        if t is not None:
            try:
                year = t[0]
                # unfortunately that function does not tell us if two digit
                # years were part of the string, or if they were prefixed
                # with two zeroes.  So what we do is to assume that 69-99
                # refer to 1900, and everything below to 2000
                if 0 <= year <= 68:
                    year += 2000
                elif 69 <= year <= 99:
                    year += 1900
                return datetime(*((year,) + t[1:7])) - timedelta(seconds=t[-1] or 0)
            except (ValueError, OverflowError):
                return None
    return None


def _dump_date(
    d: Optional[Union[float, datetime, int, struct_time]], delim: str
) -> str:
    """Used for `http_date` and `cookie_date`."""
    if d is None:
        d = gmtime()
    elif isinstance(d, datetime):
        d = d.utctimetuple()
    elif isinstance(d, (int, float)):
        d = gmtime(d)
    weekday = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[d.tm_wday]
    month = (
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    )[d.tm_mon - 1]
    return (
        f"{weekday}, {d.tm_mday:02d}{delim}{month}{delim}{d.tm_year:04d}"
        f" {d.tm_hour:02d}:{d.tm_min:02d}:{d.tm_sec:02d} GMT"
    )


def cookie_date(expires: Optional[Union[datetime, int, float]] = None) -> str:
    """Formats the time to ensure compatibility with Netscape's cookie
    standard.

    Accepts a floating point number expressed in seconds since the epoch in, a
    datetime object or a timetuple.  All times in UTC.  The :func:`parse_date`
    function can be used to parse such a date.

    Outputs a string in the format ``Wdy, DD-Mon-YYYY HH:MM:SS GMT``.

    :param expires: If provided that date is used, otherwise the current.
    """
    return _dump_date(expires, "-")


def http_date(timestamp: Optional[Union[float, datetime, int]] = None) -> str:
    """Formats the time to match the RFC1123 date format.

    Accepts a floating point number expressed in seconds since the epoch in, a
    datetime object or a timetuple.  All times in UTC.  The :func:`parse_date`
    function can be used to parse such a date.

    Outputs a string in the format ``Wdy, DD Mon YYYY HH:MM:SS GMT``.

    :param timestamp: If provided that date is used, otherwise the current.
    """
    return _dump_date(timestamp, " ")


def parse_age(value: Optional[str] = None) -> timedelta:
    """Parses a base-10 integer count of seconds into a timedelta.

    If parsing fails, the return value is `None`.

    :param value: a string consisting of an integer represented in base-10
    :return: a :class:`datetime.timedelta` object or `None`.
    """
    if not value:
        return None
    try:
        seconds = int(value)
    except ValueError:
        return None
    if seconds < 0:
        return None
    try:
        return timedelta(seconds=seconds)
    except OverflowError:
        return None


def dump_age(age: Optional[Union[timedelta, int]] = None) -> Optional[str]:
    """Formats the duration as a base-10 integer.

    :param age: should be an integer number of seconds,
                a :class:`datetime.timedelta` object, or,
                if the age is unknown, `None` (default).
    """
    if age is None:
        return None
    if isinstance(age, timedelta):
        age = age.total_seconds()  # type: ignore
    age = int(age)  # type: ignore
    if age < 0:
        raise ValueError("age cannot be negative")

    return str(age)


def is_resource_modified(
    environ: WSGIEnvironment,
    etag: Optional[str] = None,
    data: Optional[Union[bytes, str]] = None,
    last_modified: Optional[datetime] = None,
    ignore_if_range: bool = True,
) -> bool:
    """Convenience method for conditional requests.

    :param environ: the WSGI environment of the request to be checked.
    :param etag: the etag for the response for comparison.
    :param data: or alternatively the data of the response to automatically
                 generate an etag using :func:`generate_etag`.
    :param last_modified: an optional date of the last modification.
    :param ignore_if_range: If `False`, `If-Range` header will be taken into
                            account.
    :return: `True` if the resource was modified, otherwise `False`.

    .. versionchanged:: 1.0.0
        The check is run for methods other than ``GET`` and ``HEAD``.
    """
    if etag is None and data is not None:
        etag = generate_etag(data)  # type: ignore
    elif data is not None:
        raise TypeError("both data and etag given")

    unmodified = False
    if isinstance(last_modified, str):
        last_modified = parse_date(last_modified)

    # ensure that microsecond is zero because the HTTP spec does not transmit
    # that either and we might have some false positives.  See issue #39
    if last_modified is not None:
        last_modified = last_modified.replace(microsecond=0)

    if_range = None
    if not ignore_if_range and "HTTP_RANGE" in environ:
        # https://tools.ietf.org/html/rfc7233#section-3.2
        # A server MUST ignore an If-Range header field received in a request
        # that does not contain a Range header field.
        if_range = parse_if_range_header(environ.get("HTTP_IF_RANGE"))

    if if_range is not None and if_range.date is not None:
        modified_since = if_range.date
    else:
        modified_since = parse_date(environ.get("HTTP_IF_MODIFIED_SINCE"))

    if modified_since and last_modified and last_modified <= modified_since:
        unmodified = True

    if etag:
        etag, _ = unquote_etag(etag)
        if if_range is not None and if_range.etag is not None:
            unmodified = parse_etags(if_range.etag).contains(etag)
        else:
            if_none_match = parse_etags(environ.get("HTTP_IF_NONE_MATCH"))
            if if_none_match:
                # https://tools.ietf.org/html/rfc7232#section-3.2
                # "A recipient MUST use the weak comparison function when comparing
                # entity-tags for If-None-Match"
                unmodified = if_none_match.contains_weak(etag)

            # https://tools.ietf.org/html/rfc7232#section-3.1
            # "Origin server MUST use the strong comparison function when
            # comparing entity-tags for If-Match"
            if_match = parse_etags(environ.get("HTTP_IF_MATCH"))
            if if_match:
                unmodified = not if_match.is_strong(etag)

    return not unmodified


def remove_entity_headers(
    headers: "AnyHeaders", allowed: Tuple[str, str] = ("expires", "content-location"),
) -> None:
    """Remove all entity headers from a list or :class:`Headers` object.  This
    operation works in-place.  `Expires` and `Content-Location` headers are
    by default not removed.  The reason for this is :rfc:`2616` section
    10.3.5 which specifies some entity headers that should be sent.

    .. versionchanged:: 0.5
       added `allowed` parameter.

    :param headers: a list or :class:`Headers` object.
    :param allowed: a list of headers that should still be allowed even though
                    they are entity headers.
    """
    allowed = {x.lower() for x in allowed}
    headers[:] = [
        (key, value)
        for key, value in headers
        if not is_entity_header(key) or key.lower() in allowed
    ]


def remove_hop_by_hop_headers(headers: "AnyHeaders") -> None:
    """Remove all HTTP/1.1 "Hop-by-Hop" headers from a list or
    :class:`Headers` object.  This operation works in-place.

    .. versionadded:: 0.5

    :param headers: a list or :class:`Headers` object.
    """
    headers[:] = [
        (key, value) for key, value in headers if not is_hop_by_hop_header(key)
    ]


def is_entity_header(header: str) -> bool:
    """Check if a header is an entity header.

    .. versionadded:: 0.5

    :param header: the header to test.
    :return: `True` if it's an entity header, `False` otherwise.
    """
    return header.lower() in _entity_headers


def is_hop_by_hop_header(header: str) -> bool:
    """Check if a header is an HTTP/1.1 "Hop-by-Hop" header.

    .. versionadded:: 0.5

    :param header: the header to test.
    :return: `True` if it's an HTTP/1.1 "Hop-by-Hop" header, `False` otherwise.
    """
    return header.lower() in _hop_by_hop_headers


@overload
def parse_cookie(
    header: Union[WSGIEnvironment, str], charset: str, errors: str, cls: None,
) -> "MultiDict":
    ...


@overload
def parse_cookie(
    header: Union[WSGIEnvironment, str], charset: str, errors: str, cls: Type[dict],
) -> dict:
    ...


def parse_cookie(header, charset="utf-8", errors="replace", cls=None):
    """Parse a cookie from a string or WSGI environ.

    The same key can be provided multiple times, the values are stored
    in-order. The default :class:`MultiDict` will have the first value
    first, and all values can be retrieved with
    :meth:`MultiDict.getlist`.

    :param header: The cookie header as a string, or a WSGI environ dict
        with a ``HTTP_COOKIE`` key.
    :param charset: The charset for the cookie values.
    :param errors: The error behavior for the charset decoding.
    :param cls: A dict-like class to store the parsed cookies in.
        Defaults to :class:`MultiDict`.

    .. versionchanged:: 1.0.0
        Returns a :class:`MultiDict` instead of a
        ``TypeConversionDict``.

    .. versionchanged:: 0.5
       Returns a :class:`TypeConversionDict` instead of a regular dict.
       The ``cls`` parameter was added.
    """
    if isinstance(header, dict):
        header = header.get("HTTP_COOKIE", "")
    elif header is None:
        header = ""

    # PEP 3333 sends headers through the environ as latin1 decoded
    # strings. Encode strings back to bytes for parsing.
    if isinstance(header, str):
        header = header.encode("latin1", "replace")

    if cls is None:
        cls = MultiDict

    def _parse_pairs():
        for key, val in _cookie_parse_impl(header):
            key = _to_str(key, charset, errors, allow_none_charset=True)
            if not key:
                continue
            val = _to_str(val, charset, errors, allow_none_charset=True)
            yield key, val

    return cls(_parse_pairs())


def dump_cookie(
    key: str,
    value: Union[str, bytes] = "",
    max_age: Optional[Union[int, timedelta]] = None,
    expires: Optional[Union[float, int, datetime]] = None,
    path: str = "/",
    domain: Optional[str] = None,
    secure: bool = False,
    httponly: bool = False,
    charset: str = "utf-8",
    sync_expires: bool = True,
    max_size: int = 4093,
    samesite: Optional[str] = None,
) -> str:
    """Create a Set-Cookie header without the ``Set-Cookie`` prefix.

    The return value is usually restricted to ascii as the vast majority
    of values are properly escaped, but that is no guarantee. It's
    tunneled through latin1 as required by :pep:`3333`.

    The return value is not ASCII safe if the key contains unicode
    characters.  This is technically against the specification but
    happens in the wild.  It's strongly recommended to not use
    non-ASCII values for the keys.

    :param max_age: should be a number of seconds, or `None` (default) if
                    the cookie should last only as long as the client's
                    browser session.  Additionally `timedelta` objects
                    are accepted, too.
    :param expires: should be a `datetime` object or unix timestamp.
    :param path: limits the cookie to a given path, per default it will
                 span the whole domain.
    :param domain: Use this if you want to set a cross-domain cookie. For
                   example, ``domain=".example.com"`` will set a cookie
                   that is readable by the domain ``www.example.com``,
                   ``foo.example.com`` etc. Otherwise, a cookie will only
                   be readable by the domain that set it.
    :param secure: The cookie will only be available via HTTPS
    :param httponly: disallow JavaScript to access the cookie.  This is an
                     extension to the cookie standard and probably not
                     supported by all browsers.
    :param charset: the encoding for string values.
    :param sync_expires: automatically set expires if max_age is defined
                         but expires not.
    :param max_size: Warn if the final header value exceeds this size. The
        default, 4093, should be safely `supported by most browsers
        <cookie_>`_. Set to 0 to disable this check.
    :param samesite: Limits the scope of the cookie such that it will
        only be attached to requests if those requests are same-site.

    .. _`cookie`: http://browsercookielimits.squawky.net/

    .. versionchanged:: 1.0.0
        The string ``'None'`` is accepted for ``samesite``.
    """
    key = _to_bytes(key, charset)
    value = _to_bytes(value, charset)

    if path is not None:
        from .urls import iri_to_uri

        path = iri_to_uri(path, charset)
    domain = _make_cookie_domain(domain)
    if isinstance(max_age, timedelta):
        max_age = (max_age.days * 60 * 60 * 24) + max_age.seconds
    if expires is not None:
        if not isinstance(expires, str):
            expires = cookie_date(expires)  # type: ignore
    elif max_age is not None and sync_expires:
        expires = _to_bytes(cookie_date(time() + max_age))  # type: ignore

    if samesite is not None:
        samesite = samesite.title()

        if samesite not in {"Strict", "Lax", "None"}:
            raise ValueError("SameSite must be 'Strict', 'Lax', or 'None'.")

    buf = [key + b"=" + _cookie_quote(value)]

    # XXX: In theory all of these parameters that are not marked with `None`
    # should be quoted.  Because stdlib did not quote it before I did not
    # want to introduce quoting there now.
    for k, v, q in (
        (b"Domain", domain, True),
        (b"Expires", expires, False),
        (b"Max-Age", max_age, False),
        (b"Secure", secure, None),
        (b"HttpOnly", httponly, None),
        (b"Path", path, False),
        (b"SameSite", samesite, False),
    ):
        if q is None:
            if v:
                buf.append(k)
            continue

        if v is None:
            continue

        tmp = bytearray(k)
        if not isinstance(v, (bytes, bytearray)):
            v = _to_bytes(str(v), charset)
        if q:
            v = _cookie_quote(v)
        tmp += b"=" + v
        buf.append(bytes(tmp))

    # The return value will be an incorrectly encoded latin1 header for
    # consistency with the headers object.
    rv = b"; ".join(buf)
    rv = rv.decode("latin1")

    # Warn if the final value of the cookie is larger than the limit. If the
    # cookie is too large, then it may be silently ignored by the browser,
    # which can be quite hard to debug.
    cookie_size = len(rv)

    if max_size and cookie_size > max_size:
        value_size = len(value)
        warnings.warn(
            f'The "{key}" cookie is too large: the value was'  # type: ignore
            f" {value_size} bytes but the"
            f" header required {cookie_size - value_size} extra bytes. The final size"
            f" was {cookie_size} bytes but the limit is {max_size} bytes. Browsers may"
            f" silently ignore cookies larger than this.",
            stacklevel=2,
        )

    return rv


def is_byte_range_valid(
    start: Optional[int], stop: Optional[int], length: Optional[int]
) -> bool:
    """Checks if a given byte content range is valid for the given length.

    .. versionadded:: 0.7
    """
    if (start is None) != (stop is None):
        return False
    elif start is None:
        return length is None or length >= 0
    elif length is None:
        return 0 <= start < stop
    elif start >= stop:
        return False
    return 0 <= start < length


# circular dependencies
from .datastructures import Accept
from .datastructures import Authorization
from .datastructures import ContentRange
from .datastructures import ContentSecurityPolicy
from .datastructures import ETags
from .datastructures import HeaderSet
from .datastructures import IfRange
from .datastructures import MultiDict
from .datastructures import Range
from .datastructures import RequestCacheControl
from .datastructures import WWWAuthenticate
