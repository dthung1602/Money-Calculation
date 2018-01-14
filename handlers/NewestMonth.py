from BaseHandler import Handler
from models import Month


class NewestMonthHandler(Handler):
    def get(self):
        month = Month.get_current_month()
        if month:
            self.redirect("/month/" + month.key.urlsafe())
        else:
            self.redirect("/")
