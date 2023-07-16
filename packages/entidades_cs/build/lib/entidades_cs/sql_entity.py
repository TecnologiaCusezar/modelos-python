from .entity import Entity
from mssql_cs import DB
import hashlib


class SQLEntity(Entity):
    # Describe el modelo de datos
    # de una entidad SQL

    # Conexión sql
    def __init__(self, table: str = None, fields: list = None, query: str = None, where: str = None) -> None:
        #

        #
        self.query = query
        self.where = where

        #
        if table != None:
            self.table = table
        super().__init__(fields)
        self._conn = DB()

    # Tabla
    table = None

    # ConsultaSQL
    query = None
    where = None

    def selectQuery(self) -> str:
        if self.query != None:
            return self.query

        # Se construye una consulta SOQL
        query = 'SELECT '

        if len(self.getFields()) > 1:
            query += ', '.join(self.getFields())
        elif len(self.getFields()) == 1:
            query += self.getFields()[0]
        else:
            query += '*'

        if self.table == None:
            raise Exception('No se ha asignado una entidad')

        query += ' FROM ' + self.table

        #
        # Para futuras versiones incluir comprobación de filtros
        #
        if self.where != None:
            query += ' WHERE ' + self.where

        return query

    def _fill_data(self) -> None:
        dataframe = self._conn.query(self.selectQuery(), self.fields)

        if self.data_limit != None:
            dataframe = dataframe.take(self.data_limit)

        self._data = dataframe

    def _signature(self) -> str:
        return str(hashlib.md5(self.selectQuery().encode()).hexdigest())
