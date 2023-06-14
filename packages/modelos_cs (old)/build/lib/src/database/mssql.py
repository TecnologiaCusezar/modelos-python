import pandas as pd
import pyodbc
from ..config.config import Config

class DB:
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=' + Config.get("MSSQL_SERVER") + ';'
                      'Database=' + Config.get("MSSQL_DATABASE") + ';'
                      'UID=' + Config.get("MSSQL_USER") + ';'
                      'PWD=' + Config.get("MSSQL_PASSWORD") + ';')
    def query(self, Query, Columns):
        return pd.DataFrame(pd.read_sql_query(Query, self.conn), columns=Columns)


