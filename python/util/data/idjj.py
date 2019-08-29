import pandas as pd
from util.data.misc import (CannotUpdateError, data_colnames,
    get_list_variable_id, get_year_max, read_mssql)

__id_admit = 400
__id_exit = 401
__id_admit_older = 402
__id_exit_older = 403

def __read_idjj_from_mssql(year, exit=False):
    """Read from the MS SQL Server the specified year's IDOC data."""
    try:
        database = 'PrisonMain'
        tbl = 'IDJJ_exits' if exit else 'IDJJ_Admissions'
        cols = 'Age, SFY, County, sex, race, admtypo, OFFTYPE9, hclass'
        condition = f'SFY = {year}'

        if exit:
            cols = 'Exit' + cols

        return read_mssql(database, tbl, cols, condition)
    except:
        raise

def __get_list_variable_id_idjj(exit, older):
    """Get a list of variable ID values for the specified IDJJ data type."""
    dict_dataset_id = {
        (False, False): __id_admit,
        (True, False): __id_exit,
        (False, True): __id_admit_older,
        (True, True): __id_exit_older
    }

    dataset_id = dict_dataset_id[(older, exit)]
    return get_list_variable_id(dataset_id)

def __get_idjj_criteria(df, older):
    """Return filtering criteria for transforming a raw IDJJ query result."""
    c_age = df['age'].isin(range(17, 20+1) if older else range(13, 16+1))
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

    c_heads = [c_new, c_ce, c_tv]
    c_tails = [
        c_male,
        c_female,
        c_whi,
        c_blk,
        c_hsp,
        c_pers,
        c_prop,
        c_drug,
        c_weap,
        c_sex,
        c_felo,
        c_misd
    ]
    
    return c_age, c_new, c_heads, c_tails

def __transform_idjj(df, exit=False, older=False):
    """Transform the specificed IDJJ data."""
    try:
        df.columns = ['age', 'year', 'fk_data_county'] + df.columns.tolist()[3:]

        c_age, c_new, c_heads, c_tails = __get_idjj_criteria(df, older)
        
        def helper(c, var, heads):
            df['fk_data_variable'] = var
            df = df[c_age & c] if heads else df[c_age & c_new & c]
            
            g = ['fk_data_variable', 'year', 'fk_data_county']
            
            return df.groupby(g).size().reset_index(name='value')

        list_variable_id = __get_list_variable_id_idjj(exit, older)
        
        out = pd.DataFrame()
        for i in range(3):
            out = out.append(helper(c_heads[i], list_variable_id[i], heads=True))
            
        for i in range(len(c_tails)):
            out = out.append(helper(c_tails[i], list_variable_id[i+3], heads=False))
        
        out = out.loc[out['fk_data_county'].isin(range(1,102+1))]
        
        return out[data_colnames]
    except:
        raise

def __transform_and_combine_idjj(df_a, df_e):
    """Combine all transformed IDJJ data."""
    try:
        return (
            __transform_idjj(df_a)
                .append(__transform_idjj(df_a, older=True))
                .append(__transform_idjj(df_e, exit=True))
                .append(__transform_idjj(df_e, exit=True, older=True))
        )
    except:
        raise

def prepare_idjj_data(year=None):
    """Return the next year's IDJJ data in the proper format.
    
    This function prepares the Illinois Department of Juvenile Justice's (IDJJ's)
    juvenile court admission and exit data for a new year. The fuction reads
    the following year's IDJJ data from ``PrisonMain.dbo.IDJJ_Admissions`` and
    ``PrisonMain.dbo.IDJJ_Exits`` tables in MS SQL Server (SPAC2SVR),
    transforms it to the proper format, and returns a ``Data`` input for
    the relevant variables.

    Args:
        year (int): Year for the new records. If None, the year after the current maximum year in database.
    
    Returns:
        pandas.DataFrame: IDJJ data in ``Data`` format.

    """
    try:
        if year is None:
            year = get_year_max(__id_admit) + 1
        df_a = __read_idjj_from_mssql(year)
        df_e = __read_idjj_from_mssql(year, exit=True)
        
        return __transform_and_combine_idjj(df_a, df_e)
    except:
        raise