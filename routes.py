#
#   Map urls and handlers
#
from handlers import *

route_list = [
    ("/(home)?", Home.HomeHandler),
    ("/newmonth", NewMonth.NewMonthHandler),
    ("/month/(.*)", MonthHandler.MonthHandler),
    ("/newest", NewestMonth.NewestMonthHandler)
]
