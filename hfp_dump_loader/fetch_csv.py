"""
Fetch, filter and save CSV data from the storage.
"""

import sys
import csv
import requests
import xmltodict
from datetime import datetime

def get_csv_chunk(req_iterator, chunk_size):
    """Fetch max `chunk_size` rows from a `requests.get(..., stream=True).iter_lines()` iterator."""
    assert chunk_size >= 1, 'chunk_size must be at least 1'
    rows = []
    for i in range(chunk_size-1):
        next_row = next(req_iterator)
        if next_row:
            rows.append(next_row)
        else:
            break
    return rows
