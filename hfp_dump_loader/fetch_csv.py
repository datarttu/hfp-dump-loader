"""
Fetch, filter and save CSV data from the storage.
"""

import sys
import csv
import requests
import xmltodict
from .utils import TYPE_CASTS
from .utils import cast_failing_to_none

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

def transpose_to_cols_dict(list_rows, field_mapping):
    """Transpose `list_rows` into list of columns, select and name the columns
    by `field_mapping`."""
    list_cols = list(map(list, zip(*list_rows)))

    idx_name_pairs = []
    for k, v in field_mapping.items():
        if isinstance(v, dict):
            idx_name_pairs.append((k, v['name']))
        else:
            idx_name_pairs.append((k, v))

    cols = {v: list_cols[k] for k, v in idx_name_pairs}
    return cols

def cast_col_types(cols_dict, field_mapping):
    """Return `cols_dict` with column data types changed according to `field_mapping`.
    If no type cast is defined, the column is left as string."""
    to_cast = {v['name']: TYPE_CASTS[v['type']] for k, v in field_mapping.items() if isinstance(v, dict)}
    for name, func in to_cast.items():
        cols_dict[name] = [cast_failing_to_none(el, func) for el in cols_dict[name]]
    return cols_dict

def transpose_to_dict_rows(cols_dict):
    """Return `cols_dict` as list of dict rows."""
    return [dict(zip(cols_dict.keys(), row)) for row in zip(*cols_dict.values())]

def split_rows_for_files(dict_rows, csvname_template):
    """Distribute rows into lists by output filename created with `csvname_template`.
    The template should contain field names present in `dict_rows` prefixed with `$`.

    ..note: Any whitespace in filenames will be replaced with `_`."""
    distributed = {}
    for row in dict_rows:
        fname = csvname_template.format(**row).replace(' ', '_').replace('"', '')
        if fname in distributed.keys():
            distributed[fname].append(row)
        else:
            distributed[fname] = [row]
    return distributed
