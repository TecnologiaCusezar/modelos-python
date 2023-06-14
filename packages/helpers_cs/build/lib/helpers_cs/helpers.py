import os
from pathlib import PurePosixPath, Path
import pandas
from dotenv import load_dotenv
import json


def path(path_string: str) -> str:
    # Verificar el sistema operativo
    if os.name == 'nt':
        # Si es Windows, convertir la ruta a sintaxis Linux
        posix_path = PurePosixPath(path_string)
        return str(Path(*posix_path.parts))
    else:
        # Si no es Windows, devolver la ruta sin cambios
        return path_string


def toString(obj: any) -> str:
    # El clásico toString()
    return str(obj)


def each(df: pandas.DataFrame, columnName: str, callback: any) -> pandas.DataFrame:
    # Ejecuta una tarea o reasigna un valor para cada elemento de una columna de un DataFrame
    df[columnName] = df[columnName].apply(callback)
    return df


path_to_env = None


def set_env_path(path_to_env_file: str):
    # Establece la ubicación del archivo de variables de entorno
    global path_to_env
    path_to_env = path(path_to_env_file)


def env(key: str, default: str | None = None) -> str | None:
    # Obtiene una variable de entorno
    global path_to_env

    if path_to_env is not None:
        load_dotenv(path_to_env)
    else:
        load_dotenv()

    return os.getenv(key, default)


def resolve_env(variable: str) -> str | None:
    # Env var resolving
    env_token = 'env:'

    #
    value = env(variable[len(env_token):])
    if env_token in variable and value != None:
        return value
    else:
        return variable


def from_json(obj: any) -> str:
    return json.dumps(obj)


def to_json(str: str) -> any:
    return json.loads(str)
