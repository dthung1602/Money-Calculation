#!/usr/bin/env python

import webapp2
from config import app_config
from routes import route_list

app = webapp2.WSGIApplication(
    route_list,
    config=app_config,
    debug=app_config.get("debug", False)
)
