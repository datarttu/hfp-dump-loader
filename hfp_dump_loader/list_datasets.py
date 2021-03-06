"""
List csv dataset URLs available in the storage.
"""

import sys
import csv
import requests
import xmltodict
from datetime import datetime

def get_raw_dataset_xml(storage_url, prefix, maxresults, marker=None):
    """Download max `maxresults` entries of available datasets from `hfp_storage_url` and return raw XML result.
    If `marker` string is provided, it is used to return data after NextMarker.
    For now, this is hard-coded to get VehiclePosition metadata only.
    """
    r = requests.get(storage_url, params={
                         'restype': 'container',
                         'comp': 'list',
                         'prefix': prefix,
                         'maxresults': maxresults,
                         'marker': marker
                     })
    return r.text

def pick_blob_attributes(blob):
    """Pick only necessary attributes of a file information blob into a flat dict.
    Also cast Last-Modified into datetime format and Content-Length into int."""
    # Assuming raw format like "Sat, 25 Apr 2020 15:32:19 GMT" here.
    last_modified = datetime.strptime(
        blob['Properties']['Last-Modified'],
        '%a, %d %b %Y %H:%M:%S %Z'
        )
    size_bytes = int(blob['Properties']['Content-Length'])
    return dict(
        dataset_name = blob['Name'],
        dataset_url = blob['Url'],
        last_modified = last_modified,
        size_bytes = size_bytes
    )

def make_tidy_result_set(raw_xml):
    """From raw XML result, make a dict with blob attributes list and NextMarker if it exists."""
    raw_res = xmltodict.parse(raw_xml)
    raw_res = raw_res['EnumerationResults']
    res = dict(
        blobs = list(map(pick_blob_attributes, raw_res['Blobs']['Blob'])),
        nextmarker = None
        )
    if 'NextMarker' in raw_res.keys():
        res['nextmarker'] = raw_res['NextMarker']
    return res

def sizeof_fmt(num, suffix='B'):
    """Return bytes size in human-readable format."""
    # Source: https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def human_readable_dataset_string(blob_dict):
    """Return basic metadata of a dataset blob as human-readable string."""
    human_readable_size = sizeof_fmt(int(blob_dict['size_bytes']))
    return f"{blob_dict['dataset_name']:<50} {human_readable_size:<20}"

def browse_datasets_interactively(storage_url, prefix, n):
    """End-user app for fetching and printing available dataset metadata to the console
    `n` entries at a time."""
    marker = None
    while True:
        print('Downloading...', end='\r')
        res = get_raw_dataset_xml(storage_url=storage_url, prefix=prefix, maxresults=n, marker=marker)
        res = make_tidy_result_set(res)
        printable_lines = list(map(human_readable_dataset_string, res['blobs']))
        for l in printable_lines:
            print(l)
        marker = res['nextmarker']
        if marker is None:
            break
        user_input = input('ENTER to continue, type a number for new n of lines, or type anything else to quit: ')
        if user_input != '':
            try:
                n = int(user_input)
            except ValueError:
                break

def print_datasets_as_csv(storage_url, prefix, n, until_n):
    """End-user app that prints dataset metadata as plain csv to stdout."""
    csv_fields = ['dataset_name', 'dataset_url', 'last_modified', 'size_bytes']
    writer = csv.DictWriter(sys.stdout, fieldnames=csv_fields)
    writer.writeheader()

    marker = None
    n_written = 0
    while True:
        res = get_raw_dataset_xml(storage_url=storage_url, prefix=prefix, maxresults=n, marker=marker)
        res = make_tidy_result_set(res)
        for el in res['blobs']:
            writer.writerow(el)
            n_written += 1
            if n_written >= until_n:
                break
        marker = res['nextmarker']
        if marker is None or n_written >= until_n:
            break
