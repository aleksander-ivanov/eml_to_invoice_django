import datetime as dt
import calendar
import re


def extract(file_name):
    m = re.search('Y(\d\d)M(\d\d).eml', file_name)
    year = int('20' + m.group(1))
    month = int(m.group(2))

    # Invoice day is the last day of the month
    invoice_date = dt.datetime(year, month, calendar.monthrange(year, month)[1])
    # Due day is the last day of the next month
    due_date = dt.datetime(year, month + 1, calendar.monthrange(year, month + 1)[1])

    return invoice_date, due_date
