"""Offer functions for handling user input in ``@/input``.

This module offer functions to import user input files from the drive.
It must be noted that only one user input file should be in ``@/input``
per use. If there are multiple files in ``@/input``, the module will only see
the first file in the alphabetical order.
The module depends on ``database`` module.

The module contains the following public functions to be called externally:

``init()`` initializes the ``inputtools`` module.
``fetch_data()`` reads in a user input file from ``@/input``.

"""
import os
import pandas as pd

from . import database

class FormatError(Exception):
    """FormatError for this module."""
    pass

def init():
    """Initialize ``inputtools`` module."""
    try:
        database.CONN
    except (AttributeError, NameError):
        database.init()

    global _CONN
    global _DIR_PATH

    _CONN = database.CONN
    _DIR_PATH = 'P:\\DATA\\CJIA_WebData\\input'

def _check_input_format(user_input):
    """Return True if a user input is in the correct format."""
    global _CONN

    target = pd.read_sql_query(f'SELECT * FROM SimpleCount LIMIT 10;', _CONN)
    input_columns = user_input.columns.tolist()
    target_columns = target.columns.tolist()

    if isinstance(user_input, pd.DataFrame) and input_columns == target_columns:
        return True
    else:
        raise FormatError('ERROR: Incorrect user input format.')

def get_input_path():
    """Return a path to input file (expecting only one at a time)."""
    global _DIR_PATH
    try:
        return f'{_DIR_PATH}\\{os.listdir(_DIR_PATH)[0]}'
    except IndexError:
        raise IndexError('ERROR: No file is found in "input" folder.')

def fetch_data(population=False):
    """Fetch a user input file and return it as a pandas DataFrame.
    
    This function reads in a user input file from ``@/input`` and returns it
    as a pandas DataFrame. The input file must be in the proper format, i.e.
    the format of ``SimpleCount`` table in the SQL database
    (``@/database/cjia_webdata.db``).

    Args:
        population (bool): Population if True, SimpleCount otherwise.

    """
    input_path = get_input_path()
    input_data = pd.read_csv(input_path)
    try:
        if not population:
            _check_input_format(input_data)
        return input_data
    except:
        raise