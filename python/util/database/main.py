import datetime
import re

from util.database.misc import execute_simple, exist_table, is_valid_temp_name
from util.database.dbread import read_table, read_table_names
from util.database.dbwrite import (append_table_to_another, create_table,
    delete_from_table, drop_table, insert_into_table)

def create_temp(df, name_temp):
    """Create temporary table in the database from input.

    Args:
        df (pandas DataFrame): Data input.
        name_temp (str): Name of the temporary table.

    """
    try:
        is_valid_temp_name(name_temp)
        create_table(df, name_temp, commit=True)
        insert_into_table(df, name_temp, commit=True)
        
        print(f"NOTE: Successfully created a temporary table '{name_temp}'.")
    except:
        msg = f"ERROR: Cannot create a temporary table '{name_temp}'."
        raise ValueError(msg)

def drop_temp(name_temp=None):
    """Drop a temporary table after added to the master table.

    Args:
        name_temp (str): Name of the temporary table to drop. Optional.
            If None, all tables with "Temp" in name will be dropped.

    """
    try:
        if name_temp == None:
            pattern = re.compile('^Temp[A-Z][a-z]+')
            table_names = read_table_names()
            for name in table_names:
                if pattern.match(name):
                    drop_table(name, commit=True)
                    print(f"NOTE: Successfully removed from database a temporary table '{name}'.")
        else:
            if exist_table(name_temp, f"Cannot find a temporary table '{name_temp}'"):
                drop_table(name_temp, commit=True)
                print(f"NOTE: Successfully removed from database a temporary table '{name_temp}'.")
    except:
        raise

def update_date_updated(id):
    """Update the updated date field in the Dataset table."""
    try:
        date = datetime.date.today().strftime('%Y-%m-%d')
        sql = f'UPDATE Dataset SET date_updated = "{date}" WHERE id = {id};'

        execute_simple(sql, commit=True)

        print(f"NOTE: Successfully updated date_updated value to {date} in Dataset {id}.")
    except:
        raise

def update_dataset_years(pop=False):
    """Update year field values in the Dataset table using the current records."""
    try:
        dataset = read_table('Dataset')
        dataset_new = dataset.copy()
        
        def update_years(year, id):
            year_min = year.min()
            year_max = year.max()

            dataset_new.loc[dataset_new['id'] == id, 'year_min'] = year_min
            dataset_new.loc[dataset_new['id'] == id, 'year_max'] = year_max
        
        if pop:
            id = 900
            year = read_table('BridgePop')['year']
            update_years(year, id)
        else:
            list_id = dataset_new['id'].unique().tolist()
            data = read_table('Data')
            variable = read_table('Variable')
            for id in list_id:
                vars = variable.loc[variable['fk_variable_dataset'] == id, 'id'].tolist()
                year = data.loc[data['fk_data_variable'].isin(vars), 'year']
                update_years(year, id)

        delete_from_table('Dataset', commit=True)
        insert_into_table(dataset_new, 'Dataset', commit=True)

        print("NOTE: Successfully updated year values in Dataset.")
    except:
        raise

def update_table_with_temp(name_temp, name_perm):
    """Update data in a permanent table with data in a temporary table.

    Args:
        name_temp (str): Name of a temporary table.
        name_perm (str): Name of a permanent table.
    
    """
    try:
        names = read_table_names()
        if name_temp not in names:
            print(f"ERROR: Cannot find a temporary table '{name_temp}'.")
        elif name_perm not in names:
            print(f"ERROR: Cannot find a permanent table '{name_perm}'.")
        else:
            if name_temp == f'Temp{name_perm}':
                append_table_to_another(name_temp, name_perm, commit=True)
            else:
                print("ERROR: Mismatch between temporary and permanent tables.")
                raise ValueError
    except:
        raise