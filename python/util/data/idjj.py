import pandas as pd
from util.data.misc import (CannotUpdateError, data_colnames,
    get_list_variable_id, get_year_max, handle_no_record, read_mssql)

__id_admit = 400
__id_exit = 401
__id_admit_older = 402
__id_exit_older = 403

def __read_idjj_from_mssql(year, exit):
    """Read from the MS SQL Server the specified year's IDOC data."""
    try:
        columns = 'Age, SFY, County, sex, race, admtypo, OFFTYPE9, hclass'
        
        return read_mssql(
            db='PrisonMain',
            tbl='IDJJ_exits' if exit else 'IDJJ_Admissions',
            columns='Exit' + columns if exit else columns,
            condition=f'SFY = {year}'
        )
    except:
        raise

def __read_all_idjj(year):
    return {
        'df_admit': __read_idjj_from_mssql(year, exit=False),
        'df_exit': __read_idjj_from_mssql(year, exit=True)
    }

def __get_list_variable_id_idjj(exit, older):
    """Get a list of variable ID values for the specified IDJJ data type."""
    dict_dataset_id = {
        (False, False): __id_admit,
        (True, False): __id_exit,
        (False, True): __id_admit_older,
        (True, True): __id_exit_older
    }

    return get_list_variable_id(dict_dataset_id[(older, exit)])

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

def __transform_idjj(df, exit, older):
    """Transform the specificed IDJJ data."""
    try:
        df.columns = ['age', 'year', 'fk_data_county'] + df.columns.tolist()[3:]

        c_age, c_new, c_heads, c_tails = __get_idjj_criteria(df, older)
        list_variable_id = __get_list_variable_id_idjj(exit, older)
        
        def helper(df, i, heads):
            return df \
                .loc[c_age & c_heads[i] if heads else c_age & c_new & c_tails[i]] \
                .assign(fk_data_variable=list_variable_id[i if heads else i+3]) \
                .groupby(['fk_data_variable', 'year', 'fk_data_county']) \
                .size() \
                .reset_index(name='value')

        return pd.concat(
                [helper(df, i, heads=True) for i in range(3)] +
                [helper(df, i, heads=False) for i in range(len(c_tails))],
                ignore_index=True
            ) \
            .filter(items=data_colnames) \
            .query('1 <= fk_data_county <= 102')
    except:
        raise

def __transform_all_idjj(df_admit, df_exit):
    """Return a list of all transformed IDJJ data."""
    try:
        return [
            __transform_idjj(df_admit, exit=False, older=False),
            __transform_idjj(df_admit, exit=False, older=True),
            __transform_idjj(df_exit, exit=True, older=False),
            __transform_idjj(df_exit, exit=True, older=True)
        ]
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
        y = get_year_max(__id_admit) + 1 if year is None else year
        list_transformed = __transform_all_idjj(**__read_all_idjj(y))
        
        return pd.concat(list_transformed, ignore_index=True) \
            .pipe(handle_no_record)
    except:
        raise