import pandas as pd
from pathlib import Path 

from util.data.misc import CannotUpdateError, data_colnames, get_year_max
from util.database.dbread import read_table

__id = 601
__vid_adp = 60100
__vid_booking = 60101

def __read_jail_from_disk(year):
    """Read from disk the given year's jail data."""
    try:
        path = str(Path(f'//MAINFILESRV/r&a/DATA/JAIL/{year} ICJIA County SUB Totals.xls'))
        return pd.read_excel(path)
    except FileNotFoundError:
        raise CannotUpdateError("ERROR: Jail data is already up to date!")
    except:
        raise

def __fix_cook_value_in_jail_data(df, adp_val, booking_val):
    """Revise Cook County's records in jail data."""
    try:
        c_cook = df['fk_data_county'] == 16
        c_adp = df['fk_data_variable'] == __vid_adp
        c_booking = df['fk_data_variable'] == __vid_booking

        if adp_val is not None:
            df.loc[c_cook & c_adp, 'value'] = adp_val
        
        if booking_val is not None:
            df.loc[c_cook & c_booking, 'value'] = booking_val
        
        return df
    except:
        raise

def __convert_county_name_to_id(df):
    """Convert county name to its ID value."""
    try:
        county = read_table('County')
        county_id_dict = dict(zip(county['county_name'].str.lower(), county['id'].astype(int)))
        county_to_id = lambda x: county_id_dict[x.lower()]
        
        df['county'] = df['county'].str.extract('(.*) County.*')
        df.loc[df['county'].isna(), 'county'] = 'Tri-County'
        df.loc[df['county'] == 'DeWitt', 'county'] = 'De Witt'
        df.loc[df['county'] == 'Tri-County', 'county'] = 'Tri-County Jail'
        
        df['fk_data_county'] = df['county'].apply(county_to_id)
        
        return df
    except:
        raise

def __transform_jail(df, year, adp_val, booking_val):
    """Transform jail data into the proper format."""
    try:
        df = df[~df['Month'].isna() & ~df['Facility'].str.contains('Alton')]
        df = df[['Facility', 'TOTAL Number of Bookings', 'Average Monthly Pop']]
        
        list_variable_id_str = [str(id) in [__vid_adp, __vid_booking]]

        df.columns = ['county'] + list_variable_id_str

        dict_agg = {
            str(__vid_adp): 'mean',
            str(__vid_booking): 'sum'
        }
        
        df = df.groupby('county') \
            .agg(dict_agg) \
            .reset_index(drop=True)
        df['year'] = year
        
        df = pd.melt(
            df,
            id_vars=['county', 'year'],
            value_vars=list_variable_id_str,
            var_name='fk_data_variable'
        ).reset_index(drop=True)

        df['fk_data_variable'] = df['fk_data_variable'].astype(int)
        df['year'] = df['year'].astype(int)

        df = __convert_county_name_to_id(df)[data_colnames]

        return __fix_cook_value_in_jail_data(df, adp_val, booking_val)
    except:
        raise

def prepare_jail_data(year=None, booking_val=None, adp_val=None):
    """Return the next year's employment data in the proper format.
    
    This function prepares the Illinois Department of Correction's
    Illinois County Jail Population data for a new year. The function fetches
    the following year's Illinois County Jail Population data from the network
    drive location, transforms it to the proper format, and returns a ``Data``
    input for the relevant variables.

    Args:
        year (int): Year for the new records. If None, the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Jail data in the ``Data`` format.

    """
    try:
        if year is None:
            year = get_year_max(__id) + 1
        df = __read_jail_from_disk(year)
        
        return __transform_jail(df, year, booking_val, adp_val)
    except:
        raise