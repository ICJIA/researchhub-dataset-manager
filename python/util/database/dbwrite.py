import pandas as pd
import re

from util.database.conn import Conn
from util.database.misc import execute_simple, get_type_sqlite

def create_table(df, name, commit=False):
    """Create an empty table in database if not exists.
    
    Args:
        df (pandas DataFrame): Data input to define columns.
        name (str): New table name.
        commit (bool): Commit the change if True.
    
    Returns:
        Conn: Connection object if not committing the change.
    """
    try:
        colnames = list(df)
        coltypes_py = [type(df[colname].iat[0]).__name__ for colname in colnames]
        coltypes = [get_type_sqlite(type_py) for type_py in coltypes_py]
        
        sql_cols = ''
        for i in range(len(colnames)):
            sql_cols += f'{colnames[i]} {coltypes[i]}'
            if i < len(colnames) - 1:
                sql_cols += ', '
        sql = f'CREATE TABLE IF NOT EXISTS {name} ({sql_cols})'
    
        if commit:
            execute_simple(sql, commit=True)
        else:
            return execute_simple(sql)
    except:
        raise


def insert_into_table(df, name, commit=False):
    """Insert data to an existing table in database.
        
    Args:
        df (pandas DataFrame): Data input.
        name (str): Table name.
        commit (bool): Commit the change if True.
    
    Returns:
        Conn: Connection object if not committing the change.
    """
    try:
        cols = ', '.join(list(df))
        params = ', '.join(['?' for i in range(len(list(df)))])
        sql = f'INSERT INTO {name} ({cols}) VALUES ({params});'

        conn = Conn()
        cursor = conn.cursor()
        cursor.executemany(sql, list(df.itertuples(index=False, name=None)))
        
        if commit:
            conn.commit()
            conn.close()
        else:
            return conn
    except:
        raise

def delete_from_table(name, commit=False):
    """Delete data from an existing table in database.
        
    Args:
        name (str): Table name.
        commit (bool): Commit the change if True.
    
    Returns:
        Conn: Connection object if not committing the change.
    """
    try:
        sql = f'DELETE FROM {name}'
        if commit:
            print(f"NOTE: Deleting all records in a table '{name}'.")
            execute_simple(sql, commit=True)
        else:
            return execute_simple(sql)
    except:
        raise

def drop_table(name, commit=False):
    """Drop a table with the given name from database if exists.
    
    Args:
        name (str): Table name.
        commit (bool): Commit the change if True.
    
    Returns:
        Conn: Connection object if not committing the change.
    """
    try:
        sql = f'DROP TABLE IF EXISTS {name};'

        if commit:
            print(f"NOTE: Dropping a table '{name}'.")
            execute_simple(sql, commit=True)
        else:
            return execute_simple(sql)
    except:
        raise

def append_table_to_another(name_from, name_to, commit=False):
    """Append one table to another table.
    
    Args:
        name_from (str): Table containing data.
        name_to (str): Table to append data to.
        commit (bool): Commit the change if True.
    
    Returns:
        Conn: Connection object if not committing the change.
    """
    try:
        sql = f'INSERT INTO {name_to} SELECT * FROM {name_from};'
        
        if commit:
            print(f"NOTE: Appending records in a table '{name_from}' to another table '{name_to}'.")
            execute_simple(sql, commit=True)
        else:
            return execute_simple(sql)
    except:
        raise