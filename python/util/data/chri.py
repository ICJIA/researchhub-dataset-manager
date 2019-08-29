import pandas as pd
from util.data.misc import CannotUpdateError, data_colnames, get_list_variable_id, get_year_max, handle_no_record, read_mssql

__id = 200

def __read_chri_from_mssql(year):
    """Read from the MS SQL Server the specified year's CHRI data."""
    try:
        database = 'AnnualPulls'
        tbl = 'Arrests'
        cols = 'ArrestYear, ArrestAge, EventORI'
        condition = f'ArrestYear = {year}'

        return read_mssql(database, tbl, cols, condition)
    except:
        raise

def __transform_chri(df):
    """Transforms a raw CHRI query result into a proper format."""
    try:
        df['year'] = df['arrestyear']
        df['county'] = df['eventori'].str[2:5].replace('CPD', '016')
        df = df[df['county'].str.contains('\d{3}')].copy()
        df.loc[:, 'fk_data_county'] = df['county'].astype(int)

        c = df['arrestage'].isin(range(10,17+1))
        df.loc[:,'fk_data_variable'] = get_list_variable_id(__id)[0]
        g = ['fk_data_variable', 'year', 'fk_data_county']
        
        df = df[c] \
            .groupby(g) \
            .size() \
            .reset_index(name='value')
            
        return df[data_colnames]
    except:
        raise


def prepare_chri_data(year=None):
    """Return the next year's CHRI data in the proper format.
    
    This function prepares the Criminal History Record Information (CHRI) data
    for a new year. The fuction fetches the following year's CHRI data from
    the ``AnnualPulls`` database  in MS SQL Server (SPAC2SVR), transforms it to
    the proper format, and returns a ``Data`` input for the relevant variables.

    Args:
        year (int): Year for the new records. If None, the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: CHRI data in ``Data`` format.

    """
    try:
        y = get_year_max(__id) + 1 if year is None else year
        df = __read_chri_from_mssql(y)
        
        return handle_no_record(__transform_chri(df))
    except:
        raise