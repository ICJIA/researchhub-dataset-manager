import pandas as pd
import re
from xlrd import XLRDError

from util.data.misc import CannotUpdateError, data_colnames, get_list_dataset_id, get_year_max
from util.database.dbread import read_table

__id_index = 500
__id_index_arrest = 500
__id_ht = 502
__id_ht_arrest = 503
__id_drug_arrest = 504
__id_domestic = 505
__id_hate = 506
__id_school = 507

dict_ucr_variable = {
    'ch':50000,
    'rape':50001,
    'rob':50002,
    'aggba':50003,
    'theft':50004,
    'burg':50005,
    'mvt':50006,
    'arson':50007,
    
    'ach':50100,
    'arape':50101,
    'arob':50102,
    'aaggba':50103,
    'atheft':50104,
    'aburg':50105,
    'amvt':50106,
    'aarson':50107,
    
    'htsex':50200,
    'htserve':50201,
    
    'ahtsex':50300,
    'ahtserve':50301,
    
    'acca': 50400,
    'acsa':50401,
    'ahsna':50402,
    'adpa':50403,
    'ameth':50404,
    
    'domestic':50500,
    
    'hate':50600,
    
    'school':50700,
}

def __fetch_ucr_from_url(which, year):
    """Fetch from online the given year's UCR data."""
    try:
        yy = str(year)[2:]
        yy_pre = str(year - 1)[2:]
        
        dict_which = {
            'index': 'CrimeData',
            'domestic': 'DomesticOffenses',
            'hate': 'HateCrime',
            'school': 'SchoolIncidents'
        }

        filename = f'{dict_which[which]}_{yy}_{yy_pre}'
        url = f'http://www.isp.state.il.us/docs/cii/cii{yy}/ds/{filename}.xlsx'
        return pd.read_excel(url)
    except XLRDError:
        raise CannotUpdateError("ERROR: Uniform Crime Report data is already up to date!")
    except:
        raise

def __rename_cols(x, year):
    return x[:-2].lower() if x[-2:] == str(year)[2:] else x.lower()

def __select_cols(x):
    return not re.search('\d', x)

def __standardize_county(df):
    return df.assign(county=df['county'].str.lower().str.replace(' ', ''))

def __transform_ucr_helper(df, year):
    """Help to transform UCR data."""
    try:
        def helper(df, year):
            rename_cols = lambda x: __rename_cols(x, year)
            
            return (
                df
                .rename(columns=rename_cols)
                .loc[:, df.rename(columns=rename_cols).columns.map(__select_cols)]
                .pipe(__standardize_county)
                .assign(year=year)
                .iloc[:102, ]
            )
        
        return pd.concat([helper(df, year), helper(df, year - 1)])
    except:
        raise

def __transform_ucr_index(df, year):
    """Transform UCR data for index crimes."""
    try:
        df = __transform_ucr_helper(df, year) \
            .drop(['aindex', 'arate'], axis=1)
        
        return pd.concat([
                df.loc[:, ['year', 'county']],
                df.loc[:, 'ch':'ahtserve'],
                df.loc[:, 'acca':'ameth']
            ],
            axis=1
        )
    except:
        raise

def __transform_ucr_school(df, year):
    """Transform UCR data for school incidents."""
    try:
        rename_cols = lambda x: __rename_cols(x, year)
        
        df = df.rename(columns=rename_cols)
        df = df.loc[:, df.columns.map(__select_cols)] \
            .drop('agency_name', axis=1) \
            .groupby('county', as_index=False) \
            .sum()

        school_cols = [
            'ch',
            'csa',
            'aggbatt',
            'batt',
            'aggasslt',
            'assault',
            'intimidate'
        ]
        df['school'] = df[school_cols].sum(axis=1)

        return __standardize_county(df[['county', 'school']])
    except:
        raise


def __transform_ucr(year, which):
    """Transform the specificed UCR data."""
    try:
        dict_transformer = {
            'index': __transform_ucr_index,
            'school': __transform_ucr_school
        }

        transformer = dict_transformer.get(which, __transform_ucr_helper)
        df = __fetch_ucr_from_url(which, year)
        return transformer(df, year)
    except:
        raise

def __prepare_info_ucr(year):
    """Prepare UCR information to merge."""
    try:
        index = __transform_ucr(year, 'index')
        domestic = __transform_ucr(year, 'domestic')
        hate = __transform_ucr(year, 'hate')
        school = __transform_ucr(year, 'school')

        df = index \
            .merge(domestic, how='left') \
            .merge(hate, how='left') \
            .merge(school, how='left')
        
        return __standardize_county(df)
    except:
        raise

def __prepare_info_county(df):
    """Prepare county information to merge."""
    try:
        df = df.loc[:103, ['id', 'county_name']]
        
        df['county_name'] = df['county_name'] \
            .str.lower() \
            .str.replace(' ', '')
        
        df.columns = ['fk_data_county', 'county']

        return df
    except:
        raise

def __merge_info(info_ucr, info_county):
    """Combine UCR and County information."""
    try:
        df = pd.melt(
            info_ucr.merge(info_county, how='left'),
            id_vars=['year', 'county', 'fk_data_county'],
            var_name='fk_data_variable',
            value_name='value'
        )
        
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        return df[data_colnames]
    except:
        raise

def __convert_variable_name_to_code(df):
    """Convert UCR variable names to their code values."""
    try:
        return (
           df
            .replace({'fk_data_variable': dict_ucr_variable})
            .sort_values(by=['year', 'fk_data_variable', 'fk_data_county'])
            .reset_index(drop=True)
        )
    except:
        raise

def __drop_bad_school_rows(df, year):
    """Drop previous year's school rows which were not provided."""
    try:
        c_drop = (df['year'] == year - 1) & (df['fk_data_variable'] == 'school')
        return df.drop(df[c_drop].index)
    except:
        raise

def prepare_ucr_data(year=None):
    """Return the next year's UCR data in the proper format.
    
    This function prepares the Illinois State Police's
    Uniform Crime Report (UCR) data for a new year. The function fetches the
    following year's UCR data from online,  transforms it to the proper format,
    and returns a ``Data`` input for the relevant variables.
    
    Args:
        year (int): Year for the new records. If None, the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: UCR data in the ``Data`` format.

    """
    try:
        y = get_year_max(__id_index) + 1 if year is None else year
        
        info_ucr = __prepare_info_ucr(y)
        info_county = __prepare_info_county(read_table('County'))
        info = __merge_info(info_ucr, info_county)
        info = __drop_bad_school_rows(info, y)

        return __convert_variable_name_to_code(info)
    except:
        raise