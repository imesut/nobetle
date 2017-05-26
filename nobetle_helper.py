import time
import calendar
import datetime


def integer(string):
    """
    int() function cannot handle NoneType values. This function handle non-NoneType values.
    :param string: 
    :return: integer value of string via int() function.
    """
    if string:
        return int(string)


month_names = {1: "ocak", 2: "subat", 3: "mart", 4: "nisan", 5: "mayis", 6: "haziran", 7: "temmuz", 8: "agustos",
               9: "eylul", 10: "ekim", 11: "kasim", 12: "aralik"}
"""
Month_names dictionary is verbal expression of month number. For English website usage, month names dictionary should be
month_names = {1: "january", 2: "fabruary", 3: "march", 4: "april", 5: "may", 6: "june", 7: "july", 8: "august",
               9: "september", 10: "october", 11: "november", 12: "december"}
"""


def nobetle_time(increment):
    """
    This function generate a pack of information about next schedule period(next month)
    :param increment: the addition to current month's numeric value.
    For current period(month) increment is 0
    For next period(month) increment is 1
    :return: a dictionary item that consist period name, year, month, day number in month of period and weekend days of
    the period
    """
    today = time.localtime(time.time())
    year = today[0]
    month = today[1]+increment
    day_number_in_month = calendar.monthrange(year, month)[-1]
    weekend_days = []
    friday_days = []
    for i in range(1, day_number_in_month+1):
        nofday = datetime.datetime(year, month, i).isoweekday()
        if nofday == 5:
            friday_days.append(i)
        elif nofday > 5:
            weekend_days.append(i)
    return {"period": month_names[month]+str(year),
            "year": year,
            "month": month,
            "day_number_in_month": day_number_in_month,
            "friday_days": friday_days,
            "weekend_days": weekend_days
            }


def reverse_period(period):
    """
    This function return numerical year and month value of period string.
    :param period: any period string
    :return: a dictionary item consits of numerical year and month values.
    """
    year = period[-4:]
    month = {"ocak": 1, "subat": 2, "mart": 3, "nisan": 4, "mayis": 5, "haziran": 6,
             "temmuz": 7, "agustos": 8, "eylul": 9, "ekim": 10, "kasim": 11, "aralik": 12}[period[:-4]]
    return {"year": year, "month": month}


def periods_nextto(period):
    """
    This function take any period string and return the following period and the previous period string.
    :param period: 
    :return: previous and following period string.
    """
    month = int(reverse_period(period)["month"])
    year = int(reverse_period(period)["year"])
    np_year = year
    pp_year = year
    np_month = month + 1
    pp_month = month - 1
    if month == 12:
        np_month = 1
        np_year += 1
    elif month == 1:
        pp_month = 12
        pp_year -= 1

    return {"prev": str(month_names[pp_month])+str(pp_year), "next": str(month_names[np_month])+str(np_year)}


def none2emp(db_object):
    """
    The equivalent of None String(NoneType) at database is an empty list for schedule script.
    This function replaces None fields to empty list.
    :param db_object: Object retrieved from database.
    :return: input object as its None fields replaced with empty lists.
    """
    for i in db_object:
        for attribute in i.__dict__.keys():
            if getattr(i, attribute) == "None":
                setattr(i, attribute, [])
