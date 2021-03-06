import pandas as pd
import pyodbc
from database.conn import Conn
from database.dbread import read_table

class CannotUpdateError(ValueError):
    """CannotUpdateError for this module."""
    pass

data_colnames = [
    'fk_data_variable',
    'fk_data_county',
    'year',
    'value'
]

def __build_sql(db, tbl, columns, condition):
    """Build a SQL statement from parameters."""
    columns = '*' if columns is None else columns
    condition = '' if condition is None else f' WHERE {condition}'

    return f'SELECT {columns} FROM {db}.dbo.{tbl}' + condition

def get_list_dataset_id(group):
    """Get a list of dataset ID values for the specified group."""
    dataset = read_table('Dataset')
    return dataset[dataset['grouping'] == group]['id'].tolist()

def get_list_variable_id(id):
    """Get a list of variable ID values for the specified dataset."""
    variable = read_table('Variable')
    return variable[variable['fk_variable_dataset'] == id]['id'].tolist()

def get_year_max(id):
    """Return the current maximum year for the specified ouptut."""
    try:
        dataset = read_table('Dataset')
        year_max = dataset[dataset['id'] == id]['year_max']
        
        return int(year_max)
    except:
        raise

def handle_no_record(df):
    """Give value 0 to counties without records."""
    all_county = pd.Series([i for i in range(1, 102+1)], name='fk_data_county')
    return df \
        .merge(all_county.to_frame(), how="outer") \
        .fillna(value={'value': 0}) \
        .fillna(method='ffill') \
        .sort_values(by=['year', 'fk_data_variable', 'fk_data_county'])

def read_mssql(db, tbl, columns=None, condition=None):
    """Read from the MS SQL Server a simple select query result. 
    
    Args:
        db (str): Database in the MS SQL Server (SPAC2SVR).
        tbl (str): Table for FROM statement.
        columns (str): Columns for SQL SELECT statement. If None, * is used.
        condition (str): Condition for SQL WHERE statement.
    
    Returns:
        pandas.DataFrame: A query result with lowercased column names. If empty, ValueError is thrown.
    """
    try:
        params = f'DRIVER=SQL Server;SERVER=SPAC2SVR;PORT=1433;DATABASE={db}'
        conn = pyodbc.connect(params)
        df = pd.read_sql(
            sql=__build_sql(db, tbl, columns, condition),
            con=conn
        )
        conn.close()

        if df.empty:
            raise CannotUpdateError('ERROR: No records found in the MS SQL Server - Data may be already up to date!')
        else:
            df.columns = [i.lower() for i in df.columns.tolist()]
            return df
    except pyodbc.Error as e:
        if e.args[0] == '42000':
            print(f"ERROR: Cannot access the SQL Server database: {db}!")