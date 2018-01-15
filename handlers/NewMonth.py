from datetime import datetime

from BaseHandler import *
from models.Month import Month
from models.Person import Person


class NewMonthHandler(Handler):
    """Handle request for creating new month"""

    PAGE_TITLE = "New month"

    def render_new_month(self, **kwargs):
        # new month info
        now = datetime.now()
        month = now.strftime("%B %Y")
        start_date = now.strftime("%d/%m/%y")
        people = Person.get_all()

        # prev month
        prev_month = Month.get_current_month()
        if prev_month and not prev_month.time_end:
            # convert people key to name
            prev_month.time_to_end = now
            prev_month.people_name = []
            for person_key in prev_month.people:
                for person in people:
                    if person.key == person_key:
                        prev_month.people_name.append(person.name)
            prev_month.people_name = ", ".join(prev_month.people_name)

        # render html
        self.render("newmonth.html", month=month, start_date=start_date, page_title=self.PAGE_TITLE,
                    people=people, prev_month=prev_month, **kwargs)

    def get(self):
        self.render_new_month()

    def post(self):
        """Handle end month and create new month"""

        action = self.request.get("action")

        # create new month
        if action == "NEW MONTH":
            try:
                # get & validate info in request
                people_key_strings = self.request.get_all("people")
                if len(people_key_strings) == 0:
                    raise ValueError("There must be at least one person in a month.")
                month = Month.new_month(people_key_strings)
            except ValueError as error:
                self.render_new_month(error=error.message)
            else:
                self.redirect("/month/" + month.key.urlsafe())

        # just end month
        elif action == "END MONTH":
            month = Month.end_month()
            if month:
                self.redirect("/month/" + month.key.urlsafe())

        # invalid action
        else:
            self.render_new_month(error="Invalid action")
