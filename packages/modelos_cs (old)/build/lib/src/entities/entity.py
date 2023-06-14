from ..database.mssql import DB
import pandas
import helpers

## Describe el modelo de datos
# de una entidad
class Entity:

    ## Variable campos
    fields = []

    ## Datos
    _data = pandas.DataFrame()

    ## Filtros
    _scopeFilters = {}

    ## Constructor
    def __init__(self, fields: list) -> None:
        self.fields = fields

    ## Completar datos
    def fill(self, data: dict|pandas.DataFrame)->None:
        self._data = data

    ## Obtener campos
    def getFields(self)->list:
        return self.fields
    
    ## Obtener datos (Debe implementarse)
    def _fill_data(self, limit: int) -> None:
        pass
    
    ## Función de datos
    def all(self) -> pandas.DataFrame:
        ## Apply filters
        for field, callback in self._data.items():
            self._data = helpers.each(self._data, field, callback)
        return self._data

## Describe el modelo de datos
# de una entidad SQL
class SQLEntity(Entity):
    
    ## ConsultaSQL
    query = ""

    def _fill_data(self, limit: int) -> None:
        self._data = DB().query(self.query, self.fields).take(limit)


    

    