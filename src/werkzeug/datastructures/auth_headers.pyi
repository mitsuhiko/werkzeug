from typing import Callable
from typing import Dict
from typing import FrozenSet
from typing import Iterable
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

from .mixins import ImmutableDictMixin
from .mixins import UpdateDictMixin
from .structures import HeaderSet

class Authorization(ImmutableDictMixin[str, str], Dict[str, str]):
    type: str
    def __init__(
        self,
        auth_type: str,
        data: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]] = None,
    ) -> None: ...
    @property
    def username(self) -> Optional[str]: ...
    @property
    def password(self) -> Optional[str]: ...
    @property
    def realm(self) -> Optional[str]: ...
    @property
    def nonce(self) -> Optional[str]: ...
    @property
    def uri(self) -> Optional[str]: ...
    @property
    def nc(self) -> Optional[str]: ...
    @property
    def cnonce(self) -> Optional[str]: ...
    @property
    def response(self) -> Optional[str]: ...
    @property
    def opaque(self) -> Optional[str]: ...
    @property
    def qop(self) -> Optional[str]: ...
    def to_header(self) -> str: ...

def auth_property(name: str, doc: Optional[str] = None) -> property: ...
def _set_property(name: str, doc: Optional[str] = None) -> property: ...

class WWWAuthenticate(UpdateDictMixin[str, str], Dict[str, str]):
    _require_quoting: FrozenSet[str]
    def __init__(
        self,
        auth_type: Optional[str] = None,
        values: Optional[Union[Mapping[str, str], Iterable[Tuple[str, str]]]] = None,
        on_update: Optional[Callable[[WWWAuthenticate], None]] = None,
    ) -> None: ...
    def set_basic(self, realm: str = ...) -> None: ...
    def set_digest(
        self,
        realm: str,
        nonce: str,
        qop: Iterable[str] = ("auth",),
        opaque: Optional[str] = None,
        algorithm: Optional[str] = None,
        stale: bool = False,
    ) -> None: ...
    def to_header(self) -> str: ...
    @property
    def type(self) -> Optional[str]: ...
    @type.setter
    def type(self, value: Optional[str]) -> None: ...
    @property
    def realm(self) -> Optional[str]: ...
    @realm.setter
    def realm(self, value: Optional[str]) -> None: ...
    @property
    def domain(self) -> HeaderSet: ...
    @property
    def nonce(self) -> Optional[str]: ...
    @nonce.setter
    def nonce(self, value: Optional[str]) -> None: ...
    @property
    def opaque(self) -> Optional[str]: ...
    @opaque.setter
    def opaque(self, value: Optional[str]) -> None: ...
    @property
    def algorithm(self) -> Optional[str]: ...
    @algorithm.setter
    def algorithm(self, value: Optional[str]) -> None: ...
    @property
    def qop(self) -> HeaderSet: ...
    @property
    def stale(self) -> Optional[bool]: ...
    @stale.setter
    def stale(self, value: Optional[bool]) -> None: ...
    @staticmethod
    def auth_property(name: str, doc: Optional[str] = None) -> property: ...
