"""
This is a wrapper for icu_daily.py that allows the script
to be run over a range of dates.

Two required command line arguments are:
python icu_daily_wrapper.py start_date end_date

A current icu status file in the SampleOutputs folder
called icu_dept_status.txt is required.
Any missing buid monitoring department files in the date range
will be skipped.
"""
import datefunctions as df
import sys
import icu_daily

def get_dates(argv):
    """
    read the system args and return range of dates as a list
    Note that argv = sys.argv[1:]
    """
    if len(argv) < 2:
        exit("Start and end dates must be given as command line arguments in format YYYYMMDD.")
    else:
        datelist = df.make_datelist(argv[0], argv[1])
        return datelist
        
def main(argv):
    #Create list of dates
    datelist = get_dates(argv)
    print("Date list is:", datelist)

    #Run icu_daily for each date
    for date in datelist:
        print("Running icu_daily with date:", date)
        icu_daily.main([date])


if __name__ == '__main__':
    main(sys.argv[1:])


