Track when department specialty is changed to ICU for COVID.

Data files are gzipped daily extracts with 3 tab-delimited columns:
Department ID, Department Name, Department Specialty

Maintain a current csv file with the first date that a 
department was considered an ICU and the most recent date
that a department was considered an ICU.
Track whether department is not ICU, currently ICU, or not active.

An initial version of the text file is required with 5 columns and no data:
Department ID, Department Name, Department Specialty, ICU Status, First ICU Date, Last ICU Date

icu_daily_wrapper.py can be used to generate an inital run over many dates.
icu_daily.py is then meant to be run daily.