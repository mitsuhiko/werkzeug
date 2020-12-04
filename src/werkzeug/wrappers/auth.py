from typing import TYPE_CHECKING

from ..http import parse_authorization_header
from ..http import parse_www_authenticate_header
from ..utils import cached_property
from werkzeug.types import WSGIEnvironment

if TYPE_CHECKING:
    from werkzeug.datastructures import WWWAuthenticate, Authorization


class AuthorizationMixin:
    """Adds an :attr:`authorization` property that represents the parsed
    value of the `Authorization` header as
    :class:`~werkzeug.datastructures.Authorization` object.
    """

    environ: WSGIEnvironment

    @cached_property
    def authorization(self) -> "Authorization":
        """The `Authorization` object in parsed form."""
        header = self.headers.get("Authorization")  # type: ignore
        return parse_authorization_header(header)


class WWWAuthenticateMixin:
    """Adds a :attr:`www_authenticate` property to a response object."""

    environ: WSGIEnvironment

    @property
    def www_authenticate(self) -> "WWWAuthenticate":
        """The `WWW-Authenticate` header in a parsed form."""

        def on_update(www_auth):
            if not www_auth and "www-authenticate" in self.headers:
                del self.headers["www-authenticate"]
            elif www_auth:
                self.headers["WWW-Authenticate"] = www_auth.to_header()

        header = self.headers.get("www-authenticate")  # type: ignore
        return parse_www_authenticate_header(header, on_update)
