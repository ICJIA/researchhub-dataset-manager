import re

from util.database.conn import Conn
from util.database.dbread import read_table_names

def execute_simple(sql, commit=False):
    """Simplify execution of a SQL commend.
    
    Args:
        sql (str): SQL to run. 
        commit (bool): Commit change if True.

    Returns:
        Conn: Connection object if not committing the change.
    """
    try:
        conn = Conn()
        conn.execute(sql)
        
        if commit:
            conn.commit()
            conn.close()
        else:
            return conn
    except:
        raise

def exist_table(name, msg):
    """Check if a table with the given name exists.
    
    Args:
        name (str): Table name to check. 
        msg (str): Error message.

    Returns:
        bool: True for success, False otherwise.
    """
    try:
        if name in read_table_names():
            return True
        else:
            raise ValueError(msg)
    except:
        raise

def get_type_sqlite(type_py):
    """Return SQLite data type translated from Python data type."""
    dict_type = {
        'int64': 'INTEGER',
        'float64': 'REAL',
        'str': 'TEXT'
    }
    
    return dict_type.get(type_py, 'BLOB')

def is_valid_temp_name(name_temp):
    """Return True if temporary table name is valid. Otherwise return False."""
    pattern = re.compile("^Temp[A-Z][a-z].*")
    names = read_table_names()
    
    if pattern.match(name_temp) and (name_temp[4:] in names):
        return True
    else:
        msg = "ERROR: Invalid temporary table name." +\
            "Must start with 'Temp', followed by the permanent table name."
        raise ValueError(msg)
