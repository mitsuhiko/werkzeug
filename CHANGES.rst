.. currentmodule:: werkzeug

Version 3.2.0
-------------

Unreleased

- The ``RequestRedirect`` exception now exposes ``new_path`` that
  contains the request path used to compute the ``new_url``.

Version 3.1.3
-------------

Released 2024-11-08

-   Initial data passed to ``MultiDict`` and similar interfaces only accepts
    ``list``, ``tuple``, or ``set`` when passing multiple values. It had been
    changed to accept any ``Collection``, but this matched types that should be
    treated as single values, such as ``bytes``. :issue:`2994`
-   When the ``Host`` header is not set and ``Request.host`` falls back to the
    WSGI ``SERVER_NAME`` value, if that value is an IPv6 address it is wrapped
    in ``[]`` to match the ``Host`` header. :issue:`2993`


Version 3.1.2
-------------

Released 2024-11-04

-   Improve type annotation for ``TypeConversionDict.get`` to allow the ``type``
    parameter to be a callable. :issue:`2988`
-   ``Headers`` does not inherit from ``MutableMapping``, as it is does not
    exactly match that interface. :issue:`2989`


Version 3.1.1
-------------

Released 2024-11-01

-   Fix an issue that caused ``str(Request.headers)`` to always appear empty.
    :issue:`2985`


Version 3.1.0
-------------

Released 2024-10-31

-   Drop support for Python 3.8. :pr:`2966`
-   Remove previously deprecated code. :pr:`2967`
-   ``Request.max_form_memory_size`` defaults to 500kB instead of unlimited.
    Non-file form fields over this size will cause a ``RequestEntityTooLarge``
    error. :issue:`2964`
-   ``OrderedMultiDict`` and ``ImmutableOrderedMultiDict`` are deprecated.
    Use ``MultiDict`` and ``ImmutableMultiDict`` instead. :issue:`2968`
-   Behavior of properties on ``request.cache_control`` and
    ``response.cache_control`` has been significantly adjusted.

    -   Dict values are always ``str | None``. Setting properties will convert
        the value to a string. Setting a property to ``False`` is equivalent to
        setting it to ``None``. Getting typed properties will return ``None`` if
        conversion raises ``ValueError``, rather than the string. :issue:`2980`
    -   ``max_age`` is ``None`` if present without a value, rather than ``-1``.
        :issue:`2980`
    -   ``no_cache`` is a boolean for requests, it is ``True`` instead of
        ``"*"`` when present. It remains a string for responses. :issue:`2980`
    -   ``max_stale`` is ``True`` if present without a value, rather
        than ``"*"``. :issue:`2980`
    -   ``no_transform`` is a boolean. Previously it was mistakenly always
        ``None``. :issue:`2881`
    -   ``min_fresh`` is ``None`` if present without a value, rather than
        ``"*"``. :issue:`2881`
    -   ``private`` is ``True`` if present without a value, rather than ``"*"``.
        :issue:`2980`
    -   Added the ``must_understand`` property. :issue:`2881`
    -   Added the ``stale_while_revalidate``, and ``stale_if_error``
        properties. :issue:`2948`
    -   Type annotations more accurately reflect the values. :issue:`2881`

-   Support Cookie CHIPS (Partitioned Cookies). :issue:`2797`
-   Add 421 ``MisdirectedRequest`` HTTP exception. :issue:`2850`
-   Increase default work factor for PBKDF2 to 1,000,000 iterations.
    :issue:`2969`
-   Inline annotations for ``datastructures``, removing stub files.
    :issue:`2970`
-   ``MultiDict.getlist`` catches ``TypeError`` in addition to ``ValueError``
    when doing type conversion. :issue:`2976`
-   Implement ``|`` and ``|=`` operators for ``MultiDict``, ``Headers``, and
    ``CallbackDict``, and disallow ``|=`` on immutable types. :issue:`2977`


Version 3.0.6
-------------

Released 2024-10-25

-   Fix how ``max_form_memory_size`` is applied when parsing large non-file
    fields. :ghsa:`q34m-jh98-gwm2`
-   ``safe_join`` catches certain paths on Windows that were not caught by
    ``ntpath.isabs`` on Python < 3.11. :ghsa:`f9vj-2wh5-fj8j`


Version 3.0.5
-------------

Released 2024-10-24

-   The Watchdog reloader ignores file closed no write events. :issue:`2945`
-   Logging works with client addresses containing an IPv6 scope :issue:`2952`
-   Ignore invalid authorization parameters. :issue:`2955`
-   Improve type annotation fore ``SharedDataMiddleware``. :issue:`2958`
-   Compatibility with Python 3.13 when generating debugger pin and the current
    UID does not have an associated name. :issue:`2957`


Version 3.0.4
-------------

Released 2024-08-21

-   Restore behavior where parsing `multipart/x-www-form-urlencoded` data with
    invalid UTF-8 bytes in the body results in no form data parsed rather than a
    413 error. :issue:`2930`
-   Improve ``parse_options_header`` performance when parsing unterminated
    quoted string values. :issue:`2904`
-   Debugger pin auth is synchronized across threads/processes when tracking
    failed entries. :issue:`2916`
-   Dev server handles unexpected `SSLEOFError` due to issue in Python < 3.13.
    :issue:`2926`
-   Debugger pin auth works when the URL already contains a query string.
    :issue:`2918`


Version 3.0.3
-------------

Released 2024-05-05

-   Only allow ``localhost``, ``.localhost``, ``127.0.0.1``, or the specified
    hostname when running the dev server, to make debugger requests. Additional
    hosts can be added by using the debugger middleware directly. The debugger
    UI makes requests using the full URL rather than only the path.
    :ghsa:`2g68-c3qc-8985`
-   Make reloader more robust when ``""`` is in ``sys.path``. :pr:`2823`
-   Better TLS cert format with ``adhoc`` dev certs. :pr:`2891`
-   Inform Python < 3.12 how to handle ``itms-services`` URIs correctly, rather
    than using an overly-broad workaround in Werkzeug that caused some redirect
    URIs to be passed on without encoding. :issue:`2828`
-   Type annotation for ``Rule.endpoint`` and other uses of ``endpoint`` is
    ``Any``. :issue:`2836`
-   Make reloader more robust when ``""`` is in ``sys.path``. :pr:`2823`


Version 3.0.2
-------------

Released 2024-04-01

-   Ensure setting ``merge_slashes`` to ``False`` results in ``NotFound`` for
    repeated-slash requests against single slash routes. :issue:`2834`
-   Fix handling of ``TypeError`` in ``TypeConversionDict.get()`` to match
    ``ValueError``. :issue:`2843`
-   Fix ``response_wrapper`` type check in test client. :issue:`2831`
-   Make the return type of ``MultiPartParser.parse`` more precise.
    :issue:`2840`
-   Raise an error if converter arguments cannot be parsed. :issue:`2822`


Version 3.0.1
-------------

Released 2023-10-24

-   Fix slow multipart parsing for large parts potentially enabling DoS attacks.


Version 3.0.0
-------------

Released 2023-09-30

-   Remove previously deprecated code. :pr:`2768`
-   Deprecate the ``__version__`` attribute. Use feature detection, or
    ``importlib.metadata.version("werkzeug")``, instead. :issue:`2770`
-   ``generate_password_hash`` uses scrypt by default. :issue:`2769`
-   Add the ``"werkzeug.profiler"`` item to the  WSGI ``environ`` dictionary
    passed to `ProfilerMiddleware`'s `filename_format` function. It contains
    the ``elapsed`` and ``time`` values for the profiled request. :issue:`2775`
-   Explicitly marked the PathConverter as non path isolating. :pr:`2784`


Version 2.3.8
-------------

Released 2023-11-08

-   Fix slow multipart parsing for large parts potentially enabling DoS
    attacks.


Version 2.3.7
-------------

Released 2023-08-14

-   Use ``flit_core`` instead of ``setuptools`` as build backend.
-   Fix parsing of multipart bodies. :issue:`2734`
-   Adjust index of last newline in data start. :issue:`2761`
-   Parsing ints from header values strips spacing first. :issue:`2734`
-   Fix empty file streaming when testing. :issue:`2740`
-   Clearer error message when URL rule does not start with slash. :pr:`2750`
-   ``Accept`` ``q`` value can be a float without a decimal part. :issue:`2751`


Version 2.3.6
-------------

Released 2023-06-08

-   ``FileStorage.content_length`` does not fail if the form data did not provide a
    value. :issue:`2726`


Version 2.3.5
-------------

Released 2023-06-07

-   Python 3.12 compatibility. :issue:`2704`
-   Fix handling of invalid base64 values in ``Authorization.from_header``. :issue:`2717`
-   The debugger escapes the exception message in the page title. :pr:`2719`
-   When binding ``routing.Map``, a long IDNA ``server_name`` with a port does not fail
    encoding. :issue:`2700`
-   ``iri_to_uri`` shows a deprecation warning instead of an error when passing bytes.
    :issue:`2708`
-   When parsing numbers in HTTP request headers such as ``Content-Length``, only ASCII
    digits are accepted rather than any format that Python's ``int`` and ``float``
    accept. :issue:`2716`


Version 2.3.4
-------------

Released 2023-05-08

-   ``Authorization.from_header`` and ``WWWAuthenticate.from_header`` detects tokens
    that end with base64 padding (``=``). :issue:`2685`
-   Remove usage of ``warnings.catch_warnings``. :issue:`2690`
-   Remove ``max_form_parts`` restriction from standard form data parsing and only use
    if for multipart content. :pr:`2694`
-   ``Response`` will avoid converting the ``Location`` header in some cases to preserve
    invalid URL schemes like ``itms-services``. :issue:`2691`


Version 2.3.3
-------------

Released 2023-05-01

-   Fix parsing of large multipart bodies. Remove invalid leading newline, and restore
    parsing speed. :issue:`2658, 2675`
-   The cookie ``Path`` attribute is set to ``/`` by default again, to prevent clients
    from falling back to RFC 6265's ``default-path`` behavior. :issue:`2672, 2679`


Version 2.3.2
-------------

Released 2023-04-28

-   Parse the cookie ``Expires`` attribute correctly in the test client. :issue:`2669`
-   ``max_content_length`` can only be enforced on streaming requests if the server
    sets ``wsgi.input_terminated``. :issue:`2668`


Version 2.3.1
-------------

Released 2023-04-27

-   Percent-encode plus (+) when building URLs and in test requests. :issue:`2657`
-   Cookie values don't quote characters defined in RFC 6265. :issue:`2659`
-   Include ``pyi`` files for ``datastructures`` type annotations. :issue:`2660`
-   ``Authorization`` and ``WWWAuthenticate`` objects can be compared for equality.
    :issue:`2665`


Version 2.3.0
-------------

Released 2023-04-25

-   Drop support for Python 3.7. :pr:`2648`
-   Remove previously deprecated code. :pr:`2592`
-   Passing bytes where strings are expected is deprecated, as well as the ``charset``
    and ``errors`` parameters in many places. Anywhere that was annotated, documented,
    or tested to accept bytes shows a warning. Removing this artifact of the transition
    from Python 2 to 3 removes a significant amount of overhead in instance checks and
    encoding cycles. In general, always work with UTF-8, the modern HTML, URL, and HTTP
    standards all strongly recommend this. :issue:`2602`
-   Deprecate the ``werkzeug.urls`` module, except for the ``uri_to_iri`` and
    ``iri_to_uri`` functions. Use the ``urllib.parse`` library instead. :issue:`2600`
-   Update which characters are considered safe when using percent encoding in URLs,
    based on the WhatWG URL Standard. :issue:`2601`
-   Update which characters are considered safe when using percent encoding for Unicode
    filenames in downloads. :issue:`2598`
-   Deprecate the ``safe_conversion`` parameter of ``iri_to_uri``. The ``Location``
    header is converted to IRI using the same process as everywhere else. :issue:`2609`
-   Deprecate ``werkzeug.wsgi.make_line_iter`` and ``make_chunk_iter``. :pr:`2613`
-   Use modern packaging metadata with ``pyproject.toml`` instead of ``setup.cfg``.
    :pr:`2574`
-   ``Request.get_json()`` will raise a ``415 Unsupported Media Type`` error if the
    ``Content-Type`` header is not ``application/json``, instead of a generic 400.
    :issue:`2550`
-   A URL converter's ``part_isolating`` defaults to ``False`` if its ``regex`` contains
    a ``/``. :issue:`2582`
-   A custom converter's regex can have capturing groups without breaking the router.
    :pr:`2596`
-   The reloader can pick up arguments to ``python`` like ``-X dev``, and does not
    require heuristics to determine how to reload the command. Only available
    on Python >= 3.10. :issue:`2589`
-   The Watchdog reloader ignores file opened events. Bump the minimum version of
    Watchdog to 2.3.0. :issue:`2603`
-   When using a Unix socket for the development server, the path can start with a dot.
    :issue:`2595`
-   Increase default work factor for PBKDF2 to 600,000 iterations. :issue:`2611`
-   ``parse_options_header`` is 2-3 times faster. It conforms to :rfc:`9110`, some
    invalid parts that were previously accepted are now ignored. :issue:`1628`
-   The ``is_filename`` parameter to ``unquote_header_value`` is deprecated. :pr:`2614`
-   Deprecate the ``extra_chars`` parameter and passing bytes to ``quote_header_value``,
    the ``allow_token`` parameter to ``dump_header``, and the ``cls`` parameter and
    passing bytes to ``parse_dict_header``. :pr:`2618`
-   Improve ``parse_accept_header`` implementation. Parse according to :rfc:`9110`.
    Discard items with invalid ``q`` values. :issue:`1623`
-   ``quote_header_value`` quotes the empty string. :pr:`2618`
-   ``dump_options_header`` skips ``None`` values rather than using a bare key.
    :pr:`2618`
-   ``dump_header`` and ``dump_options_header`` will not quote a value if the key ends
    with an asterisk ``*``.
-   ``parse_dict_header`` will decode values with charsets. :pr:`2618`
-   Refactor the ``Authorization`` and ``WWWAuthenticate`` header data structures.
    :issue:`1769`, :pr:`2619`

    -   Both classes have ``type``, ``parameters``, and ``token`` attributes. The
        ``token`` attribute supports auth schemes that use a single opaque token rather
        than ``key=value`` parameters, such as ``Bearer``.
    -   Neither class is a ``dict`` anymore, although they still implement getting,
        setting, and deleting ``auth[key]`` and ``auth.key`` syntax, as well as
        ``auth.get(key)`` and ``key in auth``.
    -   Both classes have a ``from_header`` class method. ``parse_authorization_header``
        and ``parse_www_authenticate_header`` are deprecated.
    -   The methods ``WWWAuthenticate.set_basic`` and ``set_digest`` are deprecated.
        Instead, an instance should be created and assigned to
        ``response.www_authenticate``.
    -   A list of instances can be assigned to ``response.www_authenticate`` to set
        multiple header values. However, accessing the property only returns the first
        instance.

-   Refactor ``parse_cookie`` and ``dump_cookie``. :pr:`2637`

    -   ``parse_cookie`` is up to 40% faster, ``dump_cookie`` is up to 60% faster.
    -   Passing bytes to ``parse_cookie`` and ``dump_cookie`` is deprecated. The
        ``dump_cookie`` ``charset`` parameter is deprecated.
    -   ``dump_cookie`` allows ``domain`` values that do not include a dot ``.``, and
        strips off a leading dot.
    -   ``dump_cookie`` does not set ``path="/"`` unnecessarily by default.

-   Refactor the test client cookie implementation. :issue:`1060, 1680`

    -   The ``cookie_jar`` attribute is deprecated. ``http.cookiejar`` is no longer used
        for storage.
    -   Domain and path matching is used when sending cookies in requests. The
        ``domain`` and ``path`` parameters default to ``localhost`` and ``/``.
    -   Added a ``get_cookie`` method to inspect cookies.
    -   Cookies have ``decoded_key`` and ``decoded_value`` attributes to match what the
        app sees rather than the encoded values a client would see.
    -   The first positional ``server_name`` parameter to ``set_cookie`` and
        ``delete_cookie`` is deprecated. Use the ``domain`` parameter instead.
    -   Other parameters to ``delete_cookie`` besides ``domain``, ``path``, and
        ``value`` are deprecated.

-   If ``request.max_content_length`` is set, it is checked immediately when accessing
    the stream, and while reading from the stream in general, rather than only during
    form parsing. :issue:`1513`
-   The development server, which must not be used in production, will exhaust the
    request stream up to 10GB or 1000 reads. This allows clients to see a 413 error if
    ``max_content_length`` is exceeded, instead of a "connection reset" failure.
    :pr:`2620`
-   The development server discards header keys that contain underscores ``_``, as they
    are ambiguous with dashes ``-`` in WSGI. :pr:`2622`
-   ``secure_filename`` looks for more Windows reserved file names. :pr:`2623`
-   Update type annotation for ``best_match`` to make ``default`` parameter clearer.
    :issue:`2625`
-   Multipart parser handles empty fields correctly. :issue:`2632`
-   The ``Map`` ``charset`` parameter and ``Request.url_charset`` property are
    deprecated. Percent encoding in URLs must always represent UTF-8 bytes. Invalid
    bytes are left percent encoded rather than replaced. :issue:`2602`
-   The ``Request.charset``, ``Request.encoding_errors``, ``Response.charset``, and
    ``Client.charset`` attributes are deprecated. Request and response data must always
    use UTF-8. :issue:`2602`
-   Header values that have charset information only allow ASCII, UTF-8, and ISO-8859-1.
    :pr:`2614, 2641`
-   Update type annotation for ``ProfilerMiddleware`` ``stream`` parameter.
    :issue:`2642`
-   Use postponed evaluation of annotations. :pr:`2644`
-   The development server escapes ASCII control characters in decoded URLs before
    logging the request to the terminal. :pr:`2652`
-   The ``FormDataParser`` ``parse_functions`` attribute and ``get_parse_func`` method,
    and the invalid ``application/x-url-encoded`` content type, are deprecated.
    :pr:`2653`
-   ``generate_password_hash`` supports scrypt. Plain hash methods are deprecated, only
    scrypt and pbkdf2 are supported. :issue:`2654`


Version 2.2.3
-------------

Released 2023-02-14

-   Ensure that URL rules using path converters will redirect with strict slashes when
    the trailing slash is missing. :issue:`2533`
-   Type signature for ``get_json`` specifies that return type is not optional when
    ``silent=False``. :issue:`2508`
-   ``parse_content_range_header`` returns ``None`` for a value like ``bytes */-1``
    where the length is invalid, instead of raising an ``AssertionError``. :issue:`2531`
-   Address remaining ``ResourceWarning`` related to the socket used by ``run_simple``.
    Remove ``prepare_socket``, which now happens when creating the server. :issue:`2421`
-   Update pre-existing headers for ``multipart/form-data`` requests with the test
    client. :issue:`2549`
-   Fix handling of header extended parameters such that they are no longer quoted.
    :issue:`2529`
-   ``LimitedStream.read`` works correctly when wrapping a stream that may not return
    the requested size in one ``read`` call. :issue:`2558`
-   A cookie header that starts with ``=`` is treated as an empty key and discarded,
    rather than stripping the leading ``==``.
-   Specify a maximum number of multipart parts, default 1000, after which a
    ``RequestEntityTooLarge`` exception is raised on parsing. This mitigates a DoS
    attack where a larger number of form/file parts would result in disproportionate
    resource use.



Version 2.2.2
-------------

Released 2022-08-08

-   Fix router to restore the 2.1 ``strict_slashes == False`` behaviour
    whereby leaf-requests match branch rules and vice
    versa. :pr:`2489`
-   Fix router to identify invalid rules rather than hang parsing them,
    and to correctly parse ``/`` within converter arguments. :pr:`2489`
-   Update subpackage imports in :mod:`werkzeug.routing` to use the
    ``import as`` syntax for explicitly re-exporting public attributes.
    :pr:`2493`
-   Parsing of some invalid header characters is more robust. :pr:`2494`
-   When starting the development server, a warning not to use it in a
    production deployment is always shown. :issue:`2480`
-   ``LocalProxy.__wrapped__`` is always set to the wrapped object when
    the proxy is unbound, fixing an issue in doctest that would cause it
    to fail. :issue:`2485`
-   Address one ``ResourceWarning`` related to the socket used by
    ``run_simple``. :issue:`2421`



Version 2.2.1
-------------

Released 2022-07-27

-   Fix router so that ``/path/`` will match a rule ``/path`` if strict
    slashes mode is disabled for the rule. :issue:`2467`
-   Fix router so that partial part matches are not allowed
    i.e. ``/2df`` does not match ``/<int>``. :pr:`2470`
-   Fix router static part weighting, so that simpler routes are matched
    before more complex ones. :issue:`2471`
-   Restore ``ValidationError`` to be importable from
    ``werkzeug.routing``. :issue:`2465`


Version 2.2.0
-------------

Released 2022-07-23

-   Deprecated ``get_script_name``, ``get_query_string``,
    ``peek_path_info``, ``pop_path_info``, and
    ``extract_path_info``. :pr:`2461`
-   Remove previously deprecated code. :pr:`2461`
-   Add MarkupSafe as a dependency and use it to escape values when
    rendering HTML. :issue:`2419`
-   Added the ``werkzeug.debug.preserve_context`` mechanism for
    restoring context-local data for a request when running code in the
    debug console. :pr:`2439`
-   Fix compatibility with Python 3.11 by ensuring that ``end_lineno``
    and ``end_col_offset`` are present on AST nodes. :issue:`2425`
-   Add a new faster URL matching router based on a state machine. If a custom converter
    needs to match a ``/`` it must set the class variable ``part_isolating = False``.
    :pr:`2433`
-   Fix branch leaf path masking branch paths when strict-slashes is
    disabled. :issue:`1074`
-   Names within options headers are always converted to lowercase. This
    matches :rfc:`6266` that the case is not relevant. :issue:`2442`
-   ``AnyConverter`` validates the value passed for it when building
    URLs. :issue:`2388`
-   The debugger shows enhanced error locations in tracebacks in Python
    3.11. :issue:`2407`
-   Added Sans-IO ``is_resource_modified`` and ``parse_cookie`` functions
    based on WSGI versions. :issue:`2408`
-   Added Sans-IO ``get_content_length`` function. :pr:`2415`
-   Don't assume a mimetype for test responses. :issue:`2450`
-   Type checking ``FileStorage`` accepts ``os.PathLike``. :pr:`2418`


Version 2.1.2
-------------

Released 2022-04-28

-   The development server does not set ``Transfer-Encoding: chunked``
    for 1xx, 204, 304, and HEAD responses. :issue:`2375`
-   Response HTML for exceptions and redirects starts with
    ``<!doctype html>`` and ``<html lang=en>``. :issue:`2390`
-   Fix ability to set some ``cache_control`` attributes to ``False``.
    :issue:`2379`
-   Disable ``keep-alive`` connections in the development server, which
    are not supported sufficiently by Python's ``http.server``.
    :issue:`2397`


Version 2.1.1
-------------

Released 2022-04-01

-   ``ResponseCacheControl.s_maxage`` converts its value to an int, like
    ``max_age``. :issue:`2364`


Version 2.1.0
-------------

Released 2022-03-28

-   Drop support for Python 3.6. :pr:`2277`
-   Using gevent or eventlet requires greenlet>=1.0 or PyPy>=7.3.7.
    ``werkzeug.locals`` and ``contextvars`` will not work correctly with
    older versions. :pr:`2278`
-   Remove previously deprecated code. :pr:`2276`

    -   Remove the non-standard ``shutdown`` function from the WSGI
        environ when running the development server. See the docs for
        alternatives.
    -   Request and response mixins have all been merged into the
        ``Request`` and ``Response`` classes.
    -   The user agent parser and the ``useragents`` module is removed.
        The ``user_agent`` module provides an interface that can be
        subclassed to add a parser, such as ua-parser. By default it
        only stores the whole string.
    -   The test client returns ``TestResponse`` instances and can no
        longer be treated as a tuple. All data is available as
        properties on the response.
    -   Remove ``locals.get_ident`` and related thread-local code from
        ``locals``, it no longer makes sense when moving to a
        contextvars-based implementation.
    -   Remove the ``python -m werkzeug.serving`` CLI.
    -   The ``has_key`` method on some mapping datastructures; use
        ``key in data`` instead.
    -   ``Request.disable_data_descriptor`` is removed, pass
        ``shallow=True`` instead.
    -   Remove the ``no_etag`` parameter from ``Response.freeze()``.
    -   Remove the ``HTTPException.wrap`` class method.
    -   Remove the ``cookie_date`` function. Use ``http_date`` instead.
    -   Remove the ``pbkdf2_hex``, ``pbkdf2_bin``, and ``safe_str_cmp``
        functions. Use equivalents in ``hashlib`` and ``hmac`` modules
        instead.
    -   Remove the ``Href`` class.
    -   Remove the ``HTMLBuilder`` class.
    -   Remove the ``invalidate_cached_property`` function. Use
        ``del obj.attr`` instead.
    -   Remove ``bind_arguments`` and ``validate_arguments``. Use
        :meth:`Signature.bind` and :func:`inspect.signature` instead.
    -   Remove ``detect_utf_encoding``, it's built-in to ``json.loads``.
    -   Remove ``format_string``, use :class:`string.Template` instead.
    -   Remove ``escape`` and ``unescape``. Use MarkupSafe instead.

-   The ``multiple`` parameter of ``parse_options_header`` is
    deprecated. :pr:`2357`
-   Rely on :pep:`538` and :pep:`540` to handle decoding file names
    with the correct filesystem encoding. The ``filesystem`` module is
    removed. :issue:`1760`
-   Default values passed to ``Headers`` are validated the same way
    values added later are. :issue:`1608`
-   Setting ``CacheControl`` int properties, such as ``max_age``, will
    convert the value to an int. :issue:`2230`
-   Always use ``socket.fromfd`` when restarting the dev server.
    :pr:`2287`
-   When passing a dict of URL values to ``Map.build``, list values do
    not filter out ``None`` or collapse to a single value. Passing a
    ``MultiDict`` does collapse single items. This undoes a previous
    change that made it difficult to pass a list, or ``None`` values in
    a list, to custom URL converters. :issue:`2249`
-   ``run_simple`` shows instructions for dealing with "address already
    in use" errors, including extra instructions for macOS. :pr:`2321`
-   Extend list of characters considered always safe in URLs based on
    :rfc:`3986`. :issue:`2319`
-   Optimize the stat reloader to avoid watching unnecessary files in
    more cases. The watchdog reloader is still recommended for
    performance and accuracy. :issue:`2141`
-   The development server uses ``Transfer-Encoding: chunked`` for
    streaming responses when it is configured for HTTP/1.1.
    :issue:`2090, 1327`, :pr:`2091`
-   The development server uses HTTP/1.1, which enables keep-alive
    connections and chunked streaming responses, when ``threaded`` or
    ``processes`` is enabled. :pr:`2323`
-   ``cached_property`` works for classes with ``__slots__`` if a
    corresponding ``_cache_{name}`` slot is added. :pr:`2332`
-   Refactor the debugger traceback formatter to use Python's built-in
    ``traceback`` module as much as possible. :issue:`1753`
-   The ``TestResponse.text`` property is a shortcut for
    ``r.get_data(as_text=True)``, for convenient testing against text
    instead of bytes. :pr:`2337`
-   ``safe_join`` ensures that the path remains relative if the trusted
    directory is the empty string. :pr:`2349`
-   Percent-encoded newlines (``%0a``), which are decoded by WSGI
    servers, are considered when routing instead of terminating the
    match early. :pr:`2350`
-   The test client doesn't set duplicate headers for ``CONTENT_LENGTH``
    and ``CONTENT_TYPE``. :pr:`2348`
-   ``append_slash_redirect`` handles ``PATH_INFO`` with internal
    slashes. :issue:`1972`, :pr:`2338`
-   The default status code for ``append_slash_redirect`` is 308 instead
    of 301. This preserves the request body, and matches a previous
    change to ``strict_slashes`` in routing. :issue:`2351`
-   Fix ``ValueError: I/O operation on closed file.`` with the test
    client when following more than one redirect. :issue:`2353`
-   ``Response.autocorrect_location_header`` is disabled by default.
    The ``Location`` header URL will remain relative, and exclude the
    scheme and domain, by default. :issue:`2352`
-   ``Request.get_json()`` will raise a 400 ``BadRequest`` error if the
    ``Content-Type`` header is not ``application/json``. This makes a
    very common source of confusion more visible. :issue:`2339`


Version 2.0.3
-------------

Released 2022-02-07

-   ``ProxyFix`` supports IPv6 addresses. :issue:`2262`
-   Type annotation for ``Response.make_conditional``,
    ``HTTPException.get_response``, and ``Map.bind_to_environ`` accepts
    ``Request`` in addition to ``WSGIEnvironment`` for the first
    parameter. :pr:`2290`
-   Fix type annotation for ``Request.user_agent_class``. :issue:`2273`
-   Accessing ``LocalProxy.__class__`` and ``__doc__`` on an unbound
    proxy returns the fallback value instead of a method object.
    :issue:`2188`
-   Redirects with the test client set ``RAW_URI`` and ``REQUEST_URI``
    correctly. :issue:`2151`


Version 2.0.2
-------------

Released 2021-10-05

-   Handle multiple tokens in ``Connection`` header when routing
    WebSocket requests. :issue:`2131`
-   Set the debugger pin cookie secure flag when on https. :pr:`2150`
-   Fix type annotation for ``MultiDict.update`` to accept iterable
    values :pr:`2142`
-   Prevent double encoding of redirect URL when ``merge_slash=True``
    for ``Rule.match``. :issue:`2157`
-   ``CombinedMultiDict.to_dict`` with ``flat=False`` considers all
    component dicts when building value lists. :issue:`2189`
-   ``send_file`` only sets a detected ``Content-Encoding`` if
    ``as_attachment`` is disabled to avoid browsers saving
    decompressed ``.tar.gz`` files. :issue:`2149`
-   Fix type annotations for ``TypeConversionDict.get`` to not return an
    ``Optional`` value if both ``default`` and ``type`` are not
    ``None``. :issue:`2169`
-   Fix type annotation for routing rule factories to accept
    ``Iterable[RuleFactory]`` instead of ``Iterable[Rule]`` for the
    ``rules`` parameter. :issue:`2183`
-   Add missing type annotation for ``FileStorage.__getattr__``
    :issue:`2155`
-   The debugger pin cookie is set with ``SameSite`` set to ``Strict``
    instead of ``None`` to be compatible with modern browser security.
    :issue:`2156`
-   Type annotations use ``IO[bytes]`` and ``IO[str]`` instead of
    ``BinaryIO`` and ``TextIO`` for wider type compatibility.
    :issue:`2130`
-   Ad-hoc TLS certs are generated with SAN matching CN. :issue:`2158`
-   Fix memory usage for locals when using Python 3.6 or pre 0.4.17
    greenlet versions. :pr:`2212`
-   Fix type annotation in ``CallbackDict``, because it is not
    utilizing a bound TypeVar. :issue:`2235`
-   Fix setting CSP header options on the response. :pr:`2237`
-   Fix an issue with with the interactive debugger where lines would
    not expand on click for very long tracebacks. :pr:`2239`
-   The interactive debugger handles displaying an exception that does
    not have a traceback, such as from ``ProcessPoolExecutor``.
    :issue:`2217`


Version 2.0.1
-------------

Released 2021-05-17

-   Fix type annotation for ``send_file`` ``max_age`` callable. Don't
    pass ``pathlib.Path`` to ``max_age``. :issue:`2119`
-   Mark top-level names as exported so type checking understands
    imports in user projects. :issue:`2122`
-   Fix some types that weren't available in Python 3.6.0. :issue:`2123`
-   ``cached_property`` is generic over its return type, properties
    decorated with it report the correct type. :issue:`2113`
-   Fix multipart parsing bug when boundary contains special regex
    characters. :issue:`2125`
-   Type checking understands that calling ``headers.get`` with a string
    default will always return a string. :issue:`2128`
-   If ``HTTPException.description`` is not a string,
    ``get_description`` will convert it to a string. :issue:`2115`


Version 2.0.0
-------------

Released 2021-05-11

-   Drop support for Python 2 and 3.5. :pr:`1693`
-   Deprecate :func:`utils.format_string`, use :class:`string.Template`
    instead. :issue:`1756`
-   Deprecate :func:`utils.bind_arguments` and
    :func:`utils.validate_arguments`, use :meth:`Signature.bind` and
    :func:`inspect.signature` instead. :issue:`1757`
-   Deprecate :class:`utils.HTMLBuilder`. :issue:`1761`
-   Deprecate :func:`utils.escape` and :func:`utils.unescape`, use
    MarkupSafe instead. :issue:`1758`
-   Deprecate the undocumented ``python -m werkzeug.serving`` CLI.
    :issue:`1834`
-   Deprecate the ``environ["werkzeug.server.shutdown"]`` function
    that is available when running the development server. :issue:`1752`
-   Deprecate the ``useragents`` module and the built-in user agent
    parser. Use a dedicated parser library instead by subclassing
    ``user_agent.UserAgent`` and setting ``Request.user_agent_class``.
    :issue:`2078`
-   Remove the unused, internal ``posixemulation`` module. :issue:`1759`
-   All ``datetime`` values are timezone-aware with
    ``tzinfo=timezone.utc``. This applies to anything using
    ``http.parse_date``: ``Request.date``, ``.if_modified_since``,
    ``.if_unmodified_since``; ``Response.date``, ``.expires``,
    ``.last_modified``, ``.retry_after``; ``parse_if_range_header``, and
    ``IfRange.date``. When comparing values, the other values must also
    be aware, or these values must be made naive. When passing
    parameters or setting attributes, naive values are still assumed to
    be in UTC. :pr:`2040`
-   Merge all request and response wrapper mixin code into single
    ``Request`` and ``Response`` classes. Using the mixin classes is no
    longer necessary and will show a deprecation warning. Checking
    ``isinstance`` or ``issubclass`` against ``BaseRequest`` and
    ``BaseResponse`` will show a deprecation warning and check against
    ``Request`` or ``Response`` instead. :issue:`1963`
-   JSON support no longer uses simplejson if it's installed. To use
    another JSON module, override ``Request.json_module`` and
    ``Response.json_module``. :pr:`1766`
-   ``Response.get_json()`` no longer caches the result, and the
    ``cache`` parameter is removed. :issue:`1698`
-   ``Response.freeze()`` generates an ``ETag`` header if one is not
    set. The ``no_etag`` parameter (which usually wasn't visible
    anyway) is no longer used. :issue:`1963`
-   Add a ``url_scheme`` argument to :meth:`~routing.MapAdapter.build`
    to override the bound scheme. :pr:`1721`
-   Passing an empty list as a query string parameter to ``build()``
    won't append an unnecessary ``?``. Also drop any number of ``None``
    items in a list. :issue:`1992`
-   When passing a ``Headers`` object to a test client method or
    ``EnvironBuilder``, multiple values for a key are joined into one
    comma separated value. This matches the HTTP spec on multi-value
    headers. :issue:`1655`
-   Setting ``Response.status`` and ``status_code`` uses identical
    parsing and error checking. :issue:`1658`, :pr:`1728`
-   ``MethodNotAllowed`` and ``RequestedRangeNotSatisfiable`` take a
    ``response`` kwarg, consistent with other HTTP errors. :pr:`1748`
-   The response generated by :exc:`~exceptions.Unauthorized` produces
    one ``WWW-Authenticate`` header per value in ``www_authenticate``,
    rather than joining them into a single value, to improve
    interoperability with browsers and other clients. :pr:`1755`
-   If ``parse_authorization_header`` can't decode the header value, it
    returns ``None`` instead of raising a ``UnicodeDecodeError``.
    :issue:`1816`
-   The debugger no longer uses jQuery. :issue:`1807`
-   The test client includes the query string in ``REQUEST_URI`` and
    ``RAW_URI``. :issue:`1781`
-   Switch the parameter order of ``default_stream_factory`` to match
    the order used when calling it. :pr:`1085`
-   Add ``send_file`` function to generate a response that serves a
    file. Adapted from Flask's implementation. :issue:`265`, :pr:`1850`
-   Add ``send_from_directory`` function to safely serve an untrusted
    path within a trusted directory. Adapted from Flask's
    implementation. :issue:`1880`
-   ``send_file`` takes ``download_name``, which is passed even if
    ``as_attachment=False`` by using ``Content-Disposition: inline``.
    ``download_name`` replaces Flask's ``attachment_filename``.
    :issue:`1869`
-   ``send_file`` sets ``conditional=True`` and ``max_age=None`` by
    default. ``Cache-Control`` is set to ``no-cache`` if ``max_age`` is
    not set, otherwise ``public``. This tells browsers to validate
    conditional requests instead of using a timed cache.
    ``max_age=None`` replaces Flask's ``cache_timeout=43200``.
    :issue:`1882`
-   ``send_file`` can be called with ``etag="string"`` to set a custom
    ETag instead of generating one. ``etag`` replaces Flask's
    ``add_etags``. :issue:`1868`
-   ``send_file`` sets the ``Content-Encoding`` header if an encoding is
    returned when guessing ``mimetype`` from ``download_name``.
    :pr:`3896`
-   Update the defaults used by ``generate_password_hash``. Increase
    PBKDF2 iterations to 260000 from 150000. Increase salt length to 16
    from 8. Use ``secrets`` module to generate salt. :pr:`1935`
-   The reloader doesn't crash if ``sys.stdin`` is somehow ``None``.
    :pr:`1915`
-   Add arguments to ``delete_cookie`` to match ``set_cookie`` and the
    attributes modern browsers expect. :pr:`1889`
-   ``utils.cookie_date`` is deprecated, use ``utils.http_date``
    instead. The value for ``Set-Cookie expires`` is no longer "-"
    delimited. :pr:`2040`
-   Use ``request.headers`` instead of ``request.environ`` to look up
    header attributes. :pr:`1808`
-   The test ``Client`` request methods (``client.get``, etc.) always
    return an instance of ``TestResponse``. In addition to the normal
    behavior of ``Response``, this class provides ``request`` with the
    request that produced the response, and ``history`` to track
    intermediate responses when ``follow_redirects`` is used.
    :issue:`763, 1894`
-   The test ``Client`` request methods takes an ``auth`` parameter to
    add an ``Authorization`` header. It can be an ``Authorization``
    object or a ``(username, password)`` tuple for ``Basic`` auth.
    :pr:`1809`
-   Calling ``response.close()`` on a response from the test ``Client``
    will close the request input stream. This matches file behavior
    and can prevent a ``ResourceWarning`` in some cases. :issue:`1785`
-   ``EnvironBuilder.from_environ`` decodes values encoded for WSGI, to
    avoid double encoding the new values. :pr:`1959`
-   The default stat reloader will watch Python files under
    non-system/virtualenv ``sys.path`` entries, which should contain
    most user code. It will also watch all Python files under
    directories given in ``extra_files``. :pr:`1945`
-   The reloader ignores ``__pycache__`` directories again. :pr:`1945`
-   ``run_simple`` takes ``exclude_patterns`` a list of ``fnmatch``
    patterns that will not be scanned by the reloader. :issue:`1333`
-   Cookie names are no longer unquoted. This was against :rfc:`6265`
    and potentially allowed setting ``__Secure`` prefixed cookies.
    :pr:`1965`
-   Fix some word matches for user agent platform when the word can be a
    substring. :issue:`1923`
-   The development server logs ignored SSL errors. :pr:`1967`
-   Temporary files for form data are opened in ``rb+`` instead of
    ``wb+`` mode for better compatibility with some libraries.
    :issue:`1961`
-   Use SHA-1 instead of MD5 for generating ETags and the debugger pin,
    and in some tests. MD5 is not available in some environments, such
    as FIPS 140. This may invalidate some caches since the ETag will be
    different. :issue:`1897`
-   Add ``Cross-Origin-Opener-Policy`` and
    ``Cross-Origin-Embedder-Policy`` response header properties.
    :pr:`2008`
-   ``run_simple`` tries to show a valid IP address when binding to all
    addresses, instead of ``0.0.0.0`` or ``::``. It also warns about not
    running the development server in production in this case.
    :issue:`1964`
-   Colors in the development server log are displayed if Colorama is
    installed on Windows. For all platforms, style support no longer
    requires Click. :issue:`1832`
-   A range request for an empty file (or other data with length 0) will
    return a 200 response with the empty file instead of a 416 error.
    :issue:`1937`
-   New sans-IO base classes for ``Request`` and ``Response`` have been
    extracted to contain all the behavior that is not WSGI or IO
    dependent. These are not a public API, they are part of an ongoing
    refactor to let ASGI frameworks use Werkzeug. :pr:`2005`
-   Parsing ``multipart/form-data`` has been refactored to use sans-io
    patterns. This should also make parsing forms with large binary file
    uploads significantly faster. :issue:`1788, 875`
-   ``LocalProxy`` matches the current Python data model special
    methods, including all r-ops, in-place ops, and async. ``__class__``
    is proxied, so the proxy will look like the object in more cases,
    including ``isinstance``. Use ``issubclass(type(obj), LocalProxy)``
    to check if an object is actually a proxy. :issue:`1754`
-   ``Local`` uses ``ContextVar`` on Python 3.7+ instead of
    ``threading.local``. :pr:`1778`
-   ``request.values`` does not include ``form`` for GET requests (even
    though GET bodies are undefined). This prevents bad caching proxies
    from caching form data instead of query strings. :pr:`2037`
-   The development server adds the underlying socket to ``environ`` as
    ``werkzeug.socket``. This is non-standard and specific to the dev
    server, other servers may expose this under their own key. It is
    useful for handling a WebSocket upgrade request. :issue:`2052`
-   URL matching assumes ``websocket=True`` mode for WebSocket upgrade
    requests. :issue:`2052`
-   Updated ``UserAgentParser`` to handle more cases. :issue:`1971`
-   ``werzeug.DechunkedInput.readinto`` will not read beyond the size of
    the buffer. :issue:`2021`
-   Fix connection reset when exceeding max content size. :pr:`2051`
-   ``pbkdf2_hex``, ``pbkdf2_bin``, and ``safe_str_cmp`` are deprecated.
    ``hashlib`` and ``hmac`` provide equivalents. :pr:`2083`
-   ``invalidate_cached_property`` is deprecated. Use ``del obj.name``
    instead. :pr:`2084`
-   ``Href`` is deprecated. Use ``werkzeug.routing`` instead.
    :pr:`2085`
-   ``Request.disable_data_descriptor`` is deprecated. Create the
    request with ``shallow=True`` instead. :pr:`2085`
-   ``HTTPException.wrap`` is deprecated. Create a subclass manually
    instead. :pr:`2085`


Version 1.0.1
-------------

Released 2020-03-31

-   Make the argument to ``RequestRedirect.get_response`` optional.
    :issue:`1718`
-   Only allow a single access control allow origin value. :pr:`1723`
-   Fix crash when trying to parse a non-existent Content Security
    Policy header. :pr:`1731`
-   ``http_date`` zero fills years < 1000 to always output four digits.
    :issue:`1739`
-   Fix missing local variables in interactive debugger console.
    :issue:`1746`
-   Fix passing file-like objects like ``io.BytesIO`` to
    ``FileStorage.save``. :issue:`1733`


Version 1.0.0
-------------

Released 2020-02-06

-   Drop support for Python 3.4. (:issue:`1478`)
-   Remove code that issued deprecation warnings in version 0.15.
    (:issue:`1477`)
-   Remove most top-level attributes provided by the ``werkzeug``
    module in favor of direct imports. For example, instead of
    ``import werkzeug; werkzeug.url_quote``, do
    ``from werkzeug.urls import url_quote``. Install version 0.16 first
    to see deprecation warnings while upgrading. :issue:`2`, :pr:`1640`
-   Added ``utils.invalidate_cached_property()`` to invalidate cached
    properties. (:pr:`1474`)
-   Directive keys for the ``Set-Cookie`` response header are not
    ignored when parsing the ``Cookie`` request header. This allows
    cookies with names such as "expires" and "version". (:issue:`1495`)
-   Request cookies are parsed into a ``MultiDict`` to capture all
    values for cookies with the same key. ``cookies[key]`` returns the
    first value rather than the last. Use ``cookies.getlist(key)`` to
    get all values. ``parse_cookie`` also defaults to a ``MultiDict``.
    :issue:`1562`, :pr:`1458`
-   Add ``charset=utf-8`` to an HTTP exception response's
    ``CONTENT_TYPE`` header. (:pr:`1526`)
-   The interactive debugger handles outer variables in nested scopes
    such as lambdas and comprehensions. :issue:`913`, :issue:`1037`,
    :pr:`1532`
-   The user agent for Opera 60 on Mac is correctly reported as
    "opera" instead of "chrome". :issue:`1556`
-   The platform for Crosswalk on Android is correctly reported as
    "android" instead of "chromeos". (:pr:`1572`)
-   Issue a warning when the current server name does not match the
    configured server name. :issue:`760`
-   A configured server name with the default port for a scheme will
    match the current server name without the port if the current scheme
    matches. :pr:`1584`
-   :exc:`~exceptions.InternalServerError` has a ``original_exception``
    attribute that frameworks can use to track the original cause of the
    error. :pr:`1590`
-   Headers are tested for equality independent of the header key case,
    such that ``X-Foo`` is the same as ``x-foo``. :pr:`1605`
-   :meth:`http.dump_cookie` accepts ``'None'`` as a value for
    ``samesite``. :issue:`1549`
-   :meth:`~test.Client.set_cookie` accepts a ``samesite`` argument.
    :pr:`1705`
-   Support the Content Security Policy header through the
    `Response.content_security_policy` data structure. :pr:`1617`
-   ``LanguageAccept`` will fall back to matching "en" for "en-US" or
    "en-US" for "en" to better support clients or translations that
    only match at the primary language tag. :issue:`450`, :pr:`1507`
-   ``MIMEAccept`` uses MIME parameters for specificity when matching.
    :issue:`458`, :pr:`1574`
-   If the development server is started with an ``SSLContext``
    configured to verify client certificates, the certificate in PEM
    format will be available as ``environ["SSL_CLIENT_CERT"]``.
    :pr:`1469`
-   ``is_resource_modified`` will run for methods other than ``GET`` and
    ``HEAD``, rather than always returning ``False``. :issue:`409`
-   ``SharedDataMiddleware`` returns 404 rather than 500 when trying to
    access a directory instead of a file with the package loader. The
    dependency on setuptools and pkg_resources is removed.
    :issue:`1599`
-   Add a ``response.cache_control.immutable`` flag. Keep in mind that
    browser support for this ``Cache-Control`` header option is still
    experimental and may not be implemented. :issue:`1185`
-   Optional request log highlighting with the development server is
    handled by Click instead of termcolor. :issue:`1235`
-   Optional ad-hoc TLS support for the development server is handled
    by cryptography instead of pyOpenSSL. :pr:`1555`
-   ``FileStorage.save()`` supports ``pathlib`` and :pep:`519`
    ``PathLike`` objects. :issue:`1653`
-   The debugger security pin is unique in containers managed by Podman.
    :issue:`1661`
-   Building a URL when ``host_matching`` is enabled takes into account
    the current host when there are duplicate endpoints with different
    hosts. :issue:`488`
-   The ``429 TooManyRequests`` and ``503 ServiceUnavailable`` HTTP
    exceptions takes a ``retry_after`` parameter to set the
    ``Retry-After`` header. :issue:`1657`
-   ``Map`` and ``Rule`` have a ``merge_slashes`` option to collapse
    multiple slashes into one, similar to how many HTTP servers behave.
    This is enabled by default. :pr:`1286, 1694`
-   Add HTTP 103, 208, 306, 425, 506, 508, and 511 to the list of status
    codes. :pr:`1678`
-   Add ``update``, ``setlist``, and ``setlistdefault`` methods to the
    ``Headers`` data structure. ``extend`` method can take ``MultiDict``
    and kwargs. :pr:`1687, 1697`
-   The development server accepts paths that start with two slashes,
    rather than stripping off the first path segment. :issue:`491`
-   Add access control (Cross Origin Request Sharing, CORS) header
    properties to the ``Request`` and ``Response`` wrappers. :pr:`1699`
-   ``Accept`` values are no longer ordered alphabetically for equal
    quality tags. Instead the initial order is preserved. :issue:`1686`
-   Added ``Map.lock_class`` attribute for alternative
    implementations. :pr:`1702`
-   Support matching and building WebSocket rules in the routing system,
    for use by async frameworks. :pr:`1709`
-   Range requests that span an entire file respond with 206 instead of
    200, to be more compliant with :rfc:`7233`. This may help serving
    media to older browsers. :issue:`410, 1704`
-   The :class:`~middleware.shared_data.SharedDataMiddleware` default
    ``fallback_mimetype`` is ``application/octet-stream``. If a filename
    looks like a text mimetype, the ``utf-8`` charset is added to it.
    This matches the behavior of :class:`~wrappers.BaseResponse` and
    Flask's ``send_file()``. :issue:`1689`


Version 0.16.1
--------------

Released 2020-01-27

-   Fix import location in deprecation messages for subpackages.
    :issue:`1663`
-   Fix an SSL error on Python 3.5 when the dev server responds with no
    content. :issue:`1659`


Version 0.16.0
--------------

Released 2019-09-19

-   Deprecate most top-level attributes provided by the ``werkzeug``
    module in favor of direct imports. The deprecated imports will be
    removed in version 1.0.

    For example, instead of ``import werkzeug; werkzeug.url_quote``, do
    ``from werkzeug.urls import url_quote``. A deprecation warning will
    show the correct import to use. ``werkzeug.exceptions`` and
    ``werkzeug.routing`` should also be imported instead of accessed,
    but for technical reasons can't show a warning.

    :issue:`2`, :pr:`1640`


Version 0.15.6
--------------

Released 2019-09-04

-   Work around a bug in pip that caused the reloader to fail on
    Windows when the script was an entry point. This fixes the issue
    with Flask's `flask run` command failing with "No module named
    Scripts\flask". :issue:`1614`
-   ``ProxyFix`` trusts the ``X-Forwarded-Proto`` header by default.
    :issue:`1630`
-   The deprecated ``num_proxies`` argument to ``ProxyFix`` sets
    ``x_for``, ``x_proto``, and ``x_host`` to match 0.14 behavior. This
    is intended to make intermediate upgrades less disruptive, but the
    argument will still be removed in 1.0. :issue:`1630`


Version 0.15.5
--------------

Released 2019-07-17

-   Fix a ``TypeError`` due to changes to ``ast.Module`` in Python 3.8.
    :issue:`1551`
-   Fix a C assertion failure in debug builds of some Python 2.7
    releases. :issue:`1553`
-   :class:`~exceptions.BadRequestKeyError` adds the ``KeyError``
    message to the description if ``e.show_exception`` is set to
    ``True``. This is a more secure default than the original 0.15.0
    behavior and makes it easier to control without losing information.
    :pr:`1592`
-   Upgrade the debugger to jQuery 3.4.1. :issue:`1581`
-   Work around an issue in some external debuggers that caused the
    reloader to fail. :issue:`1607`
-   Work around an issue where the reloader couldn't introspect a
    setuptools script installed as an egg. :issue:`1600`
-   The reloader will use ``sys.executable`` even if the script is
    marked executable, reverting a behavior intended for NixOS
    introduced in 0.15. The reloader should no longer cause
    ``OSError: [Errno 8] Exec format error``. :issue:`1482`,
    :issue:`1580`
-   ``SharedDataMiddleware`` safely handles paths with Windows drive
    names. :issue:`1589`


Version 0.15.4
--------------

Released 2019-05-14

-   Fix a ``SyntaxError`` on Python 2.7.5. (:issue:`1544`)


Version 0.15.3
--------------

Released 2019-05-14

-   Properly handle multi-line header folding in development server in
    Python 2.7. (:issue:`1080`)
-   Restore the ``response`` argument to :exc:`~exceptions.Unauthorized`.
    (:pr:`1527`)
-   :exc:`~exceptions.Unauthorized` doesn't add the ``WWW-Authenticate``
    header if ``www_authenticate`` is not given. (:issue:`1516`)
-   The default URL converter correctly encodes bytes to string rather
    than representing them with ``b''``. (:issue:`1502`)
-   Fix the filename format string in
    :class:`~middleware.profiler.ProfilerMiddleware` to correctly handle
    float values. (:issue:`1511`)
-   Update :class:`~middleware.lint.LintMiddleware` to work on Python 3.
    (:issue:`1510`)
-   The debugger detects cycles in chained exceptions and does not time
    out in that case. (:issue:`1536`)
-   When running the development server in Docker, the debugger security
    pin is now unique per container.


Version 0.15.2
--------------

Released 2019-04-02

-   ``Rule`` code generation uses a filename that coverage will ignore.
    The previous value, "generated", was causing coverage to fail.
    (:issue:`1487`)
-   The test client removes the cookie header if there are no persisted
    cookies. This fixes an issue introduced in 0.15.0 where the cookies
    from the original request were used for redirects, causing functions
    such as logout to fail. (:issue:`1491`)
-   The test client copies the environ before passing it to the app, to
    prevent in-place modifications from affecting redirect requests.
    (:issue:`1498`)
-   The ``"werkzeug"`` logger only adds a handler if there is no handler
    configured for its level in the logging chain. This avoids double
    logging if other code configures logging first. (:issue:`1492`)


Version 0.15.1
--------------

Released 2019-03-21

-   :exc:`~exceptions.Unauthorized` takes ``description`` as the first
    argument, restoring previous behavior. The new ``www_authenticate``
    argument is listed second. (:issue:`1483`)


Version 0.15.0
--------------

Released 2019-03-19

-   Building URLs is ~7x faster. Each :class:`~routing.Rule` compiles
    an optimized function for building itself. (:pr:`1281`)
-   :meth:`MapAdapter.build() <routing.MapAdapter.build>` can be passed
    a :class:`~datastructures.MultiDict` to represent multiple values
    for a key. It already did this when passing a dict with a list
    value. (:pr:`724`)
-   ``path_info`` defaults to ``'/'`` for
    :meth:`Map.bind() <routing.Map.bind>`. (:issue:`740`, :pr:`768`,
    :pr:`1316`)
-   Change ``RequestRedirect`` code from 301 to 308, preserving the verb
    and request body (form data) during redirect. (:pr:`1342`)
-   ``int`` and ``float`` converters in URL rules will handle negative
    values if passed the ``signed=True`` parameter. For example,
    ``/jump/<int(signed=True):count>``. (:pr:`1355`)
-   ``Location`` autocorrection in :func:`Response.get_wsgi_headers()
    <wrappers.BaseResponse.get_wsgi_headers>` is relative to the current
    path rather than the root path. (:issue:`693`, :pr:`718`,
    :pr:`1315`)
-   412 responses once again include entity headers and an error message
    in the body. They were originally omitted when implementing
    ``If-Match`` (:pr:`1233`), but the spec doesn't seem to disallow it.
    (:issue:`1231`, :pr:`1255`)
-   The Content-Length header is removed for 1xx and 204 responses. This
    fixes a previous change where no body would be sent, but the header
    would still be present. The new behavior matches RFC 7230.
    (:pr:`1294`)
-   :class:`~exceptions.Unauthorized` takes a ``www_authenticate``
    parameter to set the ``WWW-Authenticate`` header for the response,
    which is technically required for a valid 401 response.
    (:issue:`772`, :pr:`795`)
-   Add support for status code 424 :exc:`~exceptions.FailedDependency`.
    (:pr:`1358`)
-   :func:`http.parse_cookie` ignores empty segments rather than
    producing a cookie with no key or value. (:issue:`1245`, :pr:`1301`)
-   ``http.parse_authorization_header`` (and
    :class:`~datastructures.Authorization`,
    :attr:`~wrappers.Request.authorization`) treats the authorization
    header as UTF-8. On Python 2, basic auth username and password are
    ``unicode``. (:pr:`1325`)
-   :func:`~http.parse_options_header` understands :rfc:`2231` parameter
    continuations. (:pr:`1417`)
-   :func:`~urls.uri_to_iri` does not unquote ASCII characters in the
    unreserved class, such as space, and leaves invalid bytes quoted
    when decoding. :func:`~urls.iri_to_uri` does not quote reserved
    characters. See :rfc:`3987` for these character classes.
    (:pr:`1433`)
-   ``get_content_type`` appends a charset for any mimetype that ends
    with ``+xml``, not just those that start with ``application/``.
    Known text types such as ``application/javascript`` are also given
    charsets. (:pr:`1439`)
-   Clean up ``werkzeug.security`` module, remove outdated hashlib
    support. (:pr:`1282`)
-   In :func:`~security.generate_password_hash`, PBKDF2 uses 150000
    iterations by default, increased from 50000. (:pr:`1377`)
-   :class:`~wsgi.ClosingIterator` calls ``close`` on the wrapped
    *iterable*, not the internal iterator. This doesn't affect objects
    where ``__iter__`` returned ``self``. For other objects, the method
    was not called before. (:issue:`1259`, :pr:`1260`)
-   Bytes may be used as keys in :class:`~datastructures.Headers`, they
    will be decoded as Latin-1 like values are. (:pr:`1346`)
-   :class:`~datastructures.Range` validates that list of range tuples
    passed to it would produce a valid ``Range`` header. (:pr:`1412`)
-   :class:`~datastructures.FileStorage` looks up attributes on
    ``stream._file`` if they don't exist on ``stream``, working around
    an issue where :func:`tempfile.SpooledTemporaryFile` didn't
    implement all of :class:`io.IOBase`. See
    https://github.com/python/cpython/pull/3249. (:pr:`1409`)
-   :class:`CombinedMultiDict.copy() <datastructures.CombinedMultiDict>`
    returns a shallow mutable copy as a
    :class:`~datastructures.MultiDict`. The copy no longer reflects
    changes to the combined dicts, but is more generally useful.
    (:pr:`1420`)
-   The version of jQuery used by the debugger is updated to 3.3.1.
    (:pr:`1390`)
-   The debugger correctly renders long ``markupsafe.Markup`` instances.
    (:pr:`1393`)
-   The debugger can serve resources when Werkzeug is installed as a
    zip file. ``DebuggedApplication.get_resource`` uses
    ``pkgutil.get_data``. (:pr:`1401`)
-   The debugger and server log support Python 3's chained exceptions.
    (:pr:`1396`)
-   The interactive debugger highlights frames that come from user code
    to make them easy to pick out in a long stack trace. Note that if an
    env was created with virtualenv instead of venv, the debugger may
    incorrectly classify some frames. (:pr:`1421`)
-   Clicking the error message at the top of the interactive debugger
    will jump down to the bottom of the traceback. (:pr:`1422`)
-   When generating a PIN, the debugger will ignore a ``KeyError``
    raised when the current UID doesn't have an associated username,
    which can happen in Docker. (:issue:`1471`)
-   :class:`~exceptions.BadRequestKeyError` adds the ``KeyError``
    message to the description, making it clearer what caused the 400
    error. Frameworks like Flask can omit this information in production
    by setting ``e.args = ()``. (:pr:`1395`)
-   If a nested ``ImportError`` occurs from :func:`~utils.import_string`
    the traceback mentions the nested import. Removes an untested code
    path for handling "modules not yet set up by the parent."
    (:pr:`735`)
-   Triggering a reload while using a tool such as PDB no longer hides
    input. (:pr:`1318`)
-   The reloader will not prepend the Python executable to the command
    line if the Python file is marked executable. This allows the
    reloader to work on NixOS. (:pr:`1242`)
-   Fix an issue where ``sys.path`` would change between reloads when
    running with ``python -m app``. The reloader can detect that a
    module was run with "-m" and reconstructs that instead of the file
    path in ``sys.argv`` when reloading. (:pr:`1416`)
-   The dev server can bind to a Unix socket by passing a hostname like
    ``unix://app.socket``. (:pr:`209`, :pr:`1019`)
-   Server uses ``IPPROTO_TCP`` constant instead of ``SOL_TCP`` for
    Jython compatibility. (:pr:`1375`)
-   When using an adhoc SSL cert with :func:`~serving.run_simple`, the
    cert is shown as self-signed rather than signed by an invalid
    authority. (:pr:`1430`)
-   The development server logs the unquoted IRI rather than the raw
    request line, to make it easier to work with Unicode in request
    paths during development. (:issue:`1115`)
-   The development server recognizes ``ConnectionError`` on Python 3 to
    silence client disconnects, and does not silence other ``OSErrors``
    that may have been raised inside the application. (:pr:`1418`)
-   The environ keys ``REQUEST_URI`` and ``RAW_URI`` contain the raw
    path before it was percent-decoded. This is non-standard, but many
    WSGI servers add them. Middleware could replace ``PATH_INFO`` with
    this to route based on the raw value. (:pr:`1419`)
-   :class:`~test.EnvironBuilder` doesn't set ``CONTENT_TYPE`` or
    ``CONTENT_LENGTH`` in the environ if they aren't set. Previously
    these used default values if they weren't set. Now it's possible to
    distinguish between empty and unset values. (:pr:`1308`)
-   The test client raises a ``ValueError`` if a query string argument
    would overwrite a query string in the path. (:pr:`1338`)
-   :class:`test.EnvironBuilder` and :class:`test.Client` take a
    ``json`` argument instead of manually passing ``data`` and
    ``content_type``. This is serialized using the
    :meth:`test.EnvironBuilder.json_dumps` method. (:pr:`1404`)
-   :class:`test.Client` redirect handling is rewritten. (:pr:`1402`)

    -   The redirect environ is copied from the initial request environ.
    -   Script root and path are correctly distinguished when
        redirecting to a path under the root.
    -   The HEAD method is not changed to GET.
    -   307 and 308 codes preserve the method and body. All others
        ignore the body and related headers.
    -   Headers are passed to the new request for all codes, following
        what browsers do.
    -   :class:`test.EnvironBuilder` sets the content type and length
        headers in addition to the WSGI keys when detecting them from
        the data.
    -   Intermediate response bodies are iterated over even when
        ``buffered=False`` to ensure iterator middleware can run cleanup
        code safely. Only the last response is not buffered. (:pr:`988`)

-   :class:`~test.EnvironBuilder`, :class:`~datastructures.FileStorage`,
    and :func:`wsgi.get_input_stream` no longer share a global
    ``_empty_stream`` instance. This improves test isolation by
    preventing cases where closing the stream in one request would
    affect other usages. (:pr:`1340`)
-   The default ``SecureCookie.serialization_method`` will change from
    :mod:`pickle` to :mod:`json` in 1.0. To upgrade existing tokens,
    override :meth:`~contrib.securecookie.SecureCookie.unquote` to try
    ``pickle`` if ``json`` fails. (:pr:`1413`)
-   ``CGIRootFix`` no longer modifies ``PATH_INFO`` for very old
    versions of Lighttpd. ``LighttpdCGIRootFix`` was renamed to
    ``CGIRootFix`` in 0.9. Both are deprecated and will be removed in
    version 1.0. (:pr:`1141`)
-   :class:`werkzeug.wrappers.json.JSONMixin` has been replaced with
    Flask's implementation. Check the docs for the full API.
    (:pr:`1445`)
-   The contrib modules are deprecated and will either be moved into
    ``werkzeug`` core or removed completely in version 1.0. Some modules
    that already issued deprecation warnings have been removed. Be sure
    to run or test your code with
    ``python -W default::DeprecationWarning`` to catch any deprecated
    code you're using. (:issue:`4`)

    -   ``LintMiddleware`` has moved to :mod:`werkzeug.middleware.lint`.
    -   ``ProfilerMiddleware`` has moved to
        :mod:`werkzeug.middleware.profiler`.
    -   ``ProxyFix`` has moved to :mod:`werkzeug.middleware.proxy_fix`.
    -   ``JSONRequestMixin`` has moved to :mod:`werkzeug.wrappers.json`.
    -   ``cache`` has been extracted into a separate project,
        `cachelib <https://github.com/pallets/cachelib>`_. The version
        in Werkzeug is deprecated.
    -   ``securecookie`` and ``sessions`` have been extracted into a
        separate project,
        `secure-cookie <https://github.com/pallets/secure-cookie>`_. The
        version in Werkzeug is deprecated.
    -   Everything in ``fixers``, except ``ProxyFix``, is deprecated.
    -   Everything in ``wrappers``, except ``JSONMixin``, is deprecated.
    -   ``atom`` is deprecated. This did not fit in with the rest of
        Werkzeug, and is better served by a dedicated library in the
        community.
    -   ``jsrouting`` is removed. Set URLs when rendering templates
        or JSON responses instead.
    -   ``limiter`` is removed. Its specific use is handled by Werkzeug
        directly, but stream limiting is better handled by the WSGI
        server in general.
    -   ``testtools`` is removed. It did not offer significant benefit
        over the default test client.
    -   ``iterio`` is deprecated.

-   :func:`wsgi.get_host` no longer looks at ``X-Forwarded-For``. Use
    :class:`~middleware.proxy_fix.ProxyFix` to handle that.
    (:issue:`609`, :pr:`1303`)
-   :class:`~middleware.proxy_fix.ProxyFix` is refactored to support
    more headers, multiple values, and more secure configuration.

    -   Each header supports multiple values. The trusted number of
        proxies is configured separately for each header. The
        ``num_proxies`` argument is deprecated. (:pr:`1314`)
    -   Sets ``SERVER_NAME`` and ``SERVER_PORT`` based on
        ``X-Forwarded-Host``. (:pr:`1314`)
    -   Sets ``SERVER_PORT`` and modifies ``HTTP_HOST`` based on
        ``X-Forwarded-Port``. (:issue:`1023`, :pr:`1304`)
    -   Sets ``SCRIPT_NAME`` based on ``X-Forwarded-Prefix``.
        (:issue:`1237`)
    -   The original WSGI environment values are stored in the
        ``werkzeug.proxy_fix.orig`` key, a dict. The individual keys
        ``werkzeug.proxy_fix.orig_remote_addr``,
        ``werkzeug.proxy_fix.orig_wsgi_url_scheme``, and
        ``werkzeug.proxy_fix.orig_http_host`` are deprecated.

-   Middleware from ``werkzeug.wsgi`` has moved to separate modules
    under ``werkzeug.middleware``, along with the middleware moved from
    ``werkzeug.contrib``. The old ``werkzeug.wsgi`` imports are
    deprecated and will be removed in version 1.0. (:pr:`1452`)

    -   ``werkzeug.wsgi.DispatcherMiddleware`` has moved to
        :class:`werkzeug.middleware.dispatcher.DispatcherMiddleware`.
    -   ``werkzeug.wsgi.ProxyMiddleware`` as moved to
        :class:`werkzeug.middleware.http_proxy.ProxyMiddleware`.
    -   ``werkzeug.wsgi.SharedDataMiddleware`` has moved to
        :class:`werkzeug.middleware.shared_data.SharedDataMiddleware`.

-   :class:`~middleware.http_proxy.ProxyMiddleware` proxies the query
    string. (:pr:`1252`)
-   The filenames generated by
    :class:`~middleware.profiler.ProfilerMiddleware` can be customized.
    (:issue:`1283`)
-   The ``werkzeug.wrappers`` module has been converted to a package,
    and its various classes have been organized into separate modules.
    Any previously documented classes, understood to be the existing
    public API, are still importable from ``werkzeug.wrappers``, or may
    be imported from their specific modules. (:pr:`1456`)


Version 0.14.1
--------------

Released on December 31st 2017

- Resolved a regression with status code handling in the integrated
  development server.

Version 0.14
------------

Released on December 31st 2017

- HTTP exceptions are now automatically caught by
  ``Request.application``.
- Added support for edge as browser.
- Added support for platforms that lack ``SpooledTemporaryFile``.
- Add support for etag handling through if-match
- Added support for the SameSite cookie attribute.
- Added ``werkzeug.wsgi.ProxyMiddleware``
- Implemented ``has`` for ``NullCache``
- ``get_multi`` on cache clients now returns lists all the time.
- Improved the watchdog observer shutdown for the reloader to not crash
  on exit on older Python versions.
- Added support for ``filename*`` filename attributes according to
  RFC 2231
- Resolved an issue where machine ID for the reloader PIN was not
  read accurately on windows.
- Added a workaround for syntax errors in init files in the reloader.
- Added support for using the reloader with console scripts on windows.
- The built-in HTTP server will no longer close a connection in cases
  where no HTTP body is expected (204, 204, HEAD requests etc.)
- The ``EnvironHeaders`` object now skips over empty content type and
  lengths if they are set to falsy values.
- Werkzeug will no longer send the content-length header on 1xx or
  204/304 responses.
- Cookie values are now also permitted to include slashes and equal
  signs without quoting.
- Relaxed the regex for the routing converter arguments.
- If cookies are sent without values they are now assumed to have an
  empty value and the parser accepts this.  Previously this could have
  corrupted cookies that followed the value.
- The test ``Client`` and ``EnvironBuilder`` now support mimetypes like
  the request object does.
- Added support for static weights in URL rules.
- Better handle some more complex reloader scenarios where sys.path
  contained non directory paths.
- ``EnvironHeaders`` no longer raises weird errors if non string keys
  are passed to it.


Version 0.13
------------

Released on December 7th 2017

- **Deprecate support for Python 2.6 and 3.3.** CI tests will not run
  for these versions, and support will be dropped completely in the next
  version. (:issue:`pallets/meta#24`)
- Raise ``TypeError`` when port is not an integer. (:pr:`1088`)
- Fully deprecate ``werkzeug.script``. Use `Click`_ instead.
  (:pr:`1090`)
- ``response.age`` is parsed as a ``timedelta``. Previously, it was
  incorrectly treated as a ``datetime``. The header value is an integer
  number of seconds, not a date string. (:pr:`414`)
- Fix a bug in ``TypeConversionDict`` where errors are not propagated
  when using the converter. (:issue:`1102`)
- ``Authorization.qop`` is a string instead of a set, to comply with
  RFC 2617. (:pr:`984`)
- An exception is raised when an encoded cookie is larger than, by
  default, 4093 bytes. Browsers may silently ignore cookies larger than
  this. ``BaseResponse`` has a new attribute ``max_cookie_size`` and
  ``dump_cookie`` has a new argument ``max_size`` to configure this.
  (:pr:`780`, :pr:`1109`)
- Fix a TypeError in ``werkzeug.contrib.lint.GuardedIterator.close``.
  (:pr:`1116`)
- ``BaseResponse.calculate_content_length`` now correctly works for
  Unicode responses on Python 3. It first encodes using
  ``iter_encoded``. (:issue:`705`)
- Secure cookie contrib works with string secret key on Python 3.
  (:pr:`1205`)
- Shared data middleware accepts a list instead of a dict of static
  locations to preserve lookup order. (:pr:`1197`)
- HTTP header values without encoding can contain single quotes.
  (:pr:`1208`)
- The built-in dev server supports receiving requests with chunked
  transfer encoding. (:pr:`1198`)

.. _Click: https://palletsprojects.com/p/click/


Version 0.12.2
--------------

Released on May 16 2017

- Fix regression: Pull request ``#892`` prevented Werkzeug from correctly
  logging the IP of a remote client behind a reverse proxy, even when using
  `ProxyFix`.
- Fix a bug in `safe_join` on Windows.

Version 0.12.1
--------------

Released on March 15th 2017

- Fix crash of reloader (used on debug mode) on Windows.
  (`OSError: [WinError 10038]`). See pull request ``#1081``
- Partially revert change to class hierarchy of `Headers`. See ``#1084``.

Version 0.12
------------

Released on March 10th 2017

- Spit out big deprecation warnings for werkzeug.script
- Use `inspect.getfullargspec` internally when available as
  `inspect.getargspec` is gone in 3.6
- Added support for status code 451 and 423
- Improved the build error suggestions.  In particular only if
  someone stringifies the error will the suggestions be calculated.
- Added support for uWSGI's caching backend.
- Fix a bug where iterating over a `FileStorage` would result in an infinite
  loop.
- Datastructures now inherit from the relevant baseclasses from the
  `collections` module in the stdlib. See #794.
- Add support for recognizing NetBSD, OpenBSD, FreeBSD, DragonFlyBSD platforms
  in the user agent string.
- Recognize SeaMonkey browser name and version correctly
- Recognize Baiduspider, and bingbot user agents
- If `LocalProxy`'s wrapped object is a function, refer to it with __wrapped__
  attribute.
- The defaults of ``generate_password_hash`` have been changed to more secure
  ones, see pull request ``#753``.
- Add support for encoding in options header parsing, see pull request
  ``#933``.
- ``test.Client`` now properly handles Location headers with relative URLs, see
  pull request ``#879``.
- When `HTTPException` is raised, it now prints the description, for easier
  debugging.
- Werkzeug's dict-like datastructures now have ``view``-methods under Python 2,
  see pull request ``#968``.
- Fix a bug in ``MultiPartParser`` when no ``stream_factory`` was provided
  during initialization, see pull request ``#973``.
- Disable autocorrect and spellchecker in the debugger middleware's Python
  prompt, see pull request ``#994``.
- Don't redirect to slash route when method doesn't match, see pull request
  ``#907``.
- Fix a bug when using ``SharedDataMiddleware`` with frozen packages, see pull
  request ``#959``.
- `Range` header parsing function fixed for invalid values ``#974``.
- Add support for byte Range Requests, see pull request ``#978``.
- Use modern cryptographic defaults in the dev servers ``#1004``.
- the post() method of the test client now accept file object through the data
  parameter.
- Color run_simple's terminal output based on HTTP codes ``#1013``.
- Fix self-XSS in debugger console, see ``#1031``.
- Fix IPython 5.x shell support, see ``#1033``.
- Change Accept datastructure to sort by specificity first, allowing for more
  accurate results when using ``best_match`` for mime types (for example in
  ``requests.accept_mimetypes.best_match``)

Version 0.11.16
---------------

- werkzeug.serving: set CONTENT_TYPE / CONTENT_LENGTH if only they're provided by the client
- werkzeug.serving: Fix crash of reloader when using `python -m werkzeug.serving`.

Version 0.11.15
---------------

Released on December 30th 2016.

- Bugfix for the bugfix in the previous release.

Version 0.11.14
---------------

Released on December 30th 2016.

- Check if platform can fork before importing ``ForkingMixIn``, raise exception
  when creating ``ForkingWSGIServer`` on such a platform, see PR ``#999``.

Version 0.11.13
---------------

Released on December 26th 2016.

- Correct fix for the reloader issuer on certain Windows installations.

Version 0.11.12
---------------

Released on December 26th 2016.

- Fix more bugs in multidicts regarding empty lists. See ``#1000``.
- Add some docstrings to some `EnvironBuilder` properties that were previously
  unintentionally missing.
- Added a workaround for the reloader on windows.

Version 0.11.11
---------------

Released on August 31st 2016.

- Fix JSONRequestMixin for Python3. See #731
- Fix broken string handling in test client when passing integers. See #852
- Fix a bug in ``parse_options_header`` where an invalid content type
  starting with comma or semi-colon would result in an invalid return value,
  see issue ``#995``.
- Fix a bug in multidicts when passing empty lists as values, see issue
  ``#979``.
- Fix a security issue that allows XSS on the Werkzeug debugger. See ``#1001``.

Version 0.11.10
---------------

Released on May 24th 2016.

- Fixed a bug that occurs when running on Python 2.6 and using a broken locale.
  See pull request #912.
- Fixed a crash when running the debugger on Google App Engine. See issue #925.
- Fixed an issue with multipart parsing that could cause memory exhaustion.

Version 0.11.9
--------------

Released on April 24th 2016.

- Corrected an issue that caused the debugger not to use the
  machine GUID on POSIX systems.
- Corrected a Unicode error on Python 3 for the debugger's
  PIN usage.
- Corrected the timestamp verification in the pin debug code.
  Without this fix the pin was remembered for too long.

Version 0.11.8
--------------

Released on April 15th 2016.

- fixed a problem with the machine GUID detection code on OS X
  on Python 3.

Version 0.11.7
--------------

Released on April 14th 2016.

- fixed a regression on Python 3 for the debugger.

Version 0.11.6
--------------

Released on April 14th 2016.

- werkzeug.serving: Still show the client address on bad requests.
- improved the PIN based protection for the debugger to make it harder to
  brute force via trying cookies.  Please keep in mind that the debugger
  *is not intended for running on production environments*
- increased the pin timeout to a week to make it less annoying for people
  which should decrease the chance that users disable the pin check
  entirely.
- werkzeug.serving: Fix broken HTTP_HOST when path starts with double slash.

Version 0.11.5
--------------

Released on March 22nd 2016.

- werkzeug.serving: Fix crash when attempting SSL connection to HTTP server.

Version 0.11.4
--------------

Released on February 14th 2016.

- Fixed werkzeug.serving not working from -m flag.
- Fixed incorrect weak etag handling.

Version 0.11.3
--------------

Released on December 20th 2015.

- Fixed an issue with copy operations not working against
  proxies.
- Changed the logging operations of the development server to
  correctly log where the server is running in all situations
  again.
- Fixed another regression with SSL wrapping similar to the
  fix in 0.11.2 but for a different code path.

Version 0.11.2
--------------

Released on November 12th 2015.

- Fix inheritable sockets on Windows on Python 3.
- Fixed an issue with the forking server not starting any longer.
- Fixed SSL wrapping on platforms that supported opening sockets
  by file descriptor.
- No longer log from the watchdog reloader.
- Unicode errors in hosts are now better caught or converted into
  bad request errors.

Version 0.11.1
--------------

Released on November 10th 2015.

- Fixed a regression on Python 3 in the debugger.

Version 0.11
------------

Released on November 8th 2015, codename Gleisbaumaschine.

- Added ``reloader_paths`` option to ``run_simple`` and other functions in
  ``werkzeug.serving``. This allows the user to completely override the Python
  module watching of Werkzeug with custom paths.
- Many custom cached properties of Werkzeug's classes are now subclasses of
  Python's ``property`` type (issue ``#616``).
- ``bind_to_environ`` now doesn't differentiate between implicit and explicit
  default port numbers in ``HTTP_HOST`` (pull request ``#204``).
- ``BuildErrors`` are now more informative. They come with a complete sentence
  as error message, and also provide suggestions (pull request ``#691``).
- Fix a bug in the user agent parser where Safari's build number instead of
  version would be extracted (pull request ``#703``).
- Fixed issue where RedisCache set_many was broken for twemproxy, which doesn't
  support the default MULTI command (pull request ``#702``).
- ``mimetype`` parameters on request and response classes are now always
  converted to lowercase.
- Changed cache so that cache never expires if timeout is 0. This also fixes
  an issue with redis setex (issue ``#550``)
- Werkzeug now assumes ``UTF-8`` as filesystem encoding on Unix if Python
  detected it as ASCII.
- New optional `has` method on caches.
- Fixed various bugs in `parse_options_header` (pull request ``#643``).
- If the reloader is enabled the server will now open the socket in the parent
  process if this is possible.  This means that when the reloader kicks in
  the connection from client will wait instead of tearing down.  This does
  not work on all Python versions.
- Implemented PIN based authentication for the debugger.  This can optionally
  be disabled but is discouraged.  This change was necessary as it has been
  discovered that too many people run the debugger in production.
- Devserver no longer requires SSL module to be installed.

Version 0.10.5
--------------

(bugfix release, release date yet to be decided)

- Reloader: Correctly detect file changes made by moving temporary files over
  the original, which is e.g. the case with PyCharm (pull request ``#722``).
- Fix bool behavior of ``werkzeug.datastructures.ETags`` under Python 3 (issue
  ``#744``).

Version 0.10.4
--------------

(bugfix release, released on March 26th 2015)

- Re-release of 0.10.3 with packaging artifacts manually removed.

Version 0.10.3
--------------

(bugfix release, released on March 26th 2015)

- Re-release of 0.10.2 without packaging artifacts.

Version 0.10.2
--------------

(bugfix release, released on March 26th 2015)

- Fixed issue where ``empty`` could break third-party libraries that relied on
  keyword arguments (pull request ``#675``)
- Improved ``Rule.empty`` by providing a ```get_empty_kwargs`` to allow setting
  custom kwargs without having to override entire ``empty`` method. (pull
  request ``#675``)
- Fixed ```extra_files``` parameter for reloader to not cause startup
  to crash when included in server params
- Using `MultiDict` when building URLs is now not supported again. The behavior
  introduced several regressions.
- Fix performance problems with stat-reloader (pull request ``#715``).

Version 0.10.1
--------------

(bugfix release, released on February 3rd 2015)

- Fixed regression with multiple query values for URLs (pull request ``#667``).
- Fix issues with eventlet's monkeypatching and the builtin server (pull
  request ``#663``).

Version 0.10
------------

Released on January 30th 2015, codename Bagger.

- Changed the error handling of and improved testsuite for the caches in
  ``contrib.cache``.
- Fixed a bug on Python 3 when creating adhoc ssl contexts, due to `sys.maxint`
  not being defined.
- Fixed a bug on Python 3, that caused
  :func:`~werkzeug.serving.make_ssl_devcert` to fail with an exception.
- Added exceptions for 504 and 505.
- Added support for ChromeOS detection.
- Added UUID converter to the routing system.
- Added message that explains how to quit the server.
- Fixed a bug on Python 2, that caused ``len`` for
  :class:`werkzeug.datastructures.CombinedMultiDict` to crash.
- Added support for stdlib pbkdf2 hmac if a compatible digest
  is found.
- Ported testsuite to use ``py.test``.
- Minor optimizations to various middlewares (pull requests ``#496`` and
  ``#571``).
- Use stdlib ``ssl`` module instead of ``OpenSSL`` for the builtin server
  (issue ``#434``). This means that OpenSSL contexts are not supported anymore,
  but instead ``ssl.SSLContext`` from the stdlib.
- Allow protocol-relative URLs when building external URLs.
- Fixed Atom syndication to print time zone offset for tz-aware datetime
  objects (pull request ``#254``).
- Improved reloader to track added files and to recover from broken
  sys.modules setups with syntax errors in packages.
- ``cache.RedisCache`` now supports arbitrary ``**kwargs`` for the redis
  object.
- ``werkzeug.test.Client`` now uses the original request method when resolving
  307 redirects (pull request ``#556``).
- ``werkzeug.datastructures.MIMEAccept`` now properly deals with mimetype
  parameters (pull request ``#205``).
- ``werkzeug.datastructures.Accept`` now handles a quality of ``0`` as
  intolerable, as per RFC 2616 (pull request ``#536``).
- ``werkzeug.urls.url_fix`` now properly encodes hostnames with ``idna``
  encoding (issue ``#559``). It also doesn't crash on malformed URLs anymore
  (issue ``#582``).
- ``werkzeug.routing.MapAdapter.match`` now recognizes the difference between
  the path ``/`` and an empty one (issue ``#360``).
- The interactive debugger now tries to decode non-ascii filenames (issue
  ``#469``).
- Increased default key size of generated SSL certificates to 1024 bits (issue
  ``#611``).
- Added support for specifying a ``Response`` subclass to use when calling
  :func:`~werkzeug.utils.redirect`\ .
- ``werkzeug.test.EnvironBuilder`` now doesn't use the request method anymore
  to guess the content type, and purely relies on the ``form``, ``files`` and
  ``input_stream`` properties (issue ``#620``).
- Added Symbian to the user agent platform list.
- Fixed make_conditional to respect automatically_set_content_length
- Unset ``Content-Length`` when writing to response.stream (issue ``#451``)
- ``wrappers.Request.method`` is now always uppercase, eliminating
  inconsistencies of the WSGI environment (issue ``647``).
- ``routing.Rule.empty`` now works correctly with subclasses of ``Rule`` (pull
  request ``#645``).
- Made map updating safe in light of concurrent updates.
- Allow multiple values for the same field for url building (issue ``#658``).

Version 0.9.7
-------------

(bugfix release, release date to be decided)

- Fix unicode problems in ``werkzeug.debug.tbtools``.
- Fix Python 3-compatibility problems in ``werkzeug.posixemulation``.
- Backport fix of fatal typo for ``ImmutableList`` (issue ``#492``).
- Make creation of the cache dir for ``FileSystemCache`` atomic (issue
  ``#468``).
- Use native strings for memcached keys to work with Python 3 client (issue
  ``#539``).
- Fix charset detection for ``werkzeug.debug.tbtools.Frame`` objects (issues
  ``#547`` and ``#532``).
- Fix ``AttributeError`` masking in ``werkzeug.utils.import_string`` (issue
  ``#182``).
- Explicitly shut down server (issue ``#519``).
- Fix timeouts greater than 2592000 being misinterpreted as UNIX timestamps in
  ``werkzeug.contrib.cache.MemcachedCache`` (issue ``#533``).
- Fix bug where ``werkzeug.exceptions.abort`` would raise an arbitrary subclass
  of the expected class (issue ``#422``).
- Fix broken ``jsrouting`` (due to removal of ``werkzeug.templates``)
- ``werkzeug.urls.url_fix`` now doesn't crash on malformed URLs anymore, but
  returns them unmodified. This is a cheap workaround for ``#582``, the proper
  fix is included in version 0.10.
- The repr of ``werkzeug.wrappers.Request`` doesn't crash on non-ASCII-values
  anymore (pull request ``#466``).
- Fix bug in ``cache.RedisCache`` when combined with ``redis.StrictRedis``
  object (pull request ``#583``).
- The ``qop`` parameter for ``WWW-Authenticate`` headers is now always quoted,
  as required by RFC 2617 (issue ``#633``).
- Fix bug in ``werkzeug.contrib.cache.SimpleCache`` with Python 3 where add/set
  may throw an exception when pruning old entries from the cache (pull request
  ``#651``).

Version 0.9.6
-------------

(bugfix release, released on June 7th 2014)

- Added a safe conversion for IRI to URI conversion and use that
  internally to work around issues with spec violations for
  protocols such as ``itms-service``.

Version 0.9.7
-------------

- Fixed uri_to_iri() not re-encoding hashes in query string parameters.

Version 0.9.5
-------------

(bugfix release, released on June 7th 2014)

- Forward charset argument from request objects to the environ
  builder.
- Fixed error handling for missing boundaries in multipart data.
- Fixed session creation on systems without ``os.urandom()``.
- Fixed pluses in dictionary keys not being properly URL encoded.
- Fixed a problem with deepcopy not working for multi dicts.
- Fixed a double quoting issue on redirects.
- Fixed a problem with unicode keys appearing in headers on 2.x.
- Fixed a bug with unicode strings in the test builder.
- Fixed a unicode bug on Python 3 in the WSGI profiler.
- Fixed an issue with the safe string compare function on
  Python 2.7.7 and Python 3.4.

Version 0.9.4
-------------

(bugfix release, released on August 26th 2013)

- Fixed an issue with Python 3.3 and an edge case in cookie parsing.
- Fixed decoding errors not handled properly through the WSGI
  decoding dance.
- Fixed URI to IRI conversion incorrectly decoding percent signs.

Version 0.9.3
-------------

(bugfix release, released on July 25th 2013)

- Restored behavior of the ``data`` descriptor of the request class to pre 0.9
  behavior.  This now also means that ``.data`` and ``.get_data()`` have
  different behavior.  New code should use ``.get_data()`` always.

  In addition to that there is now a flag for the ``.get_data()`` method that
  controls what should happen with form data parsing and the form parser will
  honor cached data.  This makes dealing with custom form data more consistent.

Version 0.9.2
-------------

(bugfix release, released on July 18th 2013)

- Added ``unsafe`` parameter to ``urls.url_quote``.
- Fixed an issue with ``urls.url_quote_plus`` not quoting
  `'+'` correctly.
- Ported remaining parts of :class:`~werkzeug.contrib.RedisCache` to
  Python 3.3.
- Ported remaining parts of :class:`~werkzeug.contrib.MemcachedCache` to
  Python 3.3
- Fixed a deprecation warning in the contrib atom module.
- Fixed a regression with setting of content types through the
  headers dictionary instead with the content type parameter.
- Use correct name for stdlib secure string comparison function.
- Fixed a wrong reference in the docstring of
  :func:`~werkzeug.local.release_local`.
- Fixed an `AttributeError` that sometimes occurred when accessing the
  :attr:`werkzeug.wrappers.BaseResponse.is_streamed` attribute.

Version 0.9.1
-------------

(bugfix release, released on June 14th 2013)

- Fixed an issue with integers no longer being accepted in certain
  parts of the routing system or URL quoting functions.
- Fixed an issue with `url_quote` not producing the right escape
  codes for single digit codepoints.
- Fixed an issue with :class:`~werkzeug.wsgi.SharedDataMiddleware` not
  reading the path correctly and breaking on etag generation in some
  cases.
- Properly handle `Expect: 100-continue` in the development server
  to resolve issues with curl.
- Automatically exhaust the input stream on request close.  This should
  fix issues where not touching request files results in a timeout.
- Fixed exhausting of streams not doing anything if a non-limited
  stream was passed into the multipart parser.
- Raised the buffer sizes for the multipart parser.

Version 0.9
-----------

Released on June 13nd 2013, codename Planierraupe.

- Added support for :meth:`~werkzeug.wsgi.LimitedStream.tell`
  on the limited stream.
- :class:`~werkzeug.datastructures.ETags` now is nonzero if it
  contains at least one etag of any kind, including weak ones.
- Added a workaround for a bug in the stdlib for SSL servers.
- Improved SSL interface of the devserver so that it can generate
  certificates easily and load them from files.
- Refactored test client to invoke the open method on the class
  for redirects.  This makes subclassing more powerful.
- ``wsgi.make_chunk_iter`` and ``make_line_iter`` now support processing
  of iterators and streams.
- URL generation by the routing system now no longer quotes
  ``+``.
- URL fixing now no longer quotes certain reserved characters.
- The :func:`werkzeug.security.generate_password_hash` and
  check functions now support any of the hashlib algorithms.
- `wsgi.get_current_url` is now ascii safe for browsers sending
  non-ascii data in query strings.
- improved parsing behavior for :func:`werkzeug.http.parse_options_header`
- added more operators to local proxies.
- added a hook to override the default converter in the routing
  system.
- The description field of HTTP exceptions is now always escaped.
  Use markup objects to disable that.
- Added number of proxy argument to the proxy fix to make it more
  secure out of the box on common proxy setups.  It will by default
  no longer trust the x-forwarded-for header as much as it did
  before.
- Added support for fragment handling in URI/IRI functions.
- Added custom class support for :func:`werkzeug.http.parse_dict_header`.
- Renamed `LighttpdCGIRootFix` to `CGIRootFix`.
- Always treat `+` as safe when fixing URLs as people love misusing them.
- Added support to profiling into directories in the contrib profiler.
- The escape function now by default escapes quotes.
- Changed repr of exceptions to be less magical.
- Simplified exception interface to no longer require environments
  to be passed to receive the response object.
- Added sentinel argument to IterIO objects.
- Added pbkdf2 support for the security module.
- Added a plain request type that disables all form parsing to only
  leave the stream behind.
- Removed support for deprecated `fix_headers`.
- Removed support for deprecated `header_list`.
- Removed support for deprecated parameter for `iter_encoded`.
- Removed support for deprecated non-silent usage of the limited
  stream object.
- Removed support for previous dummy `writable` parameter on
  the cached property.
- Added support for explicitly closing request objects to close
  associated resources.
- Conditional request handling or access to the data property on responses no
  longer ignores direct passthrough mode.
- Removed werkzeug.templates and werkzeug.contrib.kickstart.
- Changed host lookup logic for forwarded hosts to allow lists of
  hosts in which case only the first one is picked up.
- Added `wsgi.get_query_string`, `wsgi.get_path_info` and
  `wsgi.get_script_name` and made the `wsgi.pop_path_info` and
  `wsgi.peek_path_info` functions perform unicode decoding.  This
  was necessary to avoid having to expose the WSGI encoding dance
  on Python 3.
- Added `content_encoding` and `content_md5` to the request object's
  common request descriptor mixin.
- added `options` and `trace` to the test client.
- Overhauled the utilization of the input stream to be easier to use
  and better to extend.  The detection of content payload on the input
  side is now more compliant with HTTP by detecting off the content
  type header instead of the request method.  This also now means that
  the stream property on the request class is always available instead
  of just when the parsing fails.
- Added support for using :class:`werkzeug.wrappers.BaseResponse` in a with
  statement.
- Changed `get_app_iter` to fetch the response early so that it does not
  fail when wrapping a response iterable.  This makes filtering easier.
- Introduced `get_data` and `set_data` methods for responses.
- Introduced `get_data` for requests.
- Soft deprecated the `data` descriptors for request and response objects.
- Added `as_bytes` operations to some of the headers to simplify working
  with things like cookies.
- Made the debugger paste tracebacks into github's gist service as
  private pastes.

Version 0.8.4
-------------

(bugfix release, release date to be announced)

- Added a favicon to the debugger which fixes problem with
  state changes being triggered through a request to
  /favicon.ico in Google Chrome.  This should fix some
  problems with Flask and other frameworks that use
  context local objects on a stack with context preservation
  on errors.
- Fixed an issue with scrolling up in the debugger.
- Fixed an issue with debuggers running on a different URL
  than the URL root.
- Fixed a problem with proxies not forwarding some rarely
  used special methods properly.
- Added a workaround to prevent the XSS protection from Chrome
  breaking the debugger.
- Skip redis tests if redis is not running.
- Fixed a typo in the multipart parser that caused content-type
  to not be picked up properly.

Version 0.8.3
-------------

(bugfix release, released on February 5th 2012)

- Fixed another issue with ``wsgi.make_line_iter``
  where lines longer than the buffer size were not handled
  properly.
- Restore stdout after debug console finished executing so
  that the debugger can be used on GAE better.
- Fixed a bug with the redis cache for int subclasses
  (affects bool caching).
- Fixed an XSS problem with redirect targets coming from
  untrusted sources.
- Redis cache backend now supports password authentication.

Version 0.8.2
-------------

(bugfix release, released on December 16th 2011)

- Fixed a problem with request handling of the builtin server
  not responding to socket errors properly.
- The routing request redirect exception's code attribute is now
  used properly.
- Fixed a bug with shutdowns on Windows.
- Fixed a few unicode issues with non-ascii characters being
  hardcoded in URL rules.
- Fixed two property docstrings being assigned to fdel instead
  of ``__doc__``.
- Fixed an issue where CRLF line endings could be split into two
  by the line iter function, causing problems with multipart file
  uploads.

Version 0.8.1
-------------

(bugfix release, released on September 30th 2011)

- Fixed an issue with the memcache not working properly.
- Fixed an issue for Python 2.7.1 and higher that broke
  copying of multidicts with :func:`copy.copy`.
- Changed hashing methodology of immutable ordered multi dicts
  for a potential problem with alternative Python implementations.

Version 0.8
-----------

Released on September 29th 2011, codename Lötkolben

- Removed data structure specific KeyErrors for a general
  purpose :exc:`~werkzeug.exceptions.BadRequestKeyError`.
- Documented :meth:`werkzeug.wrappers.BaseRequest._load_form_data`.
- The routing system now also accepts strings instead of
  dictionaries for the `query_args` parameter since we're only
  passing them through for redirects.
- Werkzeug now automatically sets the content length immediately when
  the :attr:`~werkzeug.wrappers.BaseResponse.data` attribute is set
  for efficiency and simplicity reasons.
- The routing system will now normalize server names to lowercase.
- The routing system will no longer raise ValueErrors in case the
  configuration for the server name was incorrect.  This should make
  deployment much easier because you can ignore that factor now.
- Fixed a bug with parsing HTTP digest headers.  It rejected headers
  with missing nc and nonce params.
- Proxy fix now also updates wsgi.url_scheme based on X-Forwarded-Proto.
- Added support for key prefixes to the redis cache.
- Added the ability to suppress some auto corrections in the wrappers
  that are now controlled via `autocorrect_location_header` and
  `automatically_set_content_length` on the response objects.
- Werkzeug now uses a new method to check that the length of incoming
  data is complete and will raise IO errors by itself if the server
  fails to do so.
- ``wsgi.make_line_iter`` now requires a limit that is
  not higher than the length the stream can provide.
- Refactored form parsing into a form parser class that makes it possible
  to hook into individual parts of the parsing process for debugging and
  extending.
- For conditional responses the content length is no longer set when it
  is already there and added if missing.
- Immutable datastructures are hashable now.
- Headers datastructure no longer allows newlines in values to avoid
  header injection attacks.
- Made it possible through subclassing to select a different remote
  addr in the proxy fix.
- Added stream based URL decoding.  This reduces memory usage on large
  transmitted form data that is URL decoded since Werkzeug will no longer
  load all the unparsed data into memory.
- Memcache client now no longer uses the buggy cmemcache module and
  supports pylibmc.  GAE is not tried automatically and the dedicated
  class is no longer necessary.
- Redis cache now properly serializes data.
- Removed support for Python 2.4

Version 0.7.2
-------------

(bugfix release, released on September 30th 2011)

- Fixed a CSRF problem with the debugger.
- The debugger is now generating private pastes on lodgeit.
- If URL maps are now bound to environments the query arguments
  are properly decoded from it for redirects.

Version 0.7.1
-------------

(bugfix release, released on July 26th 2011)

- Fixed a problem with newer versions of IPython.
- Disabled pyinotify based reloader which does not work reliably.

Version 0.7
-----------

Released on July 24th 2011, codename Schraubschlüssel

- Add support for python-libmemcached to the Werkzeug cache abstraction
  layer.
- Improved :func:`url_decode` and :func:`url_encode` performance.
- Fixed an issue where the SharedDataMiddleware could cause an
  internal server error on weird paths when loading via pkg_resources.
- Fixed an URL generation bug that caused URLs to be invalid if a
  generated component contains a colon.
- :func:`werkzeug.import_string` now works with partially set up
  packages properly.
- Disabled automatic socket switching for IPv6 on the development
  server due to problems it caused.
- Werkzeug no longer overrides the Date header when creating a
  conditional HTTP response.
- The routing system provides a method to retrieve the matching
  methods for a given path.
- The routing system now accepts a parameter to change the encoding
  error behaviour.
- The local manager can now accept custom ident functions in the
  constructor that are forwarded to the wrapped local objects.
- url_unquote_plus now accepts unicode strings again.
- Fixed an issue with the filesystem session support's prune
  function and concurrent usage.
- Fixed a problem with external URL generation discarding the port.
- Added support for pylibmc to the Werkzeug cache abstraction layer.
- Fixed an issue with the new multipart parser that happened when
  a linebreak happened to be on the chunk limit.
- Cookies are now set properly if ports are in use.  A runtime error
  is raised if one tries to set a cookie for a domain without a dot.
- Fixed an issue with Template.from_file not working for file
  descriptors.
- Reloader can now use inotify to track reloads.  This requires the
  pyinotify library to be installed.
- Werkzeug debugger can now submit to custom lodgeit installations.
- redirect function's status code assertion now allows 201 to be used
  as redirection code.  While it's not a real redirect, it shares
  enough with redirects for the function to still be useful.
- Fixed securecookie for pypy.
- Fixed `ValueErrors` being raised on calls to `best_match` on
  `MIMEAccept` objects when invalid user data was supplied.
- Deprecated `werkzeug.contrib.kickstart` and `werkzeug.contrib.testtools`
- URL routing now can be passed the URL arguments to keep them for
  redirects.  In the future matching on URL arguments might also be
  possible.
- Header encoding changed from utf-8 to latin1 to support a port to
  Python 3.  Bytestrings passed to the object stay untouched which
  makes it possible to have utf-8 cookies.  This is a part where
  the Python 3 version will later change in that it will always
  operate on latin1 values.
- Fixed a bug in the form parser that caused the last character to
  be dropped off if certain values in multipart data are used.
- Multipart parser now looks at the part-individual content type
  header to override the global charset.
- Introduced mimetype and mimetype_params attribute for the file
  storage object.
- Changed FileStorage filename fallback logic to skip special filenames
  that Python uses for marking special files like stdin.
- Introduced more HTTP exception classes.
- `call_on_close` now can be used as a decorator.
- Support for redis as cache backend.
- Added `BaseRequest.scheme`.
- Support for the RFC 5789 PATCH method.
- New custom routing parser and better ordering.
- Removed support for `is_behind_proxy`.  Use a WSGI middleware
  instead that rewrites the `REMOTE_ADDR` according to your setup.
  Also see the :class:`werkzeug.contrib.fixers.ProxyFix` for
  a drop-in replacement.
- Added cookie forging support to the test client.
- Added support for host based matching in the routing system.
- Switched from the default 'ignore' to the better 'replace'
  unicode error handling mode.
- The builtin server now adds a function named 'werkzeug.server.shutdown'
  into the WSGI env to initiate a shutdown.  This currently only works
  in Python 2.6 and later.
- Headers are now assumed to be latin1 for better compatibility with
  Python 3 once we have support.
- Added :func:`werkzeug.security.safe_join`.
- Added `accept_json` property analogous to `accept_html` on the
  :class:`werkzeug.datastructures.MIMEAccept`.
- :func:`werkzeug.utils.import_string` now fails with much better
  error messages that pinpoint to the problem.
- Added support for parsing of the `If-Range` header
  (:func:`werkzeug.http.parse_if_range_header` and
  :class:`werkzeug.datastructures.IfRange`).
- Added support for parsing of the `Range` header
  (:func:`werkzeug.http.parse_range_header` and
  :class:`werkzeug.datastructures.Range`).
- Added support for parsing of the `Content-Range` header of responses
  and provided an accessor object for it
  (:func:`werkzeug.http.parse_content_range_header` and
  :class:`werkzeug.datastructures.ContentRange`).

Version 0.6.2
-------------

(bugfix release, released on April 23th 2010)

- renamed the attribute `implicit_seqence_conversion` attribute of the
  request object to `implicit_sequence_conversion`.

Version 0.6.1
-------------

(bugfix release, released on April 13th 2010)

- heavily improved local objects.  Should pick up standalone greenlet
  builds now and support proxies to free callables as well.  There is
  also a stacked local now that makes it possible to invoke the same
  application from within itself by pushing current request/response
  on top of the stack.
- routing build method will also build non-default method rules properly
  if no method is provided.
- added proper IPv6 support for the builtin server.
- windows specific filesystem session store fixes.
  (should now be more stable under high concurrency)
- fixed a `NameError` in the session system.
- fixed a bug with empty arguments in the werkzeug.script system.
- fixed a bug where log lines will be duplicated if an application uses
  :meth:`logging.basicConfig` (#499)
- added secure password hashing and checking functions.
- `HEAD` is now implicitly added as method in the routing system if
  `GET` is present.  Not doing that was considered a bug because often
  code assumed that this is the case and in web servers that do not
  normalize `HEAD` to `GET` this could break `HEAD` requests.
- the script support can start SSL servers now.

Version 0.6
-----------

Released on Feb 19th 2010, codename Hammer.

- removed pending deprecations
- sys.path is now printed from the testapp.
- fixed an RFC 2068 incompatibility with cookie value quoting.
- the :class:`FileStorage` now gives access to the multipart headers.
- `cached_property.writeable` has been deprecated.
- :meth:`MapAdapter.match` now accepts a `return_rule` keyword argument
  that returns the matched `Rule` instead of just the `endpoint`
- :meth:`routing.Map.bind_to_environ` raises a more correct error message
  now if the map was bound to an invalid WSGI environment.
- added support for SSL to the builtin development server.
- Response objects are no longer modified in place when they are evaluated
  as WSGI applications.  For backwards compatibility the `fix_headers`
  function is still called in case it was overridden.
  You should however change your application to use `get_wsgi_headers` if
  you need header modifications before responses are sent as the backwards
  compatibility support will go away in future versions.
- :func:`append_slash_redirect` no longer requires the QUERY_STRING to be
  in the WSGI environment.
- added :class:`~werkzeug.contrib.wrappers.DynamicCharsetResponseMixin`
- added :class:`~werkzeug.contrib.wrappers.DynamicCharsetRequestMixin`
- added :attr:`BaseRequest.url_charset`
- request and response objects have a default `__repr__` now.
- builtin data structures can be pickled now.
- the form data parser will now look at the filename instead the
  content type to figure out if it should treat the upload as regular
  form data or file upload.  This fixes a bug with Google Chrome.
- improved performance of ``make_line_iter`` and the multipart parser
  for binary uploads.
- fixed :attr:`~werkzeug.BaseResponse.is_streamed`
- fixed a path quoting bug in `EnvironBuilder` that caused PATH_INFO and
  SCRIPT_NAME to end up in the environ unquoted.
- :meth:`werkzeug.BaseResponse.freeze` now sets the content length.
- for unknown HTTP methods the request stream is now always limited
  instead of being empty.  This makes it easier to implement DAV
  and other protocols on top of Werkzeug.
- added :meth:`werkzeug.MIMEAccept.best_match`
- multi-value test-client posts from a standard dictionary are now
  supported.  Previously you had to use a multi dict.
- rule templates properly work with submounts, subdomains and
  other rule factories now.
- deprecated non-silent usage of the :class:`werkzeug.LimitedStream`.
- added support for IRI handling to many parts of Werkzeug.
- development server properly logs to the werkzeug logger now.
- added :func:`werkzeug.extract_path_info`
- fixed a querystring quoting bug in :func:`url_fix`
- added `fallback_mimetype` to :class:`werkzeug.SharedDataMiddleware`.
- deprecated :meth:`BaseResponse.iter_encoded`'s charset parameter.
- added :meth:`BaseResponse.make_sequence`,
  :attr:`BaseResponse.is_sequence` and
  :meth:`BaseResponse._ensure_sequence`.
- added better __repr__ of :class:`werkzeug.Map`
- `import_string` accepts unicode strings as well now.
- development server doesn't break on double slashes after the host name.
- better `__repr__` and `__str__` of
  :exc:`werkzeug.exceptions.HTTPException`
- test client works correctly with multiple cookies now.
- the :class:`werkzeug.routing.Map` now has a class attribute with
  the default converter mapping.  This helps subclasses to override
  the converters without passing them to the constructor.
- implemented :class:`OrderedMultiDict`
- improved the session support for more efficient session storing
  on the filesystem.  Also added support for listing of sessions
  currently stored in the filesystem session store.
- werkzeug no longer utilizes the Python time module for parsing
  which means that dates in a broader range can be parsed.
- the wrappers have no class attributes that make it possible to
  swap out the dict and list types it uses.
- werkzeug debugger should work on the appengine dev server now.
- the URL builder supports dropping of unexpected arguments now.
  Previously they were always appended to the URL as query string.
- profiler now writes to the correct stream.

Version 0.5.1
-------------
(bugfix release for 0.5, released on July 9th 2009)

- fixed boolean check of :class:`FileStorage`
- url routing system properly supports unicode URL rules now.
- file upload streams no longer have to provide a truncate()
  method.
- implemented :meth:`BaseRequest._form_parsing_failed`.
- fixed #394
- :meth:`ImmutableDict.copy`, :meth:`ImmutableMultiDict.copy` and
  :meth:`ImmutableTypeConversionDict.copy` return mutable shallow
  copies.
- fixed a bug with the `make_runserver` script action.
- :meth:`MultiDict.items` and :meth:`MutiDict.iteritems` now accept an
  argument to return a pair for each value of each key.
- the multipart parser works better with hand-crafted multipart
  requests now that have extra newlines added.  This fixes a bug
  with setuptools uploads not handled properly (#390)
- fixed some minor bugs in the atom feed generator.
- fixed a bug with client cookie header parsing being case sensitive.
- fixed a not-working deprecation warning.
- fixed package loading for :class:`SharedDataMiddleware`.
- fixed a bug in the secure cookie that made server-side expiration
  on servers with a local time that was not set to UTC impossible.
- fixed console of the interactive debugger.


Version 0.5
-----------

Released on April 24th, codename Schlagbohrer.

- requires Python 2.4 now
- fixed a bug in :class:`~contrib.IterIO`
- added :class:`MIMEAccept` and :class:`CharsetAccept` that work like the
  regular :class:`Accept` but have extra special normalization for mimetypes
  and charsets and extra convenience methods.
- switched the serving system from wsgiref to something homebrew.
- the :class:`Client` now supports cookies.
- added the :mod:`~werkzeug.contrib.fixers` module with various
  fixes for webserver bugs and hosting setup side-effects.
- added :mod:`werkzeug.contrib.wrappers`
- added :func:`is_hop_by_hop_header`
- added :func:`is_entity_header`
- added :func:`remove_hop_by_hop_headers`
- added :func:`pop_path_info`
- added :func:`peek_path_info`
- added :func:`wrap_file` and :class:`FileWrapper`
- moved `LimitedStream` from the contrib package into the regular
  werkzeug one and changed the default behavior to raise exceptions
  rather than stopping without warning.  The old class will stick in
  the module until 0.6.
- implemented experimental multipart parser that replaces the old CGI hack.
- added :func:`dump_options_header` and :func:`parse_options_header`
- added :func:`quote_header_value` and :func:`unquote_header_value`
- :func:`url_encode` and :func:`url_decode` now accept a separator
  argument to switch between `&` and `;` as pair separator.  The magic
  switch is no longer in place.
- all form data parsing functions as well as the :class:`BaseRequest`
  object have parameters (or attributes) to limit the number of
  incoming bytes (either totally or per field).
- added :class:`LanguageAccept`
- request objects are now enforced to be read only for all collections.
- added many new collection classes, refactored collections in general.
- test support was refactored, semi-undocumented `werkzeug.test.File`
  was replaced by :class:`werkzeug.FileStorage`.
- :class:`EnvironBuilder` was added and unifies the previous distinct
  :func:`create_environ`, :class:`Client` and
  :meth:`BaseRequest.from_values`.  They all work the same now which
  is less confusing.
- officially documented imports from the internal modules as undefined
  behavior.  These modules were never exposed as public interfaces.
- removed `FileStorage.__len__` which previously made the object
  falsy for browsers not sending the content length which all browsers
  do.
- :class:`SharedDataMiddleware` uses `wrap_file` now and has a
  configurable cache timeout.
- added :class:`CommonRequestDescriptorsMixin`
- added :attr:`CommonResponseDescriptorsMixin.mimetype_params`
- added :mod:`werkzeug.contrib.lint`
- added `passthrough_errors` to `run_simple`.
- added `secure_filename`
- added ``make_line_iter``
- :class:`MultiDict` copies now instead of revealing internal
  lists to the caller for `getlist` and iteration functions that
  return lists.
- added :attr:`follow_redirect` to the :func:`open` of :class:`Client`.
- added support for `extra_files` in
  :func:`~werkzeug.script.make_runserver`

Version 0.4.1
-------------

(Bugfix release, released on January 11th 2009)

- `werkzeug.contrib.cache.Memcached` accepts now objects that
  implement the memcache.Client interface as alternative to a list of
  strings with server addresses.
  There is also now a `GAEMemcachedCache` that connects to the Google
  appengine cache.
- explicitly convert secret keys to bytestrings now because Python
  2.6 no longer does that.
- `url_encode` and all interfaces that call it, support ordering of
  options now which however is disabled by default.
- the development server no longer resolves the addresses of clients.
- Fixed a typo in `werkzeug.test` that broke `File`.
- `Map.bind_to_environ` uses the `Host` header now if available.
- Fixed `BaseCache.get_dict` (#345)
- `werkzeug.test.Client` can now run the application buffered in which
  case the application is properly closed automatically.
- Fixed `Headers.set` (#354).  Caused header duplication before.
- Fixed `Headers.pop` (#349).  default parameter was not properly
  handled.
- Fixed UnboundLocalError in `create_environ` (#351)
- `Headers` is more compatible with wsgiref now.
- `Template.render` accepts multidicts now.
- dropped support for Python 2.3

Version 0.4
-----------

Released on November 23rd 2008, codename Schraubenzieher.

- `Client` supports an empty `data` argument now.
- fixed a bug in `Response.application` that made it impossible to use it
  as method decorator.
- the session system should work on appengine now
- the secure cookie works properly in load balanced environments with
  different cpu architectures now.
- `CacheControl.no_cache` and `CacheControl.private` behavior changed to
  reflect the possibilities of the HTTP RFC.  Setting these attributes to
  `None` or `True` now sets the value to "the empty value".
  More details in the documentation.
- fixed `werkzeug.contrib.atom.AtomFeed.__call__`. (#338)
- `BaseResponse.make_conditional` now always returns `self`.  Previously
  it didn't for post requests and such.
- fixed a bug in boolean attribute handling of `html` and `xhtml`.
- added graceful error handling to the debugger pastebin feature.
- added a more list like interface to `Headers` (slicing and indexing
  works now)
- fixed a bug with the `__setitem__` method of `Headers` that didn't
  properly remove all keys on replacing.
- added `remove_entity_headers` which removes all entity headers from
  a list of headers (or a `Headers` object)
- the responses now automatically call `remove_entity_headers` if the
  status code is 304.
- fixed a bug with `Href` query parameter handling.  Previously the last
  item of a call to `Href` was not handled properly if it was a dict.
- headers now support a `pop` operation to better work with environ
  properties.


Version 0.3.1
-------------

(bugfix release, released on June 24th 2008)

- fixed a security problem with `werkzeug.contrib.SecureCookie`.


Version 0.3
-----------

Released on June 14th 2008, codename EUR325CAT6.

- added support for redirecting in url routing.
- added `Authorization` and `AuthorizationMixin`
- added `WWWAuthenticate` and `WWWAuthenticateMixin`
- added `parse_list_header`
- added `parse_dict_header`
- added `parse_authorization_header`
- added `parse_www_authenticate_header`
- added `_get_current_object` method to `LocalProxy` objects
- added `parse_form_data`
- `MultiDict`, `CombinedMultiDict`, `Headers`, and `EnvironHeaders` raise
  special key errors now that are subclasses of `BadRequest` so if you
  don't catch them they give meaningful HTTP responses.
- added support for alternative encoding error handling and the new
  `HTTPUnicodeError` which (if not caught) behaves like a `BadRequest`.
- added `BadRequest.wrap`.
- added ETag support to the SharedDataMiddleware and added an option
  to disable caching.
- fixed `is_xhr` on the request objects.
- fixed error handling of the url adapter's `dispatch` method. (#318)
- fixed bug with `SharedDataMiddleware`.
- fixed `Accept.values`.
- `EnvironHeaders` contain content-type and content-length now
- `url_encode` treats lists and tuples in dicts passed to it as multiple
  values for the same key so that one doesn't have to pass a `MultiDict`
  to the function.
- added `validate_arguments`
- added `BaseRequest.application`
- improved Python 2.3 support
- `run_simple` accepts `use_debugger` and `use_evalex` parameters now,
  like the `make_runserver` factory function from the script module.
- the `environ_property` is now read-only by default
- it's now possible to initialize requests as "shallow" requests which
  causes runtime errors if the request object tries to consume the
  input stream.


Version 0.2
-----------

Released Feb 14th 2008, codename Faustkeil.

- Added `AnyConverter` to the routing system.
- Added `werkzeug.contrib.securecookie`
- Exceptions have a ``get_response()`` method that return a response object
- fixed the path ordering bug (#293), thanks Thomas Johansson
- `BaseReporterStream` is now part of the werkzeug contrib module.  From
  Werkzeug 0.3 onwards you will have to import it from there.
- added `DispatcherMiddleware`.
- `RequestRedirect` is now a subclass of `HTTPException` and uses a
  301 status code instead of 302.
- `url_encode` and `url_decode` can optionally treat keys as unicode strings
  now, too.
- `werkzeug.script` has a different caller format for boolean arguments now.
- renamed `lazy_property` to `cached_property`.
- added `import_string`.
- added is_* properties to request objects.
- added `empty()` method to routing rules.
- added `werkzeug.contrib.profiler`.
- added `extends` to `Headers`.
- added `dump_cookie` and `parse_cookie`.
- added `as_tuple` to the `Client`.
- added `werkzeug.contrib.testtools`.
- added `werkzeug.unescape`
- added `BaseResponse.freeze`
- added `werkzeug.contrib.atom`
- the HTTPExceptions accept an argument `description` now which overrides the
  default description.
- the `MapAdapter` has a default for path info now.  If you use
  `bind_to_environ` you don't have to pass the path later.
- the wsgiref subclass werkzeug uses for the dev server does not use direct
  sys.stderr logging any more but a logger called "werkzeug".
- implemented `Href`.
- implemented `find_modules`
- refactored request and response objects into base objects, mixins and
  full featured subclasses that implement all mixins.
- added simple user agent parser
- werkzeug's routing raises `MethodNotAllowed` now if it matches a
  rule but for a different method.
- many fixes and small improvements


Version 0.1
-----------

Released on Dec 9th 2007, codename Wictorinoxger.

- Initial release
