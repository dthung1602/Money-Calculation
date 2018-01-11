class Monthly(Hl):
    """Handle request for a particular month"""

    def get(self, month_id):
        """Get month info and render html"""
        month = Month.get_by_id(int(month_id))
        if month is None:
            self.error(404)
        else:
            self.render_current_month(month)

    def post(self, month_id):
        """Handle 2 actions: add new Good & end current month"""
        month = Month.get_by_id(int(month_id))
        if month is None:  # invalid month id
            self.error(404)
        else:
            if self.request.get("action") == "Add":
                self.add_good(month)
            else:
                self.end_month(month)

    def render_current_month(self, month, error=[]):
        """Render money_current_month.html"""
        buyers = list(Buyer.get_all_buyers())

        # calculate and put attributes to buyer objects
        usage = {}
        for u in MoneyUsage.get_usage_in_month(month):
            usage[u.buyer_id] = u

        for buyer in buyers:
            u = usage[buyer.key().id()]
            buyer.money = u.money_spend
            buyer.last_month_left = u.last_month_left
            buyer.charge = u.money_to_pay
            buyer.roundup = u.roundup
            buyer.next_month_left = u.next_month_left

        self.render("money_current_month.html", month=month, buyers=buyers, error=error, round_float=round_float,
                    __page_title__=month.to_string_short())

    def add_good(self, month):
        """add a good to database"""
        # get info
        month_id = month.key().id()
        price = self.request.get("price")
        what = self.request.get("what")
        buyer = self.request.get("buyer")

        # validate
        error = []
        # check for empty fields
        if None in [price, what, buyer]:
            error.append("Please fill all information")
        # check if buyer exists
        try:
            buyer = int(buyer)
            if Buyer.get_by_id(buyer) is None:
                raise ValueError
        except ValueError:
            error.append("Invalid buyer")
        # evaluate price
        try:
            if not re.match("^[0-9 \-+*/()]+$", price):
                raise SyntaxError
            price = eval(price)
            if price <= 0 or not isinstance(price, int):
                raise ValueError
        except (SyntaxError, ZeroDivisionError):
            error.append("Invalid arithmetic expression in field price")
        except ValueError:
            error.append("Price must be a positive integer")

        if len(error) > 0:
            self.render_current_month(month, error)
            return

        # put to database
        good = Good(month_id=month_id, price=price, what=what, buyer=buyer)
        good.put()
        sleep(0.5)
        MoneyUsage.update(good)
        month.update()
        self.render_current_month(month)

    def end_month(self, old_month):
        """
            add time_end to old month, making its data can not be change;
            create a new month
        """
        # check if old_month has already ended
        if old_month.time_end is not None:
            self.render_current_month(old_month, ["This month has already ended."])
            return

        # create new month
        new_month = Month.new_month(old_month)

        # end old month
        old_month.time_end = datetime.now()
        old_month.next_month = new_month.key().id()
        old_month.put()

        sleep(0.8)
        self.render_current_month(old_month)
