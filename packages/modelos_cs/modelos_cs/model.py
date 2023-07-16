from pandas import DataFrame
from pandas import read_parquet
from pandas import Series
from .coefficient import Coefficient
from enum import Enum
import pandas
import importlib
import inspect
import helpers_cs
import os
import json


class Model:
    # Esta clase describe un modelo
    # probabilístico serializable

    #
    # Funciones modelo
    #

    def predict(self, data: any) -> any:
        # Realiza la predicción en base a los datos del modelo
        pass

    #
    # Metadatos del modelo
    #

    # Nombre del adaptador
    driver: str = None

    def getDriver(self) -> str:
        # Obtiene el nombre del modelo
        return self.driver

    # Nombre del modelo
    name: str = None

    def getName(self) -> str:
        # Obtiene el nombre del modelo
        return self.name

    # Firma del modelo
    sign: str = None

    def getSign(self) -> str:
        # Obtiene la firma del modelo
        if self.sign == None:
            self.sign = self.getName() + '-' + self.getDriver()
        return self.sign

    # Modelo
    model: any = None

    def getModel(self) -> any:
        # Obtiene el operador del modelo
        return self.model

    #
    model_params: dict = None

    def getModelParams(self) -> dict:
        # Obtiene los parámetros del modelo
        return self.model_params

    #
    coefficients: list = None

    def getCoefficients(self) -> list:
        # Obtiene estimadores
        return self.coefficients

    #
    # Procesamiento de datos
    #

    # Variable endógena
    endogenous: list[str] = None

    def getEndogenous(self) -> list[str]:
        # Obtiene la variable endógena
        return self.endogenous

    # Variables exógenas
    exogenous: list[str] = None

    def getExogenous(self) -> list[str]:
        # Obtiene la variable endógena
        return self.exogenous

    #
    # Archivo de datos
    #

    # Datos
    data: DataFrame = None

    def getData(self) -> DataFrame:
        # Obtiene la ruta del archivo de datos
        return self.data

    def filterData(self, dataframe: DataFrame) -> DataFrame:
        # Modifica la variable {self.data}
        return dataframe

    def storeData(self) -> None:
        # Convierte el modelo en texto json
        self.getData().to_parquet(self.getDataFilePath())

    def loadData(self) -> None:
        # Convierte el modelo json en instancia de clase
        self.data = self.filterData(read_parquet(self.getDataFilePath()))

    # Ruta del archivo de datos
    data_file_path: str = None

    def getDataFilePath(self) -> str:
        # Obtiene la ruta del archivo de datos
        if self.data_file_path == None:
            # Asignar
            self.data_file_path = helpers_cs.path(
                './datasets/' + self.getSign() + self.getDataFileExtension())
            # Creación de directorio
            os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
            if not os.path.exists(self.data_file_path):
                self.data_file_path = helpers_cs.path(
                    './datasets/' + self.getName() + self.getDataFileExtension())
                if not os.path.exists(self.data_file_path):
                    raise Exception('No existe el archivo con los datos')

        return self.data_file_path

    # Extension del archivo de datos
    data_file_extension: str = None

    def getDataFileExtension(self) -> str:
        # Obtiene la extensión del archivo de datos
        if self.data_file_extension == None:
            self.data_file_extension = ".parquet"
        return self.data_file_extension

    #
    # Archivo de modelo
    #

    # Representación del archivo de configuración
    __config: dict = None

    def config(self, key: str = None, default: any = None) -> dict:
        # Obtiene el valor de configuración
        if key == None:
            return self.getConfig()
        return self.__config.get(key, default)

    def setConfig(self) -> None:
        self.driver = self.config('driver', self.driver)
        self.params = self.config('params', self.params)
        self.name = self.config('name', self.name)
        self.data_file_path = self.config('data', self.data_file_path)
        self.coefficients = self.config('coefficients', self.coefficients)
        self.endogenous = self.config('endogenous', self.endogenous)
        self.exogenous = self.config('exogenous', self.exogenous)

    def getConfig(self) -> dict:
        return {
            'driver': self.getDriver(),
            'params': self.getModelParams(),
            'name': self.getName(),
            'data': self.getDataFilePath(),
            'coefficients': self.getCoefficients(),
            'endogenous': self.getEndogenous(),
            'exogenous': self.getExogenous(),
        }

    def storeConfig(self) -> None:
        # Convierte el modelo en texto json
        with open(self.getConfigFilePath(), 'w') as file:
            file.write(json.dumps(self.config()))

    def loadConfig(self) -> None:
        # Convierte el modelo json en instancia de clase
        if os.path.exists(self.getConfigFilePath()):
            file = open(self.getConfigFilePath(), 'r')
            file_content = file.read()
            if len(file_content) > 3:
                self.__config = json.loads(file_content)
                self.setConfig()

    # Ruta del archivo del modelo
    config_file_path: str = None

    def getConfigFilePath(self) -> str:
        # Obtiene la ruta del archivo del modelo
        if self.config_file_path == None:
            # Asignar
            self.config_file_path = helpers_cs.path(
                './' + self.getSign() + self.getConfigFileExtension())

        return self.config_file_path

    # Extension del archivo de datos
    config_file_extension: str = None

    def getConfigFileExtension(self) -> str:
        # Obtiene la extensión del archivo de datos
        if self.config_file_extension == None:
            self.config_file_extension = ".model.json"
        return self.config_file_extension

    #
    # Comportamiento
    #

    def __init__(self, **kwargs):
        # Instanciar clase con argumentos
        for property, value in kwargs.items():
            setattr(self, property, value)

        # Cargar modelo existente
        self.loadConfig()

        #
        self.loadData()

        # Función de boot
        self.boot()

    def boot(self) -> None:
        pass
