"""Offer functions for interacting with the SQL database.

This module offer functions to interact with the database file, ``database.db``,
in the ``@/database``. The module is intended to be imported and used by other
modules rather than directly imported by the main program.

The module contains the following public functions to be called externally:

``init()`` establishes connection to a SQLite database, ``@/database/database.db``.
``close()`` closes database connection.
``commit()`` commits changes to the database.
``execute_simple_sql`` runs a simple sequel query without returning any output.
``fetch_table()`` fetches a table from the database.
``create_temp()``creates a temporary table.
``add_to_master()``appends a temporary table to the master table.
``delete_temp()`` deletes a temporary table.
"""
import pandas as pd
import re
import sqlite3

def init():
    """Initialize module and connect to database."""
    global CONN
    CONN = sqlite3.connect('P:\\DATA\\CJIA_WebData\\database\\database.db')

def close():
    """Close database connection."""
    global CONN
    CONN.close()

def commit():
    """Commit changes."""
    global CONN
    CONN.commit()

def _get_type_sqlite(type_py):
    """Return SQLite data type translated from Python data type."""
    if type_py == 'int64':
        return 'INTEGER'
    elif type_py == 'float64':
        return 'REAL'
    elif type_py == 'str':
        return 'TEXT'
    else:
        return 'BLOB'

def execute_simple_sql(sql):
    """Execute simple sql command."""
    global CONN

    try:
        c = CONN.cursor()
        c.execute(sql)
        c.close()
    except:
        sql_to_print = sql if len(sql) < 100 else f'{sql[:80]}...(omitted)...{sql[-10:]}'
        print(f'ERROR: Failed SQL query attempt: "{sql_to_print}"')
        raise


def _create_table(df, name):
    """Create an empty table in database if not exists.
    
    Args:
        df (pandas DataFrame): Data input to define columns.
        name (str): New table name.
    """
    colnames = list(df)
    coltypes_py = [type(df[colname].iat[0]).__name__ for colname in colnames]
    coltypes = [_get_type_sqlite(i) for i in coltypes_py]
    
    sql_columns = ''
    for i in range(len(colnames)):
        sql_columns += f'{colnames[i]} {coltypes[i]}'
        if i < len(colnames) - 1:
            sql_columns += ', '
    sql = f'CREATE TABLE IF NOT EXISTS {name} ({sql_columns})'
    
    try:
        execute_simple_sql(sql)
    except:
        raise

def _insert_to_table(df, name):
    """Insert data to an existing table in database.
        
    Args:
        df (pandas DataFrame): Data input.
        name (str): Table name.
    """
    global CONN
    
    columns = ', '.join(list(df))
    params = ', '.join(['?' for i in range(len(list(df)))])
    sql = f'INSERT INTO {name} ({columns}) VALUES ({params});'
   
    try:
        c = CONN.cursor()
        c.executemany(sql, list(df.itertuples(index=False, name=None)))
        c.close()
    except:
        sql_to_print = sql if len(sql) < 100 else f'{sql[:80]}...(omitted)...{sql[-10:]}'
        print(f'ERROR: Failed SQL query attempt: "{sql_to_print}"')
        raise

def _create_and_insert_to_table(df, name):
    """Create and insert data to a table.
    
    Args:
        df (pandas DataFrame): Data input.
        name (str): Table name.
    """
    try:
        _create_table(df, name)
        _insert_to_table(df, name)
    except:
        raise

def fetch_table(name):
    """Return a table with the given name from database as a pandas DataFrame.
    
    Args:
        name (str): Table name.
    
    Returns:
        pandas DataFrame: Table from database.
    """
    global CONN
    sql = f'SELECT * FROM {name};'

    try:
        return pd.read_sql(sql, CONN)
    except:
        print(f'ERROR: Failed SQL query attempt: "{sql}"')
        raise

def fetch_tables(name_list=None):
    """Return a list of tables with the given names fetched from database, each as a pandas.DataFrame.

    This function returns a list of tables fetched from database.
    For efficiency, if a table already exists in the environment as an object,
    the function simply uses the existing object instead of fetching the table
    anew from the database.
    
    Args:
        name_list (list): List of table names to fetch.
    
    Returns:
        list: List of pandas.DataFrame objects of tables from database.
    """
    try:
        name_dict = {
            'County': 'county',
            'CombinedCounty': 'combined_county',
            'Indicator': 'indicator',
            'Population': 'population',
            'PopulationOld': 'population_old',
            'SimpleCount': 'simplecount',
            'Output': 'output',
            'Package': 'package'
        }

        if name_list == None:
            name_list = [
                'County',
                'CombinedCounty',
                'Indicator',
                'Population',
                'PopulationOld',
                'SimpleCount',
                'Output',
                'Package'
            ]
        
        table_list = []
        for name in name_list:
            varname = name_dict[name]
            if varname in locals():
                table_list.append(locals()[varname])
            elif varname in globals():
                table_list.append(globals()[varname])
            else:
                table_list.append(fetch_table(name))
        return table_list
    except:
        raise

def _append_to_another_table(name_from, name_to):
    """Append one table to another table."""
    try:
        execute_simple_sql(f'INSERT INTO {name_to} SELECT * FROM {name_from};')
    except:
        raise

def _delete_table(name):
    """Delete a table with the given name from database if exists."""
    try:
        execute_simple_sql(f'DROP TABLE IF EXISTS {name};')
    except:
        raise

def _get_table_names():
    """Return a list of existing table names in database."""
    global CONN
    sql = "SELECT name FROM sqlite_master WHERE type='table';"

    try:
        c = CONN.cursor()
        names = c.execute(sql).fetchall()
        c.close()
        return [i[0] for i in names]
    except:
        print(f'ERROR: Failed SQL query attempt: "{sql}"')
        raise

def _check_table_name(name, msg):
    """Check if a table with the given name exists.
    
    Args:
        name (str): Table name to check. 
        msg (str): Error message.

    Returns:
        bool: True for success, False otherwise.
    """
    try:
        if name in _get_table_names():
            return True
        else:
            raise ValueError(msg)
    except:
        raise

def validate_temp_table_name(name_temp):
    """Return True if temporary table name is valid. Otherwise return False."""
    pattern = re.compile("^Temp[A-Z][a-z].*")
    table_names = _get_table_names()
    if pattern.match(name_temp) and (name_temp[4:] in table_names):
        return True
    else:
        raise ValueError('ERROR: Invalid temporary table name. Name must start with "Temp", followed by its master table name.')

def create_temp(df, name_temp):
    """Create temporary table in the database from input.

    Args:
        df (pandas DataFrame): Data input.
        name_temp (str): Name of the temporary table.

    """
    try:
        validate_temp_table_name(name_temp)
        _create_and_insert_to_table(df, name_temp)
        commit()
        print(f'NOTE: "{name_temp}" is successfully generated in database.')
    except:
        raise ValueError(f'ERROR: Cannot create a temporary table with the given name: {name_temp}.')
    
def add_to_master(name_temp, name_master):
    """Append data in a temporary table to an existing `master` table.

    Args:
        name_temp (str): Name of the temporary table.
        name_master (str): Name of the master table.
    
    """
    try:
        table_names = _get_table_names()
        if name_temp not in table_names:
            print('ERROR: No temporary table found with the given name.')
        elif name_master not in table_names:
            print('ERROR: No master table found with the given name.')
        else:
            if name_temp != f'Temp{name_master}':
                print('ERROR: Mismatch between temporary and master tables.')
            else:
                _append_to_another_table(name_temp, name_master)
                commit()
    except:
        raise

def delete_temp(name_temp=None):
    """Delete a temporary table after added to the master table.

    Args:
        name_temp (str): Name of the temporary table to delete. Optional.
            If None, all tables with "Temp" in name will be deleted.

    """
    try:
        if name_temp == None:
            pattern = re.compile("^Temp[A-Z][a-z]+")
            table_names = _get_table_names()
            for name in table_names:
                if pattern.match(name):
                    _delete_table(name)
                    commit()
                    print(f'NOTE: "{name}" is successfully removed from database.')
        else:
            if _check_table_name(name_temp, 'No temporary table found with the given name.'):
                _delete_table(name_temp)
                commit()
                print(f'NOTE: "{name_temp}" is successfully removed from database.')
    except:
        raise
    
def update_output_years(pop=False):
    """Update year columns in Output table based on the current records."""
    try:
        output = fetch_tables(['Output'])[0]
        data = output.copy()
        
        def helper(year, id):
            year_min = year.min()
            year_max = year.max()

            data.loc[data['id'] == id, 'year_min'] = year_min
            data.loc[data['id'] == id, 'year_max'] = year_max
        
        if pop:
            year = fetch_tables(["Population"])[0]['year']
            helper(year, 25)
        else:
            id_list = data['id'].unique().tolist()
            indicator, simplecount = fetch_tables(['Indicator', 'SimpleCount'])
            for id in id_list:
                ind_list = indicator.loc[indicator['fk_indicator_output'] == id, 'id'].tolist()
                year = simplecount.loc[simplecount['fk_simplecount_indicator'].isin(ind_list), 'year']
                helper(year, id)

        _delete_table("Output")
        _create_and_insert_to_table(data, "Output")
        commit()

        print('NOTE: Year values are successfully updated.')
    except:
        raise
    

