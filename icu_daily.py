"""
Determine which departments have been changed to ICU
since yesterday.

One optional command line argument is date. If not supplied,
uses today's date.
python icu_daily.py YYYYMMDD

This script looks for a current icu status file
in the SampleOutputs called icu_dept_status.txt.
It also looks for a build monitoring department file in the SampleInputs folder
with the specified date called dep_YYYYMMDD.txt.gz.
If both files are found, it will overwrite the icu status file
based on the department data in the buildmon dept file.
"""
import datefunctions as df
import processfiles as pf
from Department import Department
import sys

def get_date(argv):
    """
    A date can be supplied as a command line arg. 
    (Should be in form YYYYMMDD.)
    Otherwise return today's date.
    Note that argv = sys.argv[1:]
    """
    if len(argv) < 1:
        date1, date2 = df.generate_datestrings()
    else:
        date2 = argv[0]
    return date2

def import_status_file(icu_status_file):
    """
    Read output from yesterday.
    This file should be a utf-8 csv file with the following header:
    DepartmentID,DepartmentNM,DepartmentSpecialtyDSC,ICU,FirstICUDate,LastICUDate
    """
    try:
        yest_output, yest_header = pf.csv_to_list(icu_status_file, header = True, delimiter = ',')
    except FileNotFoundError:
        sys.exit('Prior ICU dept status file not found at: ' + icu_status_file)
    return yest_output, yest_header

def create_yest_dict(yest_output):
    """
    given a list of lists with current icd status data
    output dictionary of Department objects
    """
    yest_dict = {}
    for row in yest_output:
        yest_dict[row[0]] = Department(ID=row[0], name=row[1], specialty=row[2],
                                       icu=row[3], first=row[4], last=row[5])
    return yest_dict

def import_dept_file(dept_file):
    """
    Read in departments from today
    """
    try:
        today_dept, today_header = pf.gzip_to_list(dept_file, header = True)
    except FileNotFoundError:
        sys.exit('Dept buildmon file not found at: ' + dept_file)
    return today_dept, today_header

def create_today_dict(today_dept, yest_dict, icu_specialties, date2):
    """
    create a dictionary of departments from today_dept list of lists
    yest_dict contains dictionary of Departments from previous icu status file
    icu_specialties is a list of specialties considered icu
    date2 is today's date, used to update first and last icu dates
    """
    today_dict = {}
    for row in today_dept:
        #if the dept specialty is an icu specialty
        if row[2] in icu_specialties:
            #if dept was not in yesterday's dictionary, create new Department
            if row[0] not in yest_dict:
                today_dict[row[0]] = Department(row[0], row[1], row[2], 'Yes', date2, date2)
            #else point today's entry for it at yesterday's entry and update
            else:
                today_dict[row[0]] = yest_dict[row[0]]
                today_dict[row[0]].name = row[1]
                today_dict[row[0]].specialty = row[2]
                today_dict[row[0]].icu = 'Yes'
                #populate first date if blank
                if not today_dict[row[0]].first:
                    today_dict[row[0]].first = date2
                #update last with today's date
                today_dict[row[0]].last = date2
        #if the dept specialty is not an icu specialty
        else:
            #if dept was not in yesterday's dictionary, create new Department
            if row[0] not in yest_dict:
                today_dict[row[0]] = Department(row[0], row[1], row[2], 'No', None, None)
            #else point today's entry for it at yesterday's entry and update
            else:
                today_dict[row[0]] = yest_dict[row[0]]
                today_dict[row[0]].name = row[1]
                today_dict[row[0]].specialty = row[2]
                today_dict[row[0]].icu = 'No'
    return today_dict

def add_inactive_depts(today_dict, yest_dict):
    """
    Add any depts that are in yest_dict but not in today_dict
    to today_dict with ICU status of "Inactive"
    """
    for dept in yest_dict:
        if dept not in today_dict:
            today_dict[dept] = yest_dict[dept]
            today_dict[dept].icu = 'Inactive'

def format_output_list(today_dict, yest_header):
    """
    Create a list that can be saved to csv with a header taken
    from the icu_status_file and converting today_dict into rows
    """
    today_output = [yest_header]
    today_output.extend([[today_dict[dept].ID, today_dict[dept].name,
                          today_dict[dept].specialty, today_dict[dept].icu,
                          today_dict[dept].first, today_dict[dept].last] for dept in today_dict])
    return today_output
        
def main(argv):
    #Define the list of specialties that are considered ICU
    icu_specialties = {'Cardiac Intensive Care',
                       'Intensive Care',
                       'Neurological Intensive Care',
                       'Pediatric Intensive Care',
                       'Surgical Intensive Care'}

    #get date if given in command line args, or use today's date.
    date2 = get_date(argv)
    print('Updating icu status with date:', date2)

    #filepath to output file (read and overwritten daily)
    icu_status_file = 'SampleOutputs\\icu_dept_status.txt'
    #filepath to today's department extract
    dept_file = 'SampleInputs\\dep_' + date2 + '.txt.gz'

    #import current icu status file
    yest_output, yest_header = import_status_file(icu_status_file)
    print(yest_header)

    #Save all depts from yesterday into dictionary of Department objects
    yest_dict = create_yest_dict(yest_output)
    print('Number of departments yesterday:', len(yest_dict))

    #Read in department data from today
    today_dept, today_header = import_dept_file(dept_file)
    print('Number of departments today:', len(today_dept))

    #Create dictionary of depts from today's file
    today_dict = create_today_dict(today_dept, yest_dict, icu_specialties, date2)

    #For any depts that were in yesterday's dict but not in today's,
    #add them to today's dict with ICU as 'Inactive'
    add_inactive_depts(today_dict, yest_dict)

    #Save output to a list
    today_output = format_output_list(today_dict, yest_header)

    #Save output to file
    pf.write_list_to_csv(icu_status_file, today_output)

if __name__ == '__main__':
    main(sys.argv[1:])


