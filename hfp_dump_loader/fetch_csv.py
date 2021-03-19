"""
Fetch, filter and save CSV data from the storage.
"""

import sys
import csv
import pytz
import requests
import xmltodict
from datetime import datetime

def milliseconds_to_timestamp(x):
    """Convert Unix milliseconds `x` into an UTC timestamp value."""
    return datetime.fromtimestamp(x / 1000.0, tz=pytz.utc)

def milliseconds_to_date(x):
    """Convert Unix seconds `x` into a date value."""
    # NOTE: We have to check the results for oday validity,
    #       there may be a caveat with UTC / Europe/Helsinki tz...
    return datetime.fromtimestamp(x / 1000.0, tz=pytz.utc).date()

# Available type cast names for config.yml and their respective functions.
TYPE_CASTS = {
    'int': int,
    'float': float,
    'timestamp': milliseconds_to_timestamp,
    'date': milliseconds_to_date
}

def get_csv_chunk(req_iterator, chunk_size):
    """Fetch max `chunk_size` rows from a `requests.get(..., stream=True).iter_lines()` iterator."""
    assert chunk_size >= 1, 'chunk_size must be at least 1'
    rows = []
    for i in range(chunk_size):
        next_row = next(req_iterator)
        if next_row:
            rows.append(next_row)
        else:
            break
    return rows

def split_fields(str_rows, expected_n_fields):
    """Make list of comma-separated string rows into list of lists,
    drop rows that do not have `expected_n_fields` elements."""
    rows = [el.split(',') for el in str_rows]
    rows = [el for el in rows if len(el) == expected_n_fields]
    return rows
