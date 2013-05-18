
from . import _urlparse as urlparse

import six
from functools import partial

def iterkeys(d, *a, **kw):
    return iter(getattr(d, six._iterkeys)(*a, **kw))

def itervalues(d, *a, **kw):
    return iter(getattr(d, six._itervalues)(*a, **kw))

def iteritems(d, *a, **kw):
    return iter(getattr(d, six._iteritems)(*a, **kw))

if six.PY3:
    _iterlists = 'lists'
    _iterlistvalues = 'listvalues'
else:
    _iterlists = 'iterlists'
    _iterlistvalues = 'iterlistvalues'

def iterlists(d, *a, **kw):
    return getattr(d, _iterlists)(*a, **kw)

def iterlistvalues(d, *a, **kw):
    return getattr(d, _iterlistvalues)(*a, **kw)

try:
    unichr = unichr # py2
except NameError:
    unichr = chr # py3
