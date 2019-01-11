import pandas as pd
from urllib.error import HTTPError

from util.data.misc import data_colnames, get_year_max, get_list_variable_id

__id = 605

def __fetch_laus_from_url(year):
    """Fetch from online the given year's LAUS data."""
    try:
        url = f'http://www.ides.illinois.gov/LMI/Local%20Area%20Unemployment%20Statistics%20LAUS/historical/{year}-moaa.xls'
        return pd.read_excel(url, skiprows=6)
    except HTTPError as e:
        if e.code == 404:
            raise ValueError("ERROR: Employment data is already up to date!")
    except:
        raise

def __transform_laus(df):
    """Transform LAUS data into the proper format."""
    try:
        df.columns = [
            'fips',
            'area',
            'year',
            'month',
            'force',
            'employed',
            'unemployed',
            'rate'
        ]
        df = df[(~df.fips.isna()) & (df.month == 13)]
        df = df.drop(columns=['area', 'month', 'rate'])
        
        list_variable_id = [str(id) for id in get_list_variable_id(__id)]
        
        df.columns = ['fips', 'year'] + list_variable_id
        df = pd.melt(
            df,
            id_vars=['fips', 'year'],
            value_vars=list_variable_id,
            var_name='fk_data_variable'
        )
        df['fk_data_county'] = (df['fips'] + 1) / 2
        
        return df[data_colnames]
    except:
        raise

def prepare_laus_data(year=None):
    """Return the next year's employment data in the proper format.
    
    This function prepares the Illinois Department of Employment Security's
    Local Area Unemployment Statistics (LAUS) data for a new year.
    The function fetches the following year's LAUS data from online,
    transforms it to the proper format, and returns a ``Data`` input
    for the relevant variables.

    Args:
        year (int): Year for the new records. If None, the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: LAUS data in the ``Data`` format.

    """
    try:
        if year is None:
            year = get_year_max(__id) + 1
        df = __fetch_laus_from_url(year)
        
        return __transform_laus(df)
    except:
        raise