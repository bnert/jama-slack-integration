import time
from dateutil.parser import parse

def convert(date):
    """
    Function will convert date to a human friendly format.
    Args:
       date (string): The unfriendly date string to be parsed 
    Returns:
       (string): The human friendly date string produced by the time objects timestamp method 
    """
    date_time = parse(date)
    return date_time.timestamp()
