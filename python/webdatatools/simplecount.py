"""Offer functions for updating the ``SimpleCount`` table in the database.

This module offer functions to automate the process of updating
the ``SimpleCount`` table in the database file, ``@/database/database.db``.
The module depends on ``database``, ``inputtools`` and ``outputtools`` modules.

The module contains the following public functions to be called externally:

``init()`` initalizes the ``simplecount`` module.
``fetch_input_and_create_temp()`` fetches input and create a temporary output.
``finalize_update()`` finalizes the process of updating the ``SimpleCount`` table.

"""
import math
import pandas as pd
import pyodbc
import re

from urllib.error import HTTPError
from xlrd import XLRDError

from . import database
from . import inputtools
from . import outputtools

def init():
    """Initialize the ``simplecount`` module."""
    try:
        database.CONN
    except Exception:
        database.init()
        print('Database connection established.')
    inputtools.init()
    outputtools.init()

    global _CONN
    global _NAME
    global _TEMP_NAME
    global _SIMPLECOUNT_COLUMNS
    global _UCR_INDICATOR_DICT
    
    _CONN = database.CONN
    _NAME = 'SimpleCount'
    _TEMP_NAME = f'Temp{_NAME}' 
    _SIMPLECOUNT_COLUMNS = ['fk_simplecount_indicator', 'fk_simplecount_county', 'year', 'value']
    _UCR_INDICATOR_DICT = {
        'domestic':1100,
        'school':1120,
        'hate':1130,
        'acca': 1400,
        'acsa':1401,
        'ahsna':1402,
        'adpa':1403,
        'ameth':1404,
        'ch':1410,
        'rape':1411,
        'rob':1412,
        'aggba':1413,
        'ach':1414,
        'arape':1415,
        'arob':1416,
        'aaggba':1417,
        'theft':1420,
        'burg':1421,
        'mvt':1422,
        'arson':1423,
        'atheft':1424,
        'aburg':1425,
        'amvt':1426,
        'aarson':1427,
        'htsex':1430,
        'htserve':1431,
        'ahtsex':1440,
        'ahtserve':1441,
    }

# automatic updating general
def _get_max_year(out_id_list):
    """Return the current maximum year for the specified ouptut."""
    try:
        indicator = database.fetch_tables(['Indicator'])[0]
        ind_list = indicator[indicator['fk_indicator_output'].isin(out_id_list)]['id'].tolist()
        ind_str = ', '.join([str(i) for i in ind_list])
        
        sql = f'SELECT MAX(year) FROM SimpleCount WHERE fk_simplecount_indicator in ({ind_str})'
        
        c = _CONN.cursor()
        c.execute(sql)
        max_year = c.fetchall()[0][0]
        c.close()

        return int(max_year)
    except:
        raise

def _fetch_from_ms_sql_server(database, table, columns=None, condition=None):
    """Fetch a simple select query result from the MS SQL Server.
    
    Args:
        database (str): Database in the MS SQL Server (SPAC2SVR).
        table (str): Table for FROM statement.
        columns (str): Columns for SQL SELECT statement. If None, * is used.
        condition (str): Condition for SQL WHERE statement.
    
    Returns:
        pandas.DataFrame: A query result with lowercased column names. If empty, ValueError is thrown.
    """
    try:
        params = f'DRIVER=SQL Server;SERVER=SPAC2SVR;PORT=1433;DATABASE={database}'
        conn = pyodbc.connect(params)

        columns = columns if columns is not None else '*'
        sql = f'SELECT {columns} FROM {database}.dbo.{table}'
        sql += f' WHERE {condition}' if condition is not None else ''
        
        df = pd.read_sql(sql, conn)
        conn.close()

        if df.empty:
            raise ValueError('ERROR: No records found in the MS SQL Server - Data may be up to date!')
        else:
            df.columns = [i.lower() for i in df.columns.tolist()]
            return df
    except pyodbc.Error as e:
        if e.args[0] == '42000':
            print(f"ERROR: Cannot access the SQL Server database: {database}!")
    except:
        raise

# automatic updating of CHRI data
def _transform_chri(df):
    """Transforms a raw CHRI query result into a proper format."""
    try:
        df['year'] = df['arrestyear']
        df['county'] = df['eventori'].str[2:5].replace('CPD', '016')
        df = df[df['county'].str.contains('\d{3}')].copy()
        df.loc[:, 'fk_simplecount_county'] = df['county'].astype(int)

        c = df['arrestage'].isin(range(10,17+1))
        df.loc[:,'fk_simplecount_indicator'] = 4000
        g = ['fk_simplecount_indicator', 'year', 'fk_simplecount_county']
        
        out = df[c].groupby(g).size().reset_index(name='value')
        return out[_SIMPLECOUNT_COLUMNS]
    except:
        raise

def _fetch_chri_data(year=None):
    """Automatically fetch the next year's CHRI data from the MS SQL Server.
    
    This function tries to automatically fetch the Criminal History Record
    Information (CHRI) data for a new year. The fuction fetches the following
    year's CHRI data from the ``AnnualPulls`` database  in MS SQL Server
    (SPAC2SVR), transforms it to the proper format, and returns
    a ``SimpleCount`` input for the relevant indicators.

    Args:
        year (int): Year for the new records. If None, automatically uses the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Data in ``SimpleCount`` format.

    """
    try:
        if year is None:
            year = _get_max_year([9]) + 1

        database = 'AnnualPulls'
        tbl = 'Arrests'
        cols = 'ArrestYear, ArrestAge, EventORI'
        condition = f'ArrestYear = {year}'

        df = _fetch_from_ms_sql_server(database, tbl, cols, condition)
        return _transform_chri(df)
    except:
        raise

# automatic updating of IDOC data
def _transform_idoc(df):
    """Transforms a raw IDOC query result into a proper format."""
    global _SIMPLECOUNT_COLUMNS

    try:
        df['comcnty'] = ((df['comcnty'] + 1) / 2).astype(int)
        df.columns = ['year', 'fk_simplecount_county'] + df.columns.tolist()[2:]

        indicator_list = [1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1620, 1621]
        
        c_nc = df['admtypo3'] == 1
        c_tv = df['admtypo3'] == 2
        c_pers = df['offtype2'] == 1 # df['offtype'] == 1
        c_prop = df['offtype2'] == 2 # df['offtype'] == 2
        c_sex = df['offtype2'] == 4 # df['offtype'] == 4
        c_drug = df['offtype2'].isin([3.1, 3.2, 3.3, 3.4, 3.5, 3.6]) # df['offtype'] == 3
        c_other = df['offtype2'].isin([0, 3, 5, 7]) # df['offtype'] == 7
        c_viol = df['offtype'] == 1
        c_male = df['sex'] == 'M'
        c_female = ~c_male

        c_first2 = [c_nc, c_tv]
        c_others = [c_pers, c_prop, c_sex, c_drug, c_other, c_viol, c_male, c_female]
        
        def helper(c, indicator_id, first2):
            df['fk_simplecount_indicator'] = indicator_id
            g = ['fk_simplecount_indicator', 'year', 'fk_simplecount_county']
            if first2:
                return df[c].groupby(g).size().reset_index(name='value')
            else:
                return df[c_nc & c].groupby(g).size().reset_index(name='value')

        out = pd.DataFrame()
        for i in range(2):
            out = out.append(helper(c_first2[i], indicator_list[i], first2=True))
            
        for i in range(len(c_others)):
            out = out.append(helper(c_others[i], indicator_list[i+2], first2=False))

        out = out.loc[out['fk_simplecount_county'].isin(range(1,102+1))]
        return out[_SIMPLECOUNT_COLUMNS]
    except:
        raise

def _fetch_idoc_data(year=None):
    """Automatically fetch the next year's IDOC data from the MS SQL Server.
    
    This function tries to automatically fetch the Illinois Department of
    Corrections' (IDOC's) prison admission data for a new year.
    The fuction fetches the following year's IDOC data from the
    ``PrisonMain.dbo.PrisonAdmits`` table in MS SQL Server (SPAC2SVR),
    transforms it to the proper format, and returns a ``SimpleCount`` input
    for the relevant indicators.

    Args:
        year (int): Year for the new records. If None, automatically uses the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Data in ``SimpleCount`` format.

    """
    try:
        if year is None:
            year = _get_max_year([10]) + 1

        database = 'PrisonMain'
        tbl = 'PrisonAdmits'
        cols = 'FiscalYr, COMCNTY, SEX, ADMTYPO3, OFFTYPE, OFFTYPE2'
        condition = f'FiscalYr = {year}'

        df = _fetch_from_ms_sql_server(database, tbl, cols, condition)
        return _transform_idoc(df)
    except:
        raise

# automatic updating of IDJJ data
def _tranform_idjj(df, age1720=False, exit=False):
    """Transform a raw IDJJ query result into a proper format."""
    global _SIMPLECOUNT_COLUMNS

    try:
        df.columns = ['age', 'year', 'fk_simplecount_county'] + df.columns.tolist()[3:]

        if not age1720:
            indicator_list = [701, 702, 703, 710, 711, 720, 721, 722, 730, 731, 732, 733, 734, 740, 741]
            c_age = df['age'].isin(range(13, 16+1))
        else:
            indicator_list = [704, 705, 706, 712, 713, 723, 724, 725, 735, 736, 737, 738, 739, 742, 743]
            c_age = df['age'].isin(range(17, 20+1))

        if exit:
            indicator_list = [i + 50 for i in indicator_list]
        
        c_new = df['admtypo'].isin(['CE', 'CER', 'DR', 'IC', 'MVN', 'PVN', 'RAM'])
        c_ce = df['admtypo'] == 'CE'
        c_tv = df['admtypo'].isin(['TMV', 'TPV'])
        c_male = df['sex'] == 'M'
        c_female = ~c_male
        c_whi = df['race'] == 'WHI'
        c_blk = df['race'] == 'BLK'
        c_hsp = df['race'] == 'HSP'
        c_pers = df['offtype9'] == 1
        c_prop = df['offtype9'] == 2
        c_drug = df['offtype9'] == 3
        c_weap = df['offtype9'] == 4
        c_sex = df['offtype9'] == 5
        c_felo = df['hclass'].isin(['M','X',1,2,3,4])
        c_misd = ~c_felo

        c_first3 = [c_new, c_ce, c_tv]
        c_others = [c_male, c_female, c_whi, c_blk, c_hsp, c_pers, c_prop, c_drug, c_weap, c_sex, c_felo, c_misd]
        
        def helper(c, indicator_id, first3):
            df['fk_simplecount_indicator'] = indicator_id
            g = ['fk_simplecount_indicator', 'year', 'fk_simplecount_county']
            if first3:
                return df[c_age & c].groupby(g).size().reset_index(name='value')
            else:
                return df[c_age & c_new & c].groupby(g).size().reset_index(name='value')

        out = pd.DataFrame()
        for i in range(3):
            out = out.append(helper(c_first3[i], indicator_list[i], first3=True))
            
        for i in range(len(c_others)):
            out = out.append(helper(c_others[i], indicator_list[i+3], first3=False))
        
        out = out[out['fk_simplecount_county'].isin(range(1,102+1))]
        return out[_SIMPLECOUNT_COLUMNS]
    except:
        raise

def _fetch_idjj_data(year=None):
    """Automatically fetch the next year's IDJJ data from the MS SQL Server.
    
    This function tries to automatically fetch the Illinois Department of
    Juvenile Justice's (IDJJ's) juvenile court admission and exit data for
    a new year. The fuction fetches the following year's IDJJ data from
    ``PrisonMain.dbo.IDJJ_Admissions`` and ``PrisonMain.dbo.IDJJ_Exits`` tables
    in MS SQL Server (SPAC2SVR), transforms it to the proper format,
    and returns a ``SimpleCount`` input for the relevant indicators.

    Args:
        year (int): Year for the new records. If None, automatically uses the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Data in ``SimpleCount`` format.

    """
    try:
        if year is None:
            year = _get_max_year([11, 12, 34, 35]) + 1

        database = 'PrisonMain'
        tbl_admit = 'IDJJ_Admissions'
        tbl_exit = 'IDJJ_exits'
        cols = 'Age, SFY, County, sex, race, admtypo, OFFTYPE9, hclass'
        condition = f'SFY = {year}'

        df_a = _fetch_from_ms_sql_server(database, tbl_admit, cols, condition)
        df_e = _fetch_from_ms_sql_server(database, tbl_exit, 'Exit'+cols, condition)

        return (
            pd.DataFrame()
            .append(_tranform_idjj(df_a))
            .append(_tranform_idjj(df_a, age1720=True))
            .append(_tranform_idjj(df_e, exit=True))
            .append(_tranform_idjj(df_e, age1720=True, exit=True))
        )
    except:
        raise

# automatic updating of UCR data
def _transform_ucr_data(df, which):
    """Transform a raw UCR table into a proper format."""
    try:
        df['county'] = df['county'].str.lower().str.replace(' ', '')

        if which == 'school':
            df = df.drop('agency_name', axis=1).groupby('county', as_index=False).sum()
            school_cols = ['ch', 'csa', 'aggbatt', 'batt', 'aggasslt', 'assault', 'intimidate']
            df['school'] = df[school_cols].sum(axis=1)
            return df[['county', 'school']]
        elif which == 'index':
            df = df.drop(['aindex', 'arate'], axis=1)
            df = pd.concat(
                [
                    df.loc[:, ['year', 'county']],
                    df.loc[:, 'ch':'ahtserve'],
                    df.loc[:, 'acca':'ameth']
                ],
                axis=1
            )
            return df # df.iloc[:102, ]
        else:
            return df # df.iloc[:102, ]
    except:
        raise

def _fetch_ucr_data_single(year, which):
    """Fetch and return a select UCR table in a proper format."""
    try:
        yy = str(year)[2:]
        yy_pre = str(year - 1)[2:]

        if which == 'index':
            filename = f'CrimeData_{yy}_{yy_pre}.xlsx'
        elif which == 'domestic':
            filename = f'DomesticOffenses_{yy}_{yy_pre}.xlsx'
        elif which == 'hate':
            filename = f'HateCrime_{yy}_{yy_pre}.xlsx'
        elif which == 'school':
            filename = f'SchoolIncidents_{yy}_{yy_pre}.xlsx'

        url = f'http://www.isp.state.il.us/docs/cii/cii{yy}/ds/{filename}'      
        df = pd.read_excel(url)
        select_cols = lambda x: not re.search('\d', x)

        if which == 'school':
            df = df.rename(columns=lambda x: x[:-2].lower() if x[-2:] == str(year)[2:] else x.lower())
            df = df.loc[:, df.columns.map(select_cols)]
        else:
            def helper(df,year):
                rename_cols = lambda x: x[:-2].lower() if x[-2:] == str(year)[2:] else x.lower()
            
                return (
                    df
                    .rename(columns=rename_cols)
                    .loc[:, df.rename(columns=rename_cols).columns.map(select_cols)]
                    .assign(year=year)
                    .iloc[:102, ]
                )

            df = pd.concat([helper(df, year), helper(df, year - 1)])

        return _transform_ucr_data(df, which)
    except XLRDError:
        raise ValueError("WARNING: Uniform Crime Report data is up to date.")
    except:
        raise

def _fetch_ucr_data(year=None):
    """Automatically fetch the next year's UCR data from the online source.
    
    This function tries to automatically fetch the Illinois State Police's
    Uniform Crime Report (UCR) data for a new year. The function fetches the
    following year's UCR data from online,  transforms it to the proper format,
    and returns a ``SimpleCount`` input for the relevant indicators.
    
    Args:
        year (int): Year for the new records. If None, automatically uses the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Data in ``SimpleCount`` format.

    """
    global _SIMPLECOUNT_COLUMNS
    global _UCR_INDICATOR_DICT
    
    try:
        if year is None:
            year = _get_max_year([13 ,14, 15, 16, 17, 18, 19, 20]) + 1
        
        index = _fetch_ucr_data_single(year, 'index')
        domestic = _fetch_ucr_data_single(year, 'domestic')
        hate = _fetch_ucr_data_single(year, 'hate')
        school = _fetch_ucr_data_single(year, 'school')

        combined = (
            index
            .merge(domestic, how='left')
            .merge(hate, how='left')
            .merge(school, how='left')
            # .fillna(0)
        )

        county_id = database.fetch_table('County') \
            .loc[:101, ['id', 'county_name']] \
            .sort_values(by='county_name')
        county_id['county_name'] = county_id['county_name'] \
            .str.lower() \
            .str.replace(' ', '')
        county_id.columns = ['fk_simplecount_county', 'county']

        pivoted = pd.melt(
                combined.merge(county_id, how='left'),
                id_vars=['year', 'county', 'fk_simplecount_county'],
                var_name='fk_simplecount_indicator',
                value_name='value'
            ) \
            .replace({'fk_simplecount_indicator': _UCR_INDICATOR_DICT}) \
            .sort_values(by=['year', 'fk_simplecount_indicator', 'fk_simplecount_county'])
        pivoted['value'] = pd.to_numeric(pivoted['value'], errors='coerce') #.fillna(0)

        return pivoted[_SIMPLECOUNT_COLUMNS]
    except:
        raise

# automatic updating of LAUS (employment) data
def _fetch_laus_data(year=None):
    """Automatically fetch the next year's employment data from the online source.
    
    This function tries to automatically fetch the Illinois Department of
    Employment Security's Local Area Unemployment Statistics (LAUS) data for
    a new year. The function fetches the following year's LAUS data from online, 
    transforms it to the proper format, and returns a ``SimpleCount`` input
    for the relevant indicators.

    Args:
        year (int): Year for the new records. If None, automatically uses the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Data in ``SimpleCount`` format.

    """
    global _SIMPLECOUNT_COLUMNS

    try:
        if year is None:
            year = _get_max_year([27]) + 1
        url = f'http://www.ides.illinois.gov/LMI/Local%20Area%20Unemployment%20Statistics%20LAUS/historical/{year}-moaa.xls'

        raw = pd.read_excel(url, skiprows=6)
        raw.columns = ['fips', 'area', 'year', 'month', 'force', 'employed', 'unemployed', 'rate']
        
        filtered = raw[(~raw.fips.isna()) & (raw.month == 13)].drop(columns=['area', 'month', 'rate'])
        filtered.columns = ['fips', 'year', '1030', '1551', '1550']

        pivoted = pd.melt(
            filtered,
            id_vars = ['fips', 'year'],
            value_vars=['1030', '1550', '1551'],
            var_name = 'fk_simplecount_indicator'
        )
        
        pivoted['fk_simplecount_county'] = (pivoted['fips'] + 1) / 2

        return pivoted[_SIMPLECOUNT_COLUMNS]
    except HTTPError as e:
        if e.code == 404:
            raise ValueError("WARNING: Employment data is up to date.")
    except:
        raise

# automatic updating of SAIPE (poverty) data
def _fetch_poverty_data(year=None):
    """Automatically fetch the next year's poverty data from the online source.
    
    This function tries to automatically fetch the U.S. Census Bureau's Small
    Area Income and Poverty Estimates (SAIPE) data for a new year.
    The function fetches the following year's SAIPE data from online,
    transforms it to the proper format, and returns a ``SimpleCount`` input
    for the relevant indicators.

    Args:
        year (int): Year for the new records. If None, automatically uses the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Data in ``SimpleCount`` format.

    """
    global _SIMPLECOUNT_COLUMNS

    try:
        if year is None:
            year = _get_max_year([30, 31]) + 1
        ext = 'txt' if year > 2003 else 'dat'
        url = f'https://www2.census.gov/programs-surveys/saipe/datasets/{year}/{year}-state-and-county/est{str(year)[2:]}-il.{ext}'

        raw = pd.read_table(url, header=None, skiprows=1, names=['raw'])
        pattern = '.{3}(?P<fips>.{3}).(?P<all>.{8}).{34}(?P<minor>.{8}).*'
        
        filtered = raw['raw'].str.extract(pattern)
        filtered['year'] = year
        filtered['fips'] = filtered['fips'].astype(int) + 1 / 2
        filtered.columns = ['fk_simplecount_county', '1200', '1201', 'year']

        pivoted = pd.melt(
                filtered.astype(int),
                id_vars = ['fk_simplecount_county', 'year'],
                value_vars=['1200', '1201'],
                var_name = 'fk_simplecount_indicator'
            )

        return pivoted[_SIMPLECOUNT_COLUMNS]
    except HTTPError as e:
        if e.code == 404:
            raise ValueError("WARNING: Poverty data is up to date.")
    except:
        raise

# automatic updating of jail data
def _fetch_jail_data(year=None):
    """Automatically fetch the next year's jail data from the network drive location.
    
    This function tries to automatically fetch the Illinois Department of Correction's
    Illinois County Jail Population data for a new year. The function fetches
    the following year's Illinois County Jail Population data from the network
    drive location, transforms it to the proper format, and returns
    a ``SimpleCount`` input for the relevant indicators.

    Args:
        year (int): Year for the new records. If None, automatically uses the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: Data in ``SimpleCount`` format.

    """
    global _SIMPLECOUNT_COLUMNS

    try:
        if year is None:
            year = _get_max_year([22]) + 1
        raw = pd.read_excel(f'P:\DATA\JAIL\{year} ICJIA County SUB Totals.xls')
        
        filtered = raw[~raw['Month'].isna() & ~raw['Facility'].str.contains('Alton')]
        filtered = filtered[['Facility', 'TOTAL Number of Bookings', 'Average Monthly Pop']]
        filtered.columns = ['county', '1500', '1510']
        
        aggregated = filtered.groupby('county').agg({'1500': 'sum', '1510': 'mean'}).reset_index(drop=True)
        aggregated['year'] = year
        
        pivoted = pd.melt(
            aggregated,
            id_vars = ['county', 'year'],
            value_vars= ['1500', '1510'],
            var_name = 'fk_simplecount_indicator'
        ).reset_index(drop=True)

        pivoted['county'] = pivoted['county'].str.extract('(.*) County.*')
        pivoted.loc[pivoted['county'].isna(), 'county'] = 'Tri-County'
        pivoted.loc[pivoted['county'] == 'DeWitt', 'county'] = 'De Witt'
        pivoted.loc[pivoted['county'] == 'Tri-County', 'county'] = 'Tri-County Jail'

        county = database.fetch_tables(['County'])[0]
        county_id_dict = dict(zip(county['county_name'].str.lower(), county['id'].astype(int)))
        county_to_id = lambda x: county_id_dict[x.lower()]

        pivoted['fk_simplecount_county'] = pivoted['county'].apply(county_to_id)
        pivoted['fk_simplecount_indicator'] = pivoted['fk_simplecount_indicator'].astype(int)
        pivoted['year'] = pivoted['year'].astype(int)

        return pivoted[_SIMPLECOUNT_COLUMNS]
    except FileNotFoundError:
        raise ValueError("WARNING: Jail data is up to date.")
    except:
        raise

def fix_cook_value_in_jail_data(jail_data, booking_value=math.nan, adp_value=math.nan):
    """Revise Cook County's records in jail data."""
    try:
        fixed = jail_data.copy()
        c_cook = fixed['fk_simplecount_county'] == 16
        c_booking = fixed['fk_simplecount_indicator'] == 1500
        c_adp = fixed['fk_simplecount_indicator'] == 1510

        if not math.isnan(booking_value):
            fixed.loc[c_cook & c_booking, 'value'] = booking_value
        if not math.isnan(adp_value):
            fixed.loc[c_cook & c_adp, 'value'] = adp_value
        
        return fixed
    except:
        raise

# general
def _fetch_input():
    """Fetch and return a prepared input data file from ``@/input``."""
    try:
        simplecount_input = inputtools.fetch_data()
        return simplecount_input
    except:
        raise

def _fetch_input_auto(source):
    """Fetch and return a prepared input data file based on source input."""
    if source not in ['chri', 'idoc', 'idjj', 'ucr', 'jail', 'employment', 'poverty']:
        raise ValueError('Invalid data source.')
    
    if source == 'chri':
        print('WAIT: Fetching Criminal History data...')
        return _fetch_chri_data()
    elif source == 'idoc':
        print('WAIT: Fetching Prison data...')
        return _fetch_idoc_data()
    elif source == 'idjj':
        print('WAIT: Fetching Juvenile Court data...')
        return _fetch_idjj_data()
    elif source == 'ucr':
        print('WAIT: Fetching Uniform Crime Report data...')
        return _fetch_ucr_data()
    elif source == 'jail':
        print('WAIT: Fetching Jail data...')
        return _fetch_jail_data()
    elif source == 'employment':
        print('WAIT: Fetching Employment data...')
        return _fetch_laus_data()
    elif source == 'poverty':
        print('WAIT: Fetching Poverty data...')
        return _fetch_poverty_data()

def _create_temp(simplecount_input):
    """Create temporary tables of the cleaned simplecount data.

    This function calls functions with the same name from two other modules,
    ``database`` and ``outputtools``, to create temporary tables in the SQL
    database (``@/database/cjia_webdata.db``) as well as in ``@/temp``.
    
    Args:
        simplecount_input (pandas DataFrame): Fetched data from ``@/input``.

    """
    global _TEMP_NAME

    try:
        database.create_temp(simplecount_input, _TEMP_NAME)
        outputtools.create_temp(simplecount_input, _TEMP_NAME)
    except:
        raise

def _add_to_master():
    """Append the temporary simplecount table to the master table.
    
    This function calls another function with the same name from the
    ``database`` module to append the temporary simplecount table
    (``TempSimpleCount``) to the master ``SimpleCount`` table in the SQL
    database (``@/database/cjia_webdata.db``).
    
    """
    global _TEMP_NAME
    global _NAME

    try:
        database.add_to_master(_TEMP_NAME, _NAME)
    except:
        raise ValueError(f'ERROR: Cannot add {_TEMP_NAME} table to {_NAME} table in the database!')

def _delete_temp():
    """Delete the temporary simplecount tables.

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

def fetch_input_and_create_temp(source=None, auto=False):
    """Fetch simplecount input and create temporary table in the database.

    This function calls private functions in the module to 1) fetch simplecount
    intput and 2) create temporary tables in the SQL database
    (``@/database/cjia_webdata.db``) as well as `@/temp`.

    Args:
        source (str): Data source if automatiically fetching data
        auto (bool): True if automatically fetching data from the source, False otherwise.

    Returns:
        bool: True for success, False otherwise.

    """
    try:
        if auto:
            simplecount_input = _fetch_input_auto(source)
        else:
            simplecount_input = _fetch_input()
        _create_temp(simplecount_input)
        return True
    except Exception as e:
        print(e)
        return False

def _remove_ucr_uncorrected_vals():
    """Remove the uncorrected UCR values from the simplecount table."""
    global _CONN
    global _UCR_INDICATOR_DICT

    try:
        c = _CONN.cursor()
        c.execute(f'SELECT max(year) FROM SimpleCount WHERE fk_simplecount_indicator = 1100')
        year = c.fetchone()[0]
        c.close()
        
        ucr_indicator_str = ', '.join([str(x) for x in _UCR_INDICATOR_DICT.values()])
        sql = f'DELETE FROM SimpleCount WHERE year = {year} AND fk_simplecount_indicator IN ({ucr_indicator_str})'
        database.execute_simple_sql(sql)
        print("NOTE: Uncorrected UCR data values are removed from the database prior to inserting the corrected values.")
    except:
        raise

def finalize_update(source=None):
    """Fianlize the updating of the ``SimpleCount`` table.

    This function calls private functions in the module to complete the
    process of updating ``SimpleCount`` table by 1) adding the temporary table
    to the master table in the SQL database and 2) deleting the temporary table
    from the database as well as `@/temp`.

    Args:
        source (str): Data source if automatiically fetching data

    Returns:
        bool: True for success, False otherwise.
    """
    try:
        if source == 'ucr':
            _remove_ucr_uncorrected_vals()
        
        _add_to_master()
        _delete_temp()
        return True
    except Exception as e:
        print(e)
        return False

