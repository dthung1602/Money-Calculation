import os

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)
        print "-----------------------------------------------------\n\n"

    @staticmethod
    def render_str(template, **kwargs):
        return jinja_env.get_template(template).render(**kwargs)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))
