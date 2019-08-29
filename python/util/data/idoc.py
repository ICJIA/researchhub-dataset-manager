import pandas as pd

from util.data.misc import data_colnames, get_list_variable_id, get_year_max, handle_no_record, read_mssql
from util.database.main import read_table

__id = 300

def __read_idoc_from_mssql(year):
    """Read from the MS SQL Server the specified year's IDOC data."""
    try:
        database = 'PrisonMain'
        tbl = 'PrisonAdmits'
        cols = 'FiscalYr, COMCNTY, SEX, ADMTYPO3, OFFTYPE2, OFFTYPE3'
        condition = f'FiscalYr = {year}'

        return read_mssql(database, tbl, cols, condition)
    except:
        raise

def __get_idoc_criteria(df):
    """Return filtering criteria for transforming a raw IDOC query result."""
    c_nc = df['admtypo3'] == 1
    c_tv = df['admtypo3'] == 2
    c_pers = df['offtype2'] == 1
    c_prop = df['offtype2'] == 2
    c_sex = df['offtype2'] == 4
    c_drug = df['offtype2'].isin([3.1, 3.2, 3.3, 3.4, 3.5, 3.6])
    c_other = df['offtype2'].isin([0, 3, 5, 7])
    c_viol = df['offtype3'] == 1
    c_male = df['sex'] == 'M'
    c_female = ~c_male

    c_heads = [c_nc, c_tv]
    c_tails = [
        c_pers,
        c_prop,
        c_sex,
        c_drug,
        c_other,
        c_viol,
        c_male,
        c_female
    ]
    return c_nc, c_heads, c_tails

def __transform_idoc(df):
    """Transforms a raw IDOC query result into a proper format."""
    try:
        df['comcnty'] = ((df['comcnty'] + 1) / 2).astype(int)
        df.columns = ['year', 'fk_data_county'] + df.columns.tolist()[2:]

        c_nc, c_heads, c_tails = __get_idoc_criteria(df)

        def helper(c, var, heads):
            df['fk_data_variable'] = var
            df = df[c] if c_heads else df[c_nc & c]
 
            g = ['fk_data_variable', 'year', 'fk_data_county']
            
            return df.groupby(g).size().reset_index(name='value')
        
        list_variable_id = get_list_variable_id(__id)

        out = pd.DataFrame()
        for i in range(2):
            out = out.append(helper(c_heads[i], list_variable_id[i], heads=True))
            
        for i in range(len(c_tails)):
            out = out.append(helper(c_tails[i], list_variable_id[i+2], heads=False))

        out = out \
            .loc[out['fk_data_county'] \
            .isin(range(1,102+1))]
        
        return out[data_colnames]
    except:
        raise

def prepare_idoc_data(year=None):
    """Return the next year's IDOC data in the proper format.
    
    This function prepares the Illinois Department of Corrections' (IDOC's)
    prison admission data for a new year. The fuction reads the following year's
    IDOC data from the ``PrisonMain.dbo.PrisonAdmits`` table in
    MS SQL Server (SPAC2SVR), transforms it to the proper format, and returns
    a ``Data`` input for the relevant variables.

    Args:
        year (int): Year for the new records. If None, the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: IDOC data in ``Data`` format.

    """
    try:
        if year is None:
            year = get_year_max(__id) + 1
        df = __read_idoc_from_mssql(year)
        
        return handle_no_record(__transform_idoc(df))
    except:
        raise