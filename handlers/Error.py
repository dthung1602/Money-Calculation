#
#  Contains handlers for common errors like 4xx, 5xx
#

import os
import sys
import traceback

import jinja2

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

error_4xx_names = {
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict"
}

error_5xx_names = {
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported"
}


def write(response, template_name, **kwargs):
    t = jinja_env.get_template(template_name)
    response.out.write(t.render(**kwargs))


def handler_4xx(code):
    """Create handlers for 4xx errors"""

    def handler(request, response, exception):
        write(response, "4xx.html", code=code, error_name=error_4xx_names[code])
        response.set_status(code)

    return handler


def handler_5xx(code):
    """Create handlers for 5xx errors"""

    def handler(request, response, exception):
        # response
        write(response, "5xx.html", code=code, error_name=error_5xx_names[code])
        response.set_status(code)

        # logging for debug
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=7, file=sys.stderr)

    return handler


# create list of error handlers to be used in main.py
error_handlers = {i: handler_4xx(i) for i in error_4xx_names}
error_handlers.update({i: handler_5xx(i) for i in error_5xx_names})
