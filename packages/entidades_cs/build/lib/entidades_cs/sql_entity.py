from .entity import Entity
from mssql_cs import DB


class SQLEntity(Entity):
    # Describe el modelo de datos
    # de una entidad SQL

    # Conexión sql
    def __init__(self, table: str = None, fields: list = None) -> None:
        #

        #
        if table != None:
            self.table = table
        super().__init__(fields)
        self._conn = DB()

    # Tabla
    table = None

    # ConsultaSQL
    query = None

    def selectQuery(self) -> str:
        if self.query != None:
            return self.query

        # Se construye una consulta SOQL
        query = 'SELECT '

        if len(self.fields) > 1:
            query += ', '.join(self.fields)
        elif len(self.fields) == 1:
            query += self.fields[0]
        else:
            query += '*'

        if self.table == None:
            raise Exception('No se ha asignado una entidad')

        query += ' FROM ' + self.table

        #
        # Para futuras versiones incluir comprobación de filtros
        #
        return query

    def _fill_data(self) -> None:
        dataframe = self._conn.query(self.selectQuery(), self.fields)

        if self.data_limit != None:
            dataframe = dataframe.take(self.data_limit)

        self._data = dataframe
