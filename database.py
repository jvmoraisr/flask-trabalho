import sqlite3

class Database:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def execute_query(self, query, params=(), commit=False):
        conn = self.get_connection()
        if not conn:
            return None
        try:
            cur = conn.cursor()
            cur.execute(query, params)
            if commit:
                conn.commit()
            result = cur.fetchall() if not commit else None
            return result
        except sqlite3.Error as e:
            print(f"Erro ao executar a query: {e}")
            return None
        finally:
            conn.close()
