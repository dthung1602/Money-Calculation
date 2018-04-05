import webapp2

from Error import jinja_env, error_4xx_names, error_5xx_names
from config import app_config


class Handler(webapp2.RequestHandler):
    """
        Base class for all Request handler
        Provides basic functions
    """

    def error(self, code):
        """Render error pages"""
        self.response.status = code
        if code in error_4xx_names:
            self.render("4xx.html", code=code, error_name=error_4xx_names[code])
        elif code in error_4xx_names:
            self.render("5xx.html", code=code, error_name=error_5xx_names[code])
        else:
            self.render("unknown_error.html")

    def write(self, *args, **kwargs):
        """
            Write to response
            Add a ---- line for debugging
        """
        self.response.out.write(*args, **kwargs)
        print "-----------------------------------------------------\n\n"

    @staticmethod
    def render_str(template, **kwargs):
        """Use jinja2 to render html to string"""
        kwargs['version'] = app_config["version"]
        return jinja_env.get_template(template).render(**kwargs)

    def render(self, template, **kwargs):
        """Render html to response"""
        self.write(self.render_str(template, **kwargs))
