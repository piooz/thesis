import logging
from typing import BinaryIO

import csv
import codecs

def read_column_binary(file: BinaryIO, have_header: bool, col: int):
    csv_reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
    data = []
    if have_header:
        next(csv_reader)

    for row in csv_reader:
        logging.debug(row)
        if col < len(row):
            data.append(float(row[col]))
        else:
            logging.warning(f'Row {row} does not have column {col}. Skipping.')

    return data
