import os
import pandas as pd
import re
from zipfile import ZipFile

from util.data.misc import get_year_max
from util.database.dbread import read_table
from util.database.misc import is_valid_temp_name
from util.dataset.main import create_data_csv, create_metadata_json, create_readme_txt
from util.fs.fread import get_input_path, get_list_filename
from util.fs.fwrite import delete_file, write_file
from util.fs.misc import check_input_format

def delete_temp(name_temp=None):
    """Delete temporary tables in ``@/temp``.

    This function deletes temporary tables in ``@/temp``. If ``name`` is given,
    only a table with the given name will be deleted. Otherwise, all tables with
    "Temp" in their names will be deleted. 

    Args:
        name_temp (str): Name of a temporary table to delete. Default is None. If None, all temporary tables will be deleted.
    
    Returns:
        bool: True for success, False otherwise.

    """
    try:
        if name_temp is None:
            list_filename = get_list_filename('temp')
            for filename in list_filename:
                filename = re.sub('\..*', '', filename)
                if is_valid_temp_name(filename):
                    delete_file('temp', filename)
                    print(f"NOTE: Successfully removed {filename} from /temp/.")
        else:
            if is_valid_temp_name(name_temp):
                delete_file('temp', name_temp)
                print(f"NOTE: Successfully removed {name_temp} from /temp/.")
    except:
        raise

def read_data():
    """Read a user input file from disk and return it as a pandas DataFrame.
    
    This function reads in a user input file from ``@/input`` and returns it
    as a pandas DataFrame. The input file must be in the proper format, i.e.
    the format of ``Data`` table in the SQL database
    (``@/database/database.db``).

    """
    try:
        input_path = get_input_path()
        input_data = pd.read_csv(input_path)
        check_input_format(input_data)
        
        return input_data
    except:
        raise

def write_dataset(id):
    """Generate dataset for a provided ID."""
    try:
        dataset = read_table('Dataset')
        dataset_out = dataset[dataset['id'] == id]
        
        name = dataset_out['name'].iloc[0]
        year_max = int(dataset_out['year_max'])

        dirpath = 'datasets'
        path = f'{dirpath}/{name}.zip'
        with ZipFile(path, 'w') as z:
            z.writestr('README.txt', create_readme_txt(id))
            z.writestr('metadata.json', create_metadata_json(id))
            z.writestr(f'{year_max}_{name}.csv', create_data_csv(id))
        return True
    except Exception as e:
        print(e)
        return False

def write_datasets_in_group(group):
    """Generate all datasets for a provided group."""
    try:
        dataset = read_table('Dataset')
        out_source = dataset[dataset['group'] == group]
        list_dataset_id = out_source['id'].unique().tolist()
        for dataset_id in list_dataset_id:
            write_dataset(dataset_id)
        
        return True
    except Exception as e:
        print(e)
        return False

def write_temp(df, name_temp):
    """Create a temporary table in ``@/temp``.

    This function creates a temporary table with the given name and saves it in
    ``@/temp``.
    
    Args:
        df (pandas DataFrame): Data for the temporary table.
        name_temp (str): Name of the temporary table.
    
    Returns:
        bool: True for success, False otherwise.

    """
    try:
        if is_valid_temp_name(name_temp):
            write_file(df, 'temp', name_temp)
            if f'{name_temp}.csv' in os.listdir('temp'):
                print(f"NOTE: Successfully generated {name_temp} in /temp/.")
    except:
        print(f"ERROR: Cannot generate {name_temp}!")
        raise