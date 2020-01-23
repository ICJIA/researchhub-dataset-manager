import pandas as pd
from util.database.conn import Conn

def read_table(table):
    """Return a table with the given name from database as a pandas DataFrame.
    
    Args:
        name (str): Table name.
    
    Returns:
        pandas DataFrame: Table from database.
    """
    try:
        sql = f'SELECT * FROM {table}'
        
        conn = Conn()
        df = pd.read_sql(sql, conn.self())
        conn.close()

        return df
    except:
        raise

def read_table_names():
    """Return a list of existing table names in database."""
    try:
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        conn = Conn()
        names = conn.execute(sql).fetchall()
        conn.close()
        
        return [name[0] for name in names]
    except AttributeError:
        print("ERROR: Database has no table.")
        raise
    except:
        raise

def read_view(view):
    """Return a table with the given name from database as a pandas DataFrame.
    
    Args:
        name (str): Table name.
    
    Returns:
        pandas DataFrame: Table from database.
    """
    try:
        return read_table(view)
    except:
        raise
