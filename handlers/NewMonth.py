from datetime import datetime

from BaseHandler import *
from models.Month import Month
from models.Person import Person


class NewMonthHandler(Handler):
    """Handle request for creating new month"""

    def render_new_month(self, **kwargs):
        now = datetime.now()
        month = now.strftime("%B %Y")
        start_date = now.strftime("%d/%m/%y")
        self.render("newmonth.html", month=month, start_date=start_date, people=Person.get_all(), **kwargs)

    def get(self):
        self.render_new_month()

    def post(self):
        """Create new month"""
        try:
            month = Month.new_month(self.request)
        except ValueError as error:
            self.render_new_month(error=error.message)
        else:
            self.redirect("/moneyM1522/" + month.key.urlsafe())
