import pandas as pd

from database.conn import Conn

def check_input_format(df):
    """Return True if a user input is in the correct format."""
    conn = Conn()
    target = pd.read_sql_query(f'SELECT * FROM Data LIMIT 1;', conn.self())
    conn.close()
    
    input_columns = df.columns.tolist()
    target_columns = target.columns.tolist()

    if isinstance(df, pd.DataFrame) and input_columns == target_columns:
        return True
    else:
        raise AssertionError("ERROR: Incorrect user input format.")