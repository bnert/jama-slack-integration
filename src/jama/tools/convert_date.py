from flask import make_response
import time
from dateutil.parser import parse

"""
Function produces and sends error message to user.

Attributes:
    None
"""
#TODO

def to_epoch_time(date):
    date_time = parse(date)
    return date_time.timestamp()
