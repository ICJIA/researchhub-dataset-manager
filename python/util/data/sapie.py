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
 
def __transform_poverty(df, year):
    """Transform poverty data into the proper format."""
    try:
        pattern = '.{3}(?P<fips>.{3}).(?P<all>.{8}).{34}(?P<minor>.{8}).*'
        df = df['raw'].str.extract(pattern)
        df['year'] = year
        df['fips'] = df['fips'].astype(int) + 1 / 2
        
        list_variable_id_total = [str(id) for id in get_list_variable_id(__id_total)]
        list_variable_id_minor = [str(id) for id in get_list_variable_id(__id_minor)]
        list_variable_id = list_variable_id_total + list_variable_id_minor
        
        df.columns = ['fk_data_county'] + list_variable_id + ['year']
        df = pd.melt(
            df.astype(int),
            id_vars=['fk_data_county', 'year'],
            value_vars=list_variable_id,
            var_name='fk_data_variable'
        )

        return df[data_colnames]
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
        df = __fetch_poverty_from_url(y)
        
        return __transform_poverty(df, y)
    except:
        raise