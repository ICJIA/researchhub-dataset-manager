import os
import pandas as pd

from fs.misc import check_input_format

def get_input_path():
    """Return a path to input file (expecting only one at a time)."""
    dirpath = 'input'
    
    try:
        return f'{dirpath}/{os.listdir(dirpath)[0]}'
    except IndexError:
        raise FileNotFoundError('ERROR: No file is found in "input" folder.')

def get_list_filename(dirname):
    """Return a list of filenames in a directory."""
    return os.listdir(dirname)