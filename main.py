#!/usr/bin/env python

import webapp2

from config import app_config
from handlers.Error import error_handlers
from routes import route_list

app = webapp2.WSGIApplication(
    routes=route_list,
    config=app_config,
    debug=app_config.get("debug", False),
)

app.error_handlers.update(error_handlers)
