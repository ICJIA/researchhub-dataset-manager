import pandas as pd
from urllib.error import HTTPError

from util.data.misc import data_colnames, get_list_variable_id, get_year_max

__id_total = 606
__id_minor = 607

def __fetch_poverty_from_url(year):
    """Fetch from online the given year's poverty data."""
    try:
        ext = 'txt' if year > 2003 else 'dat'
        url = 'https://www2.census.gov/programs-surveys/saipe/datasets/' +\
            f'{year}/{year}-state-and-county/est{str(year)[2:]}-il.{ext}'
        
        return pd.read_table(url, header=None, skiprows=1, names=['raw'])
    except HTTPError as e:
        if e.code == 404:
            raise ValueError("ERROR: Poverty data is already up to date!")
    except:
        raise

def __get_list_variable_id():
    try:
        total = get_list_variable_id(__id_total)
        minor = get_list_variable_id(__id_minor)
        return [str(id) for id in total + minor]
    except:
        raise

def __extract_variables(df):
    try:
        pattern = '.{3}(?P<fips>.{3}).(?P<all>.{8}).{34}(?P<minor>.{8}).*'
        return df['raw'].str.extract(pattern)
    except:
        raise

def __pivot_poverty_variable(df, value_vars):
    try:
        return pd.melt(
            df,
            id_vars=['fk_data_county', 'year'],
            value_vars=value_vars,
            var_name='fk_data_variable'
        )
    except:
        raise

def __transform_poverty(df, year):
    """Transform poverty data into the proper format."""
    try:
        list_variable_id = __get_list_variable_id()
        
        return df \
            .pipe(__extract_variables) \
            .assign(
                fips=lambda x: (x.fips.astype(int) + 1) / 2,
                year=year
            ) \
            .set_axis(
                ['fk_data_county'] + list_variable_id + ['year'],
                axis='columns',
                inplace=False
            ) \
            .astype(int) \
            .pipe(__pivot_poverty_variable, value_vars=list_variable_id) \
            .filter(items=data_colnames)
    except:
        raise

def prepare_poverty_data(year=None):
    """Return the next year's poverty data in the proper format.
    
    This function prepares the U.S. Census Bureau's
    Small Area Income and Poverty Estimates (SAIPE) data for a new year.
    The function fetches the following year's SAIPE data from online,
    transforms it to the proper format, and returns a ``Data`` input
    for the relevant variables.

    Args:
        year (int): Year for the new records. If None, the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Poverty data in the ``Data`` format.

    """
    try:
        y = get_year_max(__id_total) + 1 if year is None else year

        return __fetch_poverty_from_url(y) \
            .pipe(__transform_poverty, y)
    except:
        raise