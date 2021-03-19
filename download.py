from hfp_dump_loader import fetch_csv as fc
from hfp_dump_loader import configuration as cf

dataset = 'csv/VehiclePosition/2020-09-21-15.csv'

conf = cf.read_conf_for_downloading('config.yml')
storage_url = conf['storage_url']
expected_n_fields = int(conf['expected_n_fields'])
field_mapping = conf['field_mapping']
csvname_template = conf['csvname_template']
target_dir = conf['target_dir']

import requests
from datetime import datetime
import os
import csv

assert os.path.isdir(target_dir)

chunk_size = 10000

filehandlers = {}
existing_files = os.listdir(target_dir)
fieldnames = [v['name'] if isinstance(v, dict) else v for k, v in field_mapping.items()]

start_t = datetime.now()

n_fetched = 0
n_written = 0
r = requests.get(f'{storage_url}/{dataset}', stream=True)
r.encoding = 'utf-8'
req_iterator = r.iter_lines(decode_unicode=True)

tdelta = datetime.now() - start_t
print(f'+{tdelta.total_seconds()} s')
try:
    while True:
        # if n_fetched >= 10000:
        #     break
        raw_chunk = fc.get_csv_chunk(req_iterator=req_iterator, chunk_size=chunk_size)
        n_fetched += len(raw_chunk)
        if not raw_chunk:
            break

        list_chunk = fc.split_fields(str_rows=raw_chunk, expected_n_fields=expected_n_fields)
        named_cols = fc.transpose_to_cols_dict(list_rows=list_chunk, field_mapping=field_mapping)
        typed_cols = fc.cast_col_types(cols_dict=named_cols, field_mapping=field_mapping)
        typed_rows = fc.transpose_to_dict_rows(cols_dict=typed_cols)
        filtered_rows = fc.filter_rows_by_attributes(dict_rows=typed_rows, field_mapping=field_mapping)
        distributed_rows = fc.split_rows_for_files(dict_rows=filtered_rows, csvname_template=csvname_template)

        for fname, rows in distributed_rows.items():
            need_header = False
            if fname not in filehandlers.keys():
                full_fpath = os.path.join(target_dir, fname)
                open_mode = 'a'
                if fname not in existing_files:
                    need_header = True
                    open_mode = 'w'
                    existing_files.append(fname)
                filehandlers[fname] = open(full_fpath, mode=open_mode, newline='')
            writer = csv.DictWriter(filehandlers[fname], fieldnames=fieldnames)
            if need_header:
                writer.writeheader()
            writer.writerows(rows)
            n_written += len(rows)

        tdelta = datetime.now() - start_t
        print(f'+{tdelta.total_seconds()} s {n_fetched} lines fetched, {n_written} lines written to {len(filehandlers)} files', end='\r')
except:
    pass
finally:
    print()
    for fname, fh in filehandlers.items():
        fh.close()

print(datetime.now() - start_t)
