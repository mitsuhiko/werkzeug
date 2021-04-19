import json
import sys
from importlib import import_module

from werkzeug.serving import generate_adhoc_ssl_context
from werkzeug.serving import run_simple
from werkzeug.serving import WSGIRequestHandler
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response


class WSGI11RequestHandler(WSGIRequestHandler):
    protocol_version = "HTTP/1.1"


name = sys.argv[1]
mod = import_module(f"{name}_app")


@Request.application
def app(request):
    if request.path == "/ensure":
        return Response()

    return Response.from_app(mod.app, request.environ)


kwargs = getattr(mod, "kwargs", {})
kwargs.update(hostname="127.0.0.1", port=5000, application=app)
kwargs.update(json.loads(sys.argv[2]))
ssl_context = kwargs.get("ssl_context")

if kwargs.get("request_handler") == "HTTP/1.1":
    kwargs["request_handler"] = WSGI11RequestHandler

if ssl_context == "custom":
    kwargs["ssl_context"] = generate_adhoc_ssl_context()
elif isinstance(ssl_context, list):
    kwargs["ssl_context"] = tuple(ssl_context)

run_simple(**kwargs)
