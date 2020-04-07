"""
Gzip a file.
For example,
    python gzip.file input_file.txt
will gzip input_file.txt to input_file.txt.gz
"""

import gzip, sys

def convert_to_gzip(input_filename, output_filename, input_encoding = 'utf-8', output_encoding = 'utf-8'):
    """
    given an input text file
    gzip it
    """
    with open(input_filename, 'rt', encoding = input_encoding) as f_in, gzip.open(output_filename, 'wt', encoding = output_encoding) as f_out:
        f_out.writelines(f_in)
    return None

convert_to_gzip(sys.argv[1], sys.argv[1] + '.gz')
