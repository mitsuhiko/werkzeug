import code
import sys
from html import escape
from types import CodeType
from typing import Any
from typing import Callable
from typing import Dict
from typing import Hashable
from typing import List
from typing import Optional
from typing import Union

from ..local import Local
from .repr import debug_repr
from .repr import dump
from .repr import helper

_local = Local()


class HTMLStringO:
    """A StringO version that HTML escapes on write."""

    _buffer: List[str]

    def __init__(self) -> None:
        self._buffer = []

    def isatty(self):
        return False

    def close(self):
        pass

    def flush(self):
        pass

    def seek(self, n, mode: int = 0):
        pass

    def readline(self):
        if len(self._buffer) == 0:
            return ""
        ret = self._buffer[0]
        del self._buffer[0]
        return ret

    def reset(self) -> str:
        val = "".join(self._buffer)
        del self._buffer[:]
        return val

    def _write(self, x: str) -> None:
        if isinstance(x, bytes):
            x = x.decode("utf-8", "replace")
        self._buffer.append(x)

    def write(self, x: str) -> None:
        self._write(escape(x))

    def writelines(self, x):
        self._write(escape("".join(x)))


class ThreadedStream:
    """Thread-local wrapper for sys.stdout for the interactive console."""

    @staticmethod
    def push() -> None:
        if not isinstance(sys.stdout, ThreadedStream):
            sys.stdout = ThreadedStream()  # type: ignore
        _local.stream = HTMLStringO()

    @staticmethod
    def fetch() -> str:
        try:
            stream = _local.stream
        except AttributeError:
            return ""
        return stream.reset()

    @staticmethod
    def displayhook(obj):
        try:
            stream = _local.stream
        except AttributeError:
            return _displayhook(obj)
        # stream._write bypasses escaping as debug_repr is
        # already generating HTML for us.
        if obj is not None:
            _local._current_ipy.locals["_"] = obj
            stream._write(debug_repr(obj))

    def __setattr__(self, name, value):
        raise AttributeError(f"read only attribute {name}")

    def __dir__(self):
        return dir(sys.__stdout__)

    def __getattribute__(self, name: str) -> Union[Callable, List[str]]:
        if name == "__members__":
            return dir(sys.__stdout__)
        try:
            stream = _local.stream
        except AttributeError:
            stream = sys.__stdout__
        return getattr(stream, name)

    def __repr__(self):
        return repr(sys.__stdout__)


# add the threaded stream as display hook
_displayhook = sys.displayhook
sys.displayhook = ThreadedStream.displayhook


class _ConsoleLoader:
    def __init__(self) -> None:
        self._storage: Dict[Hashable, Any] = {}

    def register(self, code, source):
        self._storage[id(code)] = source
        # register code objects of wrapped functions too.
        for var in code.co_consts:
            if isinstance(var, CodeType):
                self._storage[id(var)] = source

    def get_source_by_code(self, code):
        try:
            return self._storage[id(code)]
        except KeyError:
            pass


def _wrap_compiler(console: "_InteractiveConsole") -> None:
    compile = console.compile  # type: ignore

    def func(source, filename, symbol):
        code = compile(source, filename, symbol)
        console.loader.register(code, source)
        return code

    console.compile = func  # type: ignore


class _InteractiveConsole(code.InteractiveInterpreter):
    globals: Any
    more: Any
    buffer: Any

    def __init__(self, globals: Dict[Any, Any], locals: Dict[Any, Any]) -> None:
        _locals = dict(globals)
        _locals.update(locals)
        locals = _locals
        locals["dump"] = dump
        locals["help"] = helper
        locals["__loader__"] = self.loader = _ConsoleLoader()
        code.InteractiveInterpreter.__init__(self, locals)
        self.more = False
        self.buffer = []
        _wrap_compiler(self)

    def runsource(self, source: str, **kwargs: Any) -> str:  # type: ignore
        source = f"{source.rstrip()}\n"
        ThreadedStream.push()
        prompt = "... " if self.more else ">>> "
        try:
            source_to_eval = "".join(self.buffer + [source])
            if code.InteractiveInterpreter.runsource(
                self, source_to_eval, "<debugger>", "single"
            ):
                self.more = True
                self.buffer.append(source)
            else:
                self.more = False
                del self.buffer[:]
        finally:
            output = ThreadedStream.fetch()
        return prompt + escape(source) + output

    def runcode(self, code):
        try:
            exec(code, self.locals)
        except Exception:
            self.showtraceback()

    def showtraceback(self):
        from .tbtools import get_current_traceback

        tb = get_current_traceback(skip=1)
        sys.stdout._write(tb.render_summary())

    def showsyntaxerror(self, filename: Optional[Any] = None):
        from .tbtools import get_current_traceback

        tb = get_current_traceback(skip=4)
        sys.stdout._write(tb.render_summary())  # type: ignore

    def write(self, data):
        sys.stdout.write(data)


class Console:
    """An interactive console."""

    def __init__(
        self, globals: Optional[Any] = None, locals: Optional[Any] = None
    ) -> None:
        if locals is None:
            locals = {}
        if globals is None:
            globals = {}
        self._ipy = _InteractiveConsole(globals, locals)

    def eval(self, code):
        _local._current_ipy = self._ipy
        old_sys_stdout = sys.stdout
        try:
            return self._ipy.runsource(code)
        finally:
            sys.stdout = old_sys_stdout
