# -*- coding: utf-8 -*-
"""
Module with functions for handling dates in buildmon
"""
from datetime import datetime, timedelta

def generate_datestrings(date2 = datetime.now()):
    """
    returns today's date and yesterday's date
    as strings formatted %YYYYMMDD
    if date2 is supplied, must be in datetime format
    """
    date1 = date2 - timedelta(days = 1)
    return (date1.strftime('%Y%m%d'), date2.strftime('%Y%m%d'))

def add_days_to_string(date2, days, date_format = '%Y%m%d'):
    """
    given a string represeting a date, number of days to add (could be negative),
    and date_format
    return datestring shifted over by number of days
    """
    datetime_object = datetime.strptime(date2, date_format) + timedelta(days = days)
    return datetime_object.strftime(date_format)

def make_datelist(startdate, enddate, date_format = '%Y%m%d'):
    """
    given strings representing start and end dates
    output list of all dates from start to end including endpoints
    """
    try:
        date1 = datetime.strptime(startdate, date_format)
        date2 = datetime.strptime(enddate, date_format)
    except:
        print("start or end date could not be converted to date")
        raise
    assert date1 <= date2, "start date is after end date."
    currentdate = startdate
    datelist = [currentdate]
    while(currentdate != enddate):
       currentdate = add_days_to_string(currentdate, 1, date_format = date_format)
       datelist.append(currentdate)
    return datelist
