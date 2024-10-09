import os
import pyodbc
from lib.custom_exceptions import DatabaseError, DatabaseQueryError


class SQLServerAccessor:
    def __init__(self):
        self.driver = os.getenv('SQL_SERVER_DRIVER')
        self.server = os.getenv('SQL_SERVER_SERVER')
        self.port = os.getenv('SQL_SERVER_PORT')
        self.database = os.getenv('SQL_SERVER_DATABASE')
        self.user = os.getenv('SQL_SERVER_USER')
        self.password = os.getenv('SQL_SERVER_PASSWORD')

        if not all([self.driver, self.server, self.port, self.database, self.user, self.password]):
            raise ValueError("すべてのDB接続情報が環境変数に設定されている必要があります。")

    def __enter__(self):
        try:
            self.conn = pyodbc.connect(f"DRIVER={self.driver};SERVER={self.server},{self.port};DATABASE={self.database};UID={self.user};PWD={self.password}")
            print("DB接続しました。")
            self.cursor = self.conn.cursor()
            return self
        except Exception as ex:
            raise DatabaseError(f"DB接続で予期しないエラーが発生しました。: {ex}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            print("DB切断しました。")
            self.cursor.close()
            self.conn.close()
        except Exception as ex:
            raise DatabaseError(f"DB切断で予期しないエラーが発生しました。: {ex}")

    def _fetchall_as_dict(self, cursor):
        columns = [column[0].lower() for column in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self._fetchall_as_dict(self.cursor)
        except Exception as ex:
            raise DatabaseQueryError(f"クエリ({query})実行中にエラーが発生しました。: {ex}")
