import pandas
import tempfile
import hashlib
import os
import helpers_cs
import time
import datetime


class Entity:
    # Describe el modelo de datos
    # de una entidad

    # Variable campos
    fields = []

    # Datos
    _data = None
    data_limit = None
    __cached_data: bool = False
    __cached_data_prefix: str = None

    # Filtros
    _scopeFilters = {}

    # Constructor
    def __init__(self, fields: list = None, caching_data: str = 'd') -> None:
        if fields != None:
            self.fields = fields

        if caching_data[0] == "m":
            prefix_pattern = "%Y%m"
        elif caching_data[0] == "y":
            prefix_pattern = "%Y"
        else:
            # caching_data[0] == "d"
            prefix_pattern = "%Y%m%d"
        self.__cached_data_prefix = datetime.datetime.now().strftime(prefix_pattern)

    # Completar datos
    def fill(self, data: dict | pandas.DataFrame) -> None:
        self._data = data

    # Obtener campos
    def getFields(self) -> list:
        return self.fields

    # Obtener datos (Debe implementarse)
    def _fill_data(self) -> None:
        pass

    # Cargar información si no existe en el sistema
    def __load_data(self) -> None:
        # Identifica a los datos mediante una firma
        temp_file_path = './.__cached_python_entities/' + self.__cached_data_prefix + '/'
        temp_file = helpers_cs.path(
            temp_file_path + self._signature() + '.json')

        # No hay datos en cache
        if os.path.exists(temp_file):
            # Carga de datos en archivo
            file = open(temp_file, 'r')
            self._data = pandas.read_json(file.read())
        else:
            # Carga de información
            self._fill_data()

            # Creación de directorio
            os.makedirs(temp_file_path, exist_ok=True)

            # Creación de archivo
            with open(temp_file, 'w') as f:
                f.write(self._data.to_json())

    # Algoritmo de firma de objeto
    def _signature(self) -> str:
        return "entity"

    # Función de datos
    def all(self) -> pandas.DataFrame:

        #
        if self._data == None:
            self.__load_data()

        # Apply filters
        for field, callback in self._scopeFilters.items():
            self._data = helpers_cs.each(self._data, field, callback)
        return self._data
