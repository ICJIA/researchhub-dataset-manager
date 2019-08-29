from util.data.bridgepop import prepare_bridgepop_data
from util.data.chri import prepare_chri_data
from util.data.idjj import prepare_idjj_data
from util.data.idoc import prepare_idoc_data
from util.data.jail import prepare_jail_data
from util.data.laus import prepare_laus_data
from util.data.sapie import prepare_poverty_data
from util.data.ucr import dict_ucr_variable, prepare_ucr_data

from util.database.conn import Conn
from util.database.main import create_temp, drop_temp, update_table_with_temp
from util.fs.main import read_data, delete_temp, write_temp

def __read_data_auto(source):
    dict_source = {
        'chri': ('Criminal History', prepare_chri_data),
        'idjj': ('Juvenile Court', prepare_idjj_data),
        'idoc': ('Prison', prepare_idoc_data),
        'jail': ('Jail', prepare_jail_data),
        'employment': ('Employment', prepare_laus_data),
        'poverty': ('Poverty', prepare_poverty_data),
        'ucr': ('Uniform Crime Report', prepare_ucr_data)
    }

    print(f"WAIT: Preparing {dict_source[source][0]} data...")
    
    return dict_source[source][1]()

def __delete_bridgepop_old_records():
    """Delete from `BridgePop` records to be outdated due to update."""
    try:
        name_perm = 'BridgePop'
        name_temp = 'Temp' + name_perm

        conn = Conn()
        cursor = conn.cursor()
        
        year_min_t, year_max_t = cursor \
            .execute(f'SELECT MIN(year), MAX(year) FROM {name_temp};') \
            .fetchone()
        
        year_max_m, = cursor \
            .execute(f'SELECT MAX(year) FROM {name_perm};') \
            .fetchone()

        if year_max_t <= year_max_m:
            raise ValueError("ERROR: BridgePop table is already up-to-date!")
        else:
            sql = f'DELETE FROM {name_perm} WHERE year BETWEEN {year_min_t} AND {year_max_t};'
            conn.execute(sql)
            conn.commit()

        conn.close()
    except:
        raise

def __delete_ucr_old_records():
    """Delete from `Data` old, uncorrected UCR values."""
    try:
        
        conn = Conn()
        cursor = conn.cursor()
        
        sql = f'SELECT max(year) FROM Data WHERE fk_data_variable = 50000'
        year, = cursor \
            .execute(sql) \
            .fetchone()
        
        ucr_var = ', '.join([str(x) for x in dict_ucr_variable.values()][:-1])
        sql = f'DELETE FROM Data WHERE year = {year} AND fk_data_variable IN ({ucr_var})'
        cursor.execute(sql)
        
        print("NOTE: Uncorrected UCR data values are removed from the database prior to inserting the corrected values.")

        conn.commit()
        conn.close()
    except:
        raise

def create_temp_bridgepop():
    try:
        df = prepare_bridgepop_data()
        name = 'TempBridgePop'

        create_temp(df, name)
        write_temp(df, name)

        return True
    except:
        raise

def create_temp_data(source=None, auto=False):
    try:
        df = __read_data_auto(source) if auto else read_data()
        name = 'TempData'
        
        create_temp(df, name)
        write_temp(df, name)
        
        return True
    except:
        raise

def remove_old_ucr_values():
    try:
        pass
    except:
        raise

def update_bridgepop():
    try:
        name_perm = 'BridgePop'
        name_temp = 'Temp' + name_perm

        __delete_bridgepop_old_records()
        update_table_with_temp(name_temp, name_perm)
        drop_temp(name_temp)
        return True
    except Exception as e:
        print(e)
        return False

def update_data(source=None):
    try:
        name_perm = 'Data'
        name_temp = 'Temp' + name_perm

        if source == 'ucr':
            __delete_ucr_old_records()

        update_table_with_temp(name_temp, name_perm)
        drop_temp(name_temp)
        delete_temp()
        return True
    except Exception as e:
        print(e)
        return False

def write_datasets_in_group(group):
    try:
        return True
    except Exception as e:
        print(e)
        return False