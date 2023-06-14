import pandas
from helpers_cs import each


class Entity:
    # Describe el modelo de datos
    # de una entidad

    # Variable campos
    fields = []

    # Datos
    _data = None
    data_limit = None

    # Filtros
    _scopeFilters = {}

    # Constructor
    def __init__(self, fields: list = None) -> None:
        if fields != None:
            self.fields = fields

    # Completar datos
    def fill(self, data: dict | pandas.DataFrame) -> None:
        self._data = data

    # Obtener campos
    def getFields(self) -> list:
        return self.fields

    # Obtener datos (Debe implementarse)
    def _fill_data(self) -> None:
        pass

    # Función de datos
    def all(self) -> pandas.DataFrame:

        #
        if self._data == None:
            self._fill_data()

        # Apply filters
        for field, callback in self._scopeFilters.items():
            self._data = each(self._data, field, callback)
        return self._data
