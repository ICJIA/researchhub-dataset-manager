from pathlib import Path
import sqlite3

class Conn:
    def __init__(self, path='database/database.db'):
        self.path = str(Path(path))
        self.conn = sqlite3.connect(self.path)
        self.crsr = None
    
    def self(self):
        return self.conn
    
    def cursor(self):
        if self.crsr is None:
            self.crsr = self.conn.cursor()
        return self.crsr

    def execute(self, sql):
        try:
            if self.crsr is None:
                self.crsr = self.conn.cursor()
            return self.crsr.execute(sql)
        except:
            msg = sql if len(sql) < 100 else f'{sql[:80]}...(omitted)...{sql[-10:]}'
            print(f'ERROR: Failed SQL query attempt: "{msg}"')
            raise

    def commit(self):
        self.conn.commit()
    
    def close(self):
        if self.crsr is not None:
            self.crsr.close()
        self.conn.close()
    
    def __str__(self):
        return self.conn.__str__()

    def __repr__(self):
        return self.conn.__repr__()