from BaseHandler import *
from models.Month import Month


class HomeHandler(Handler):
    """Handle home page"""

    PAGE_TITLE = "Monthly money calculation"

    def get(self, *args):
        """Render home page"""
        if args[0] is None:
            self.redirect("/home")
        else:
            self.render("home.html", months=Month.get_all(), page_title=self.PAGE_TITLE)
