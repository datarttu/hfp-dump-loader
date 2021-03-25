**NOTE: This project is not being updated anymore, since I decided to write a more feasible solution in R.**

# List and download HFP dumps from blob storage

This tool allows you to browse [HFP](https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/) csv dumps available in Azure blob storage and download filtered versions of them.

## Setup

Python >= 3.7 is required.
We are currently using the [venv](https://docs.python.org/3/library/venv.html) package for dependency management.

```
git clone https://github.com/datarttu/hfp-dump-loader.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Make the YAML configuration file to suit your needs.
Check the example file for reference.

```
cp example-config.yml config.yml
# Modify config.yml entries manually.
```

## Usage

Remember to activate your virtual Python environment, unless you decided to install the dependencies globally.

```
source env/bin/activate
```

### List available datasets

By default, `list.py` lists 10 `csv/VehiclePosition` dataset names and their sizes at a time interactively to the console, starting from the first available ones:

```
> python list.py
csv/VehiclePosition/2020-04-22-01.csv              822.1MiB            
csv/VehiclePosition/2020-04-22-02.csv              910.1MiB            
csv/VehiclePosition/2020-04-22-09.csv              261.0MiB            
csv/VehiclePosition/2020-04-22-10.csv              787.2MiB            
csv/VehiclePosition/2020-04-22-11.csv              954.1KiB            
csv/VehiclePosition/2020-04-22-12.csv              797.4MiB            
csv/VehiclePosition/2020-04-22-15.csv              605.1MiB            
csv/VehiclePosition/2020-04-22-16.csv              1.0GiB              
csv/VehiclePosition/2020-04-22-17.csv              959.1MiB            
csv/VehiclePosition/2020-04-22-18.csv              830.3MiB
ENTER to continue, type a number for new n of lines, or type anything else to quit:
```

Dataset properties can also be printed out in csv format.
This command fetches them in chunks of 1000 and saves them into a file (the script itself prints to stdout).

```
python list.py --csv --n 1000 > datasets.csv
```

Run `python list.py --help` for more help.

- *`csv/VehiclePosition` is set in the YAML configuration, there are some other dataset types as well.*
- *Filtering by date range would also be useful, but unfortunately the Azure Blob Storage API does not have a method for that (other than filtering by filename prefix), so in most cases fetching the complete list would be necessary anyway.*

### Download a dataset

*WIP*
