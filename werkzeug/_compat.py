import sys
try:
    import builtins
except ImportError:
    import __builtin__ as builtins


PY2 = sys.version_info[0] == 2

_identity = lambda x: x

if PY2:
    unichr = unichr
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)

    iterkeys = lambda d, *args, **kwargs: d.iterkeys(*args, **kwargs)
    itervalues = lambda d, *args, **kwargs: d.itervalues(*args, **kwargs)
    iteritems = lambda d, *args, **kwargs: d.iteritems(*args, **kwargs)

    iterlists = lambda d, *args, **kwargs: d.iterlists(*args, **kwargs)
    iterlistvalues = lambda d, *args, **kwargs: d.iterlistvalues(*args, **kwargs)

    def int2byte(i):
        return chr(i)

    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')

    def implements_iterator(cls):
        cls.next = cls.__next__
        del cls.__next__
        return cls

    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls

    def implements_bool(cls):
        cls.__nonzero__ = cls.__bool__
        del cls.__bool__
        return cls

    from itertools import imap, izip, ifilter
    xrange = xrange

    from StringIO import StringIO, StringIO as BytesIO
    NativeStringIO = BytesIO
else:
    unichr = chr
    text_type = str
    string_types = (str, )
    integer_types = (int, )

    iterkeys = lambda d, *args, **kwargs: iter(d.keys(*args, **kwargs))
    itervalues = lambda d, *args, **kwargs: iter(d.values(*args, **kwargs))
    iteritems = lambda d, *args, **kwargs: iter(d.items(*args, **kwargs))

    iterlists = lambda d, *args, **kwargs: iter(d.lists(*args, **kwargs))
    iterlistvalues = lambda d, *args, **kwargs: iter(d.listvalues(*args, **kwargs))

    def int2byte(i):
        return bytes((i, ))

    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

    implements_iterator = _identity
    implements_to_string = _identity
    implements_bool = _identity
    imap = map
    izip = zip
    ifilter = filter
    xrange = range

    from io import StringIO, BytesIO
    NativeStringIO = StringIO


def to_unicode(x, charset):
    '''please use carefully'''
    if x is None:
        return None
    if not isinstance(x, bytes):
        return str(x)
    return x.decode(charset)


def to_bytes(x, charset):
    '''please use carefully'''
    if x is None:
        return None
    if PY2:
        if isinstance(x, unicode):
            return x.encode(charset)
        return str(x)
    else:
        if not isinstance(x, bytes):
            x = str(x).encode(charset)
        return x


def to_native(x, charset=sys.getdefaultencoding()):
    '''please use carefully'''
    if x is None or isinstance(x, str):
        return x
    if PY2:
        return x.encode(charset)
    else:
        return x.decode(charset)


def string_join(iterable, default=''):
    '''concatenate any string type'''
    l = list(iterable)
    if l:
        if isinstance(l[0], bytes):
            return b''.join(l)
        return u''.join(l)
    return default

def iter_bytes_as_bytes(iterable):
    '''
    list(iter_bytes_as_bytes(b'abc')) -> [b'a', b'b', b'c']
    '''
    return ((int2byte(x) if isinstance(x, int) else x) for x in iterable)
