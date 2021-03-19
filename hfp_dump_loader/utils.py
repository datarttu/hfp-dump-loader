"""Utility functions and constants."""

import pytz
from datetime import datetime

def milliseconds_to_timestamp(x):
    """Convert Unix milliseconds `x` into an UTC timestamp value."""
    return datetime.fromtimestamp(float(x) / 1000.0, tz=pytz.utc)

def milliseconds_to_date(x):
    """Convert Unix seconds `x` into a date value."""
    # NOTE: We have to check the results for oday validity,
    #       there may be a caveat with UTC / Europe/Helsinki tz...
    return datetime.fromtimestamp(float(x) / 1000.0, tz=pytz.utc).date()

# Available type cast names for config.yml and their respective functions.
TYPE_CASTS = {
    'int': int,
    'float': float,
    'timestamp': milliseconds_to_timestamp,
    'date': milliseconds_to_date
}

def cast_failing_to_none(x, f):
    """Return `f(x)`, returning `None` on any error."""
    try:
        return f(x)
    except:
        return None
