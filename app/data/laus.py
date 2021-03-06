import pandas as pd
from urllib.error import HTTPError

from data.misc import data_colnames, get_year_max, get_list_variable_id

__id = 605

def __fetch_laus_from_url(year):
    """Fetch from online the given year's LAUS data."""
    try:
        url = f'http://www2.illinois.gov/ides/LMI/Local%20Area%20Unemployment%20Statistics%20LAUS/historical/{year}-moaa.xls'
        return pd.read_excel(url, skiprows=6)
    except HTTPError as e:
        if e.code == 404:
            raise ValueError("ERROR: Employment data is already up to date!")
    except:
        raise

def __pivot_laus_variable(df, value_vars):
    try:
        return pd.melt(
            df,
            id_vars=['fips', 'year'],
            value_vars=value_vars,
            var_name='fk_data_variable'
        )
    except:
        raise

def __transform_laus(df):
    """Transform LAUS data into the proper format."""
    try:
        list_variable_id = [str(id) for id in get_list_variable_id(__id)]
        colnames = [
            'fips',
            'area',
            'year',
            'month',
            'force',
            'employed',
            'unemployed',
            'rate'
        ]
        colnames2 = ['fips', 'year'] + list_variable_id
        
        df2 = df.set_axis(colnames, axis='columns', inplace=False)
        c_has_fips = df2['fips'].notna()
        c_month_13 = df2['month'] == 13

        return df2 \
            .loc[c_has_fips & c_month_13] \
            .filter(items=['fips', 'year', 'force', 'unemployed', 'employed']) \
            .set_axis(colnames2, axis='columns', inplace=False) \
            .pipe(__pivot_laus_variable, value_vars=list_variable_id) \
            .assign(fk_data_county=lambda x: (x.fips + 1) / 2) \
            .filter(items=data_colnames)
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
        y = get_year_max(__id) + 1 if year is None else year

        return __fetch_laus_from_url(y) \
            .pipe(__transform_laus)
    except:
        raise