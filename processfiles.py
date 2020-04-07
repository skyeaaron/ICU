"""
Module with functions for reading and writing files
needed for ICU department tracking
"""

import gzip
import csv

def preview_zipped_file(filename1, lines = 4, mode = 'rt', encoding = 'utf-8'):
    """
    prints first 4 lines of gz zipped file, parsed using csv reader
    """
    with gzip.open(filename1, mode = mode, encoding = encoding) as fn1:
        f1 = csv.reader(fn1, delimiter = '\t', quoting=csv.QUOTE_NONE)
        for i in range(lines):
            print(next(f1))
    return None

def gzip_to_list(filename1, header = True, delimiter = '\t', mode = 'rt', encoding = 'utf-8'):
    """
    import gz zipped file as list of lists of strings using csv reader
    if header is True then returns first row as header
    delimiter defaults to ","
    """
    with gzip.open(filename1, mode = mode, encoding = encoding) as fn1:
        csv_f = csv.reader(fn1, delimiter = delimiter, quoting=csv.QUOTE_NONE)
        if header:
            output_header = next(csv_f)
            output_data = [row for row in csv_f]
            return output_data, output_header
        else:
            output_header = None
            output_data = [row for row in csv_f]
            return output_data


def csv_to_list(filename, header = True, delimiter = ",", encoding = 'utf-8', quoting = csv.QUOTE_MINIMAL):
    """
    read csv file
    if header is True then returns first row as header
    delimiter defaults to ","
    """
    with open(filename, 'r', encoding = encoding) as f:
        csv_f = csv.reader(f, delimiter = delimiter, quoting = quoting)
        if header:
            output_header = next(csv_f)
            output_data = [row for row in csv_f]
            return output_data, output_header
        else:
            output_header = None
            output_data = [row for row in csv_f]
            return output_data

def write_list_to_csv(filename, output, delimiter = ',', encoding = 'utf-8'):
    """
    Save output list to csv
    """
    with open(filename, 'w+', encoding = encoding) as f:
        csv_f = csv.writer(f, delimiter = delimiter, lineterminator = '\n')
        for row in output:
            csv_f.writerow(row)
    return None
