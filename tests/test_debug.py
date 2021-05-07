import io
import re
import sys

import pytest

from werkzeug.debug import console
from werkzeug.debug import DebuggedApplication
from werkzeug.debug import get_machine_id
from werkzeug.debug.console import HTMLStringO
from werkzeug.debug.repr import debug_repr
from werkzeug.debug.repr import DebugReprGenerator
from werkzeug.debug.repr import dump
from werkzeug.debug.repr import helper
from werkzeug.debug.tbtools import Traceback
from werkzeug.test import Client
from werkzeug.wrappers import Request


class TestDebugRepr:
    def test_basic_repr(self):
        assert debug_repr([]) == "[]"
        assert debug_repr([1, 2]) == (
            '[<span class="number">1</span>, <span class="number">2</span>]'
        )
        assert debug_repr([1, "test"]) == (
            '[<span class="number">1</span>,'
            ' <span class="string">&#x27;test&#x27;</span>]'
        )
        assert debug_repr([None]) == '[<span class="object">None</span>]'

    def test_string_repr(self):
        assert debug_repr("") == '<span class="string">&#x27;&#x27;</span>'
        assert debug_repr("foo") == '<span class="string">&#x27;foo&#x27;</span>'
        assert debug_repr("s" * 80) == (
            f'<span class="string">&#x27;{"s" * 69}'
            f'<span class="extended">{"s" * 11}&#x27;</span></span>'
        )
        assert debug_repr("<" * 80) == (
            f'<span class="string">&#x27;{"&lt;" * 69}'
            f'<span class="extended">{"&lt;" * 11}&#x27;</span></span>'
        )

    def test_string_subclass_repr(self):
        class Test(str):
            pass

        assert debug_repr(Test("foo")) == (
            '<span class="module">test_debug.</span>'
            'Test(<span class="string">&#x27;foo&#x27;</span>)'
        )

    def test_sequence_repr(self):
        assert debug_repr(list(range(20))) == (
            '[<span class="number">0</span>, <span class="number">1</span>, '
            '<span class="number">2</span>, <span class="number">3</span>, '
            '<span class="number">4</span>, <span class="number">5</span>, '
            '<span class="number">6</span>, <span class="number">7</span>, '
            '<span class="extended"><span class="number">8</span>, '
            '<span class="number">9</span>, <span class="number">10</span>, '
            '<span class="number">11</span>, <span class="number">12</span>, '
            '<span class="number">13</span>, <span class="number">14</span>, '
            '<span class="number">15</span>, <span class="number">16</span>, '
            '<span class="number">17</span>, <span class="number">18</span>, '
            '<span class="number">19</span></span>]'
        )

    def test_mapping_repr(self):
        assert debug_repr({}) == "{}"
        assert debug_repr({"foo": 42}) == (
            '{<span class="pair"><span class="key"><span class="string">&#x27;foo&#x27;'
            '</span></span>: <span class="value"><span class="number">42'
            "</span></span></span>}"
        )
        assert debug_repr(dict(zip(range(10), [None] * 10))) == (
            '{<span class="pair"><span class="key"><span class="number">0'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="pair"><span class="key"><span class="number">1'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="pair"><span class="key"><span class="number">2'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="pair"><span class="key"><span class="number">3'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="extended">'
            '<span class="pair"><span class="key"><span class="number">4'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="pair"><span class="key"><span class="number">5'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="pair"><span class="key"><span class="number">6'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="pair"><span class="key"><span class="number">7'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="pair"><span class="key"><span class="number">8'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span>, "
            '<span class="pair"><span class="key"><span class="number">9'
            '</span></span>: <span class="value"><span class="object">None'
            "</span></span></span></span>}"
        )
        assert debug_repr((1, "zwei", "drei")) == (
            '(<span class="number">1</span>, <span class="string">&#x27;'
            'zwei&#x27;</span>, <span class="string">&#x27;drei&#x27;</span>)'
        )

    def test_custom_repr(self):
        class Foo:
            def __repr__(self):
                return "<Foo 42>"

        assert debug_repr(Foo()) == '<span class="object">&lt;Foo 42&gt;</span>'

    def test_list_subclass_repr(self):
        class MyList(list):
            pass

        assert debug_repr(MyList([1, 2])) == (
            '<span class="module">test_debug.</span>MyList(['
            '<span class="number">1</span>, <span class="number">2</span>])'
        )

    def test_regex_repr(self):
        assert (
            debug_repr(re.compile(r"foo\d"))
            == "re.compile(<span class=\"string regex\">r'foo\\d'</span>)"
        )
        # No ur'' in Py3
        # https://bugs.python.org/issue15096
        assert debug_repr(re.compile("foo\\d")) == (
            "re.compile(<span class=\"string regex\">r'foo\\d'</span>)"
        )

    def test_set_repr(self):
        assert (
            debug_repr(frozenset("x"))
            == 'frozenset([<span class="string">&#x27;x&#x27;</span>])'
        )
        assert debug_repr(set("x")) == (
            'set([<span class="string">&#x27;x&#x27;</span>])'
        )

    def test_recursive_repr(self):
        a = [1]
        a.append(a)
        assert debug_repr(a) == '[<span class="number">1</span>, [...]]'

    def test_broken_repr(self):
        class Foo:
            def __repr__(self):
                raise Exception("broken!")

        assert debug_repr(Foo()) == (
            '<span class="brokenrepr">&lt;broken repr (Exception: '
            "broken!)&gt;</span>"
        )


class Foo:
    x = 42
    y = 23

    def __init__(self):
        self.z = 15


class TestDebugHelpers:
    def test_object_dumping(self):
        drg = DebugReprGenerator()
        out = drg.dump_object(Foo())
        assert re.search("Details for test_debug.Foo object at", out)
        assert re.search('<th>x.*<span class="number">42</span>', out, flags=re.DOTALL)
        assert re.search('<th>y.*<span class="number">23</span>', out, flags=re.DOTALL)
        assert re.search('<th>z.*<span class="number">15</span>', out, flags=re.DOTALL)

        out = drg.dump_object({"x": 42, "y": 23})
        assert re.search("Contents of", out)
        assert re.search('<th>x.*<span class="number">42</span>', out, flags=re.DOTALL)
        assert re.search('<th>y.*<span class="number">23</span>', out, flags=re.DOTALL)

        out = drg.dump_object({"x": 42, "y": 23, 23: 11})
        assert not re.search("Contents of", out)

        out = drg.dump_locals({"x": 42, "y": 23})
        assert re.search("Local variables in frame", out)
        assert re.search('<th>x.*<span class="number">42</span>', out, flags=re.DOTALL)
        assert re.search('<th>y.*<span class="number">23</span>', out, flags=re.DOTALL)

    def test_debug_dump(self):
        old = sys.stdout
        sys.stdout = HTMLStringO()
        try:
            dump([1, 2, 3])
            x = sys.stdout.reset()
            dump()
            y = sys.stdout.reset()
        finally:
            sys.stdout = old

        assert "Details for list object at" in x
        assert '<span class="number">1</span>' in x
        assert "Local variables in frame" in y
        assert "<th>x" in y
        assert "<th>old" in y

    def test_debug_help(self):
        old = sys.stdout
        sys.stdout = HTMLStringO()
        try:
            helper([1, 2, 3])
            x = sys.stdout.reset()
        finally:
            sys.stdout = old

        assert "Help on list object" in x
        assert "__delitem__" in x

    def test_exc_divider_found_on_chained_exception(self):
        @Request.application
        def app(request):
            def do_something():
                raise ValueError("inner")

            try:
                do_something()
            except ValueError:
                raise KeyError("outer")

        debugged = DebuggedApplication(app)
        client = Client(debugged)
        response = client.get("/")
        data = response.get_data(as_text=True)
        assert 'raise ValueError("inner")' in data
        assert '<div class="exc-divider">' in data
        assert 'raise KeyError("outer")' in data


class TestTraceback:
    def test_log(self):
        try:
            1 / 0
        except ZeroDivisionError:
            traceback = Traceback(*sys.exc_info())

        buffer_ = io.StringIO()
        traceback.log(buffer_)
        assert buffer_.getvalue().strip() == traceback.plaintext.strip()

    def test_filename_encoding(self, tmpdir, monkeypatch):
        moduledir = tmpdir.mkdir("föö")
        moduledir.join("bar.py").write("def foo():\n    1/0\n")
        monkeypatch.syspath_prepend(str(moduledir))

        import bar  # type: ignore

        try:
            bar.foo()
        except ZeroDivisionError:
            traceback = Traceback(*sys.exc_info())

        assert "föö" in "\n".join(frame.render() for frame in traceback.frames)


def test_get_machine_id():
    rv = get_machine_id()
    assert isinstance(rv, bytes)


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.parametrize("crash", (True, False))
def test_basic(dev_server, crash):
    c = dev_server(use_debugger=True)
    r = c.request("/crash" if crash else "")
    assert r.status == (500 if crash else 200)

    if crash:
        assert b"The debugger caught an exception in your WSGI application" in r.data
    else:
        assert r.json["PATH_INFO"] == "/"


def test_console_closure_variables(monkeypatch):
    # restore the original display hook
    monkeypatch.setattr(sys, "displayhook", console._displayhook)
    c = console.Console()
    c.eval("y = 5")
    c.eval("x = lambda: y")
    ret = c.eval("x()")
    assert ret == ">>> x()\n5\n"


@pytest.mark.timeout(2)
def test_chained_exception_cycle():
    try:
        try:
            raise ValueError()
        except ValueError:
            raise TypeError()
    except TypeError as e:
        # create a cycle and make it available outside the except block
        e.__context__.__context__ = error = e

    # if cycles aren't broken, this will time out
    tb = Traceback(TypeError, error, error.__traceback__)
    assert len(tb.groups) == 2


def test_non_hashable_exception():
    class MutableException(ValueError):
        __hash__ = None

    try:
        raise MutableException()
    except MutableException:
        # previously crashed: `TypeError: unhashable type 'MutableException'`
        Traceback(*sys.exc_info())
