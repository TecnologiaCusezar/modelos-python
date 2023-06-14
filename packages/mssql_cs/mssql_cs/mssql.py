import pandas as pd
# import pyodbc # Deprecated (Is not safeful)
from helpers_cs import env
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import sqlalchemy as sa


class DB:
    def __init__(self) -> None:
        connection_string = """Driver={ODBC Driver 17 for SQL Server};Server=""" + env("MSSQL_SERVER") + """;Database=""" + env(
            "MSSQL_DATABASE") + """;UID=""" + env("MSSQL_USER") + """;PWD=""" + env("MSSQL_PASSWORD") + """;"""
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})

        self._engine = create_engine(connection_url)

    def query(self, query: str, columns: list = []) -> pd.DataFrame:
        with self._engine.begin() as connection:
            result = pd.read_sql_query(sa.text(query), connection)
            if len(columns) == 0:
                return result
            return pd.DataFrame(result, columns=columns)
