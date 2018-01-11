class HomeHandler(Hl):
    """Handle home page"""

    page_title = "Monthly money calculation"

    def get(self):
        """Render home page"""
        query = db.GqlQuery("SELECT * FROM Month ORDER BY time_begin DESC")
        months = [m for m in query]
        if len(months) == 0:
            self.render("money_home.html")
        else:
            self.render("money_home.html", months=months)

    def post(self):
        """Create first new month"""
        # check if Month is empty
        query = db.GqlQuery("SELECT * FROM Month ORDER BY time_begin DESC")
        months = [m for m in query]
        if len(months) != 0:
            self.render("money_home.html", error=["New month is created automatically when user ends current month."],
                        months=months)
            return

        # new month
        month = Month.new_month()
        self.redirect("/moneyM1522/{}".format(month.key().id()))
