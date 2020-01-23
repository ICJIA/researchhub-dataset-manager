import pandas as pd
from pathlib import Path 

from data.misc import CannotUpdateError, data_colnames, get_year_max
from database.dbread import read_table

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

def __fix_cook_value(df, adp_val, booking_val):
    """Revise Cook County's records in jail data."""
    try:
        c_cook = df['fk_data_county'] == 16

        if adp_val is not None:
            c_adp = df['fk_data_variable'] == __vid_adp
            df.loc[c_cook & c_adp, 'value'] = adp_val
        
        if booking_val is not None:
            c_booking = df['fk_data_variable'] == __vid_booking
            df.loc[c_cook & c_booking, 'value'] = booking_val
        
        return df
    except:
        raise

def __rename_county(df):
    try:
        df = df.copy()
        df['county'] = df['county'].str.extract('(.*) County.*')
        df.loc[df['county'].isna(), 'county'] = 'Tri-County'
        df.loc[df['county'] == 'DeWitt', 'county'] = 'De Witt'
        df.loc[df['county'] == 'Tri-County', 'county'] = 'Tri-County Jail'
        return df
    except:
        raise

def __county_name_to_id(df):
    """Convert county name to its ID value."""
    try:
        county = read_table('County')
        county_id_dict = dict(zip(county['county_name'].str.lower(), county['id'].astype(int)))
        county_to_id = lambda x: county_id_dict[x.lower()]
        
        return df \
            .pipe(__rename_county) \
            .assign(fk_data_county=lambda x: x.county.apply(county_to_id))
    except:
        raise

def __pivot_jail_variable(df):
    try:
        return pd.melt(
                df,
                id_vars=['county', 'year'],
                value_vars=[str(__vid_adp), str(__vid_booking)],
                var_name='fk_data_variable'
            ) \
            .reset_index(drop=True) \
            .astype({'fk_data_variable': 'int64', "year": 'int64'})
    except:
        raise

def __transform_jail(df, year):
    """Transform jail data into the proper format."""
    try:
        c_has_month = df['Month'].notna()
        c_no_alton = ~df['Facility'].str.contains('Alton')
        dict_agg = {
            str(__vid_adp): 'mean',
            str(__vid_booking): 'sum'
        }
        
        return df \
            .loc[c_has_month & c_no_alton, [
                'Facility',
                'TOTAL Number of Bookings',
                'Average Monthly Pop'
            ]] \
            .rename({
                'Facility': 'county',
                'TOTAL Number of Bookings': str(__vid_booking),
                'Average monthly Pop': str(__vid_adp)
            }) \
            .groupby('county') \
            .agg(dict_agg) \
            .reset_index(drop=True) \
            .assign(year=year) \
            .pipe(__pivot_jail_variable) \
            .pipe(__county_name_to_id) \
            .filter(items=data_colnames)
    except:
        raise

def prepare_jail_data(year=None, adp_val=None, booking_val=None):
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
        y = get_year_max(__id) + 1 if year is None else year

        return __read_jail_from_disk(y) \
            .pipe(__transform_jail, y) \
            .pipe(__fix_cook_value, adp_val, booking_val)
    except:
        raise