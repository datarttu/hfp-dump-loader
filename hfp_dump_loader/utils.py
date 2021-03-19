"""Utility functions and constants."""

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
