"""Offer functions for updating the ``Population`` table in the database.

This module offer functions to automate the process of updating
the ``Population`` table in the database file, ``@/database/database.db``.
The module depends on ``database``, ``inputtools`` and ``outputtools`` modules.

The module contains the following public functions to be called externally:

``init()`` initalizes the ``population`` module.
``fetch_input_and_create_temp()`` fetches input and create a temporary output.
``finalize_update()`` finalizes the process of updating the ``Population`` table.

"""
import pandas as pd
import requests

from io import BytesIO
from urllib.error import HTTPError
from zipfile import ZipFile

from . import database
from . import inputtools
from . import outputtools

def init():
    """Initialize the ``population`` module."""
    try:
        database.CONN
    except (AttributeError, NameError):
        database.init()
    inputtools.init()
    outputtools.init()
    
    global _CONN
    global _NAME
    global _TEMP_NAME

    _CONN = database.CONN
    _NAME = 'Population'
    _TEMP_NAME = f'Temp{_NAME}'
    
def _filter_illinois(df):
    """Filter to keep population estimates for Illinois only."""
    pattern = f'^\d{{{df["raw_value"].str.len().max() - 17}}}17'
    return df[df['raw_value'].str.contains(pattern)].reset_index(drop=True)

def _fetch_data_helper(raw_input):
    try:
        zip = ZipFile(raw_input)
        content = zip.open(zip.namelist()[0])
        fetched = pd.read_table(content, header=None, names=['raw_value'])
        return _filter_illinois(fetched)
    except:
        raise

def _fetch_data_auto_helper(v, y):
    """Automatically fetch a single year population estimates for Illinois.

    This function fetches a single population estimates data from the source
    ftp server, which contains the Bridged-Race Population Estimates datasets
    prepared by the National Center for Health Statistics of the Centers for
    Disease Control and Prevention.

    Args:
        v (int): Version year (YYYY) for the population data.
        y (int): Estimate year (yy) for the population data.

    Returns:
        pandas.DataFrame: Single year population estimates for Illinois.
    
    """
    filename = f'pcen_v{v}_y{y}_jul.txt.zip' if y % 10 == 0  else f'pcen_v{v}_y{y}.txt.zip'
    url = f'https://ftp.cdc.gov/pub/health_statistics/nchs/Datasets/NVSS/bridgepop/{v}/{filename}' 
    print(f'WAIT: Fetching {filename}...')

    res = requests.get(url, verify=False)
    if res.status_code == 200:
        return _fetch_data_helper(BytesIO(res.content))
    elif res.status_code == 404:
        raise ValueError('WARNING: Population is up to date!')
    else:
        res.raise_for_status()

def _fetch_data_auto(multi=True):
    """Automatically fetch the latest population estimates data.
    
    This function fetches the latest population data from the source ftp server,
    which contains the Bridged-Race Population Estimates datasets prepared by
    the National Center for Health Statistics of the Centers for Disease Control
    and Prevention.

    Args:
        multi (bool): Fetching all estimates since the latest census year if True; the latest year's estimates only if False. 

    Returns:
        pandas.DataFrame: Population estimates data for Illinois.

    """
    try:
        c = _CONN.cursor()
        c.execute('SELECT MAX(year) FROM Population;')
        year_max = c.fetchone()[0]
        c.close()

        v = year_max + 1
        y = v - 2000
        y_all = range(y - (y % 10), y + 1) if multi else range(y, y + 1)

        population_raw_input = pd.DataFrame()
        for y_each in y_all:
            try:
                fetched = _fetch_data_auto_helper(v, y_each)
                population_raw_input = population_raw_input.append(fetched).reset_index(drop=True)
            except:
                raise
    
        return population_raw_input
    except:
        raise

def _fetch_data_manual():
    """Manualy fetch the population estimates data from ``@/input`` and return as a pandas.DataFrame."""
    path = inputtools.get_input_path()
    if path.find('pcen_v\d{4}_y\d{2}(_jul)?.txt.zip'):
        return _fetch_data_helper(path)
    else:
        raise ValueError('Invalid population input!')

def _fetch_input(auto=True, multi=True):
    """Fetch the input for updating the population data.

    This function fetches
    
    Args:
        auto (bool): Automatically fetching data if True, manually providing input if False (default).
        multi (bool): Fetching all estimates since the latest census year if True; the latest year's estimates only if False. 
    
    Returns:
        pandas.DataFrame: Population data for Illinois in the original format.
    """
    try:
        return _fetch_data_auto(multi) if auto else _fetch_data_manual()
    except:
        raise

def _clean_data(population_raw_input):
    """Clean data by transforming it into the proper format.
    
    Args:
        population_raw_input (pandas.DataFrame): Population data in the original format.

    Returns:
        pandas.DataFrame: Transformed data in the proper format.
    
    """
    try:
        df = population_raw_input.copy()
        ix = df['raw_value'].str.len().max() - 15
        fips_to_icjia_num = lambda x: (int(x) + 1)/2

        df['FK_population_county'] = df['raw_value'].apply(lambda x: x[ix:ix+3]).apply(fips_to_icjia_num)
        df['year'] = df['raw_value'].apply(lambda x: x[:4])
        df['age'] = df['raw_value'].apply(lambda x: x[ix+3:ix+5])
        df['race_gender'] = df['raw_value'].apply(lambda x: x[ix+5])
        df['hispanic'] = df['raw_value'].apply(lambda x: x[ix+6])
        df['value'] = df['raw_value'].apply(lambda x: x[ix+7:])
        
        population_input = df.iloc[:, 1:].astype(int)

        return population_input
    except:
        raise

def _create_temp(population_input):
    """Create temporary tables of the cleaned population data.

    This function calls functions with the same name from two other modules,
    ``database`` and ``outputtools``, to create temporary tables in the SQL
    database (``@/database/cjia_webdata.db``) as well as in ``@/temp``.
    
    Args:
        population_input (pandas.DataFrame): Transformed data into the proper format.
    
    """
    global _TEMP_NAME

    try:
        database.create_temp(population_input, _TEMP_NAME)
        outputtools.create_temp(population_input, _TEMP_NAME)
    except:
        raise

def _delete_outdated_in_master(name_temp, name_master):
    """Delete from the master table all records to be outdated due to update.
    
    Args:
        name_temp (str): Name of the temporary table.
        name_master (str): Name of the master table.

    """
    try:
        c = _CONN.cursor()
        c.execute(f'SELECT MIN(year) FROM {name_temp};')
        year_min_t = c.fetchone()
        c.execute(f'SELECT MAX(year) FROM {name_temp};')
        year_max_t = c.fetchone()
        c.execute(f'SELECT MAX(year) FROM {name_master};')
        year_max_m = c.fetchone()
        c.close()

        if year_max_t <= year_max_m:
            raise ValueError('WARNING: Population table is already up-to-date.')
        else:
            sql = f'DELETE FROM {name_master} WHERE year BETWEEN {year_min_t} AND {year_max_t};'
            database.execute_simple_sql(sql)
            database.commit()
    except:
        raise

def _add_to_master():
    """Append the temporary population table to the master table.
    
    This function calls another function with the same name from the
    ``database`` module to append the temporary population table
    (``TempPopulation``) to the master ``Population`` table in the SQL database
    (``@/database/cjia_webdata.db``).
    
    """
    global _TEMP_NAME
    global _NAME

    try:
        _delete_outdated_in_master(_TEMP_NAME, _NAME)
        database.add_to_master(_TEMP_NAME, _NAME)
    except:
        raise

def _delete_temp():
    """Delete the temporary population tables.

    This function calls functions with the same name from two other modules,
    ``database`` and ``outputtools``, to delete temporary tables in the SQL
    database (``@/database/cjia_webdata.db``). as well as in ``@/temp``.

    """
    global _TEMP_NAME

    try:
        database.delete_temp(_TEMP_NAME)
        outputtools.delete_temp(_TEMP_NAME)
    except:
        raise

def fetch_input_and_create_temp(auto=True, multi=True):
    """Fetch population input and create temporary table in the database.

    This function calls private functions in the module to 1) fetch simplecount
    intput and 2) create temporary tables in the SQL database
    (``@/database/cjia_webdata.db``) as well as `@/temp`.

    Args:
        auto (bool): Automatically fetching data if True, manually providing input if False (default).
        multi (bool): Fetching all estimates since the latest census year if True; the latest year's estimates only if False. 

    Returns:
        bool: True for success, False otherwise.

    """
    try:
        population_raw_input = _fetch_input(auto, multi)
        population_input = _clean_data(population_raw_input)
        _create_temp(population_input)
        return True
    except Exception as e:
        print(e)
        return False

def finalize_update():
    """Fianlize the updating of the ``Population`` table.

    This function calls private functions in the module to complete the
    process of updating ``Population`` table by 1) adding the temporary table
    to the master table in the SQL database and 2) deleting the temporary table
    from the database as well as `@/temp`.

    Returns:
        bool: True for success, False otherwise.
    """
    try:
        _add_to_master()
        _delete_temp()
        return True
    except Exception as e:
        print(e)
        return False