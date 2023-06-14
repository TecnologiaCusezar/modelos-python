from .entity import Entity
from helpers_cs import resolve_env
from helpers_cs import to_json
import requests
import pandas as pd


class SalesforceEntity(Entity):
    # Describe el modelo de datos
    # de una entidad SQL

    # Variables de conexión
    _protocol = 'https'
    _tenant = 'env:SALESFORCE_TENANT'

    # Parámetros de autenticación
    _auth = dict(
        path='/services/oauth2/token',
        params=dict(
            grant_type='env:SALESFORCE_GRANT_TYPE',
            client_id='env:SALESFORCE_CLIENT_ID',
            client_secret='env:SALESFORCE_CLIENT_SECRET',
            username='env:SALESFORCE_USERNAME',
            password='env:SALESFORCE_PASSWORD'
        )
    )

    # Almacena el token de acceso para futuras solicitudes
    _access_token = None

    # Entidad en Salesforce
    entityName: str = None

    # Consulta SOQL
    soql_path = '/services/data/v52.0/query?&q='
    soql_query = None

    def __init__(self, entity: str = None, fields: list = None) -> None:
        # Instancia el servicio de salesforce

        #
        if entity != None:
            self.entityName = entity
        super().__init__(fields)

        #
        params_array = []
        for param, value in self._auth['params'].items():
            params_array.append(param + '=' + resolve_env(value))
        params = '&'.join(params_array)

        #
        login_endpoint = self.getBaseUrl() + self._auth['path'] + '?' + params
        response_object = self.invoke_request(login_endpoint, 'post')

        #
        if 'access_token' not in response_object:
            raise Exception(
                'Error de autenticación - Detalles:' + to_json(response_object))

        self._access_token = response_object['access_token']

    def getQuery(self) -> str:
        if self.soql_query != None:
            return self.soql_query

        #
        require_limit: bool = False

        # Se construye una consulta SOQL
        query = 'SELECT '

        if len(self.fields) > 1:
            query += ', '.join(self.fields)
        elif len(self.fields) == 1:
            query += self.fields[0]
        else:
            query += 'FIELDS(ALL)'
            require_limit = True

        if self.entityName == None:
            raise Exception('No se ha asignado una entidad')

        query += ' FROM ' + self.entityName

        #
        # Para futuras versiones incluir comprobación de filtros
        #

        if self.data_limit != None or require_limit:
            query += ' LIMIT ' + str(self.data_limit or 200)

        return query

    def executeQuery(self) -> pd.DataFrame:
        endpoint = self.getBaseUrl() + self.soql_path + self.getQuery()
        return self.parse_json_result(self.invoke_request(endpoint, bearer_token=True))

    def parse_json_result(self, obj: any) -> pd.DataFrame | None:
        if 'records' not in obj:
            return None

        result = pd.json_normalize(obj.get('records'))

        if len(self.fields) == 0:
            return result
        return pd.DataFrame(result, columns=self.fields)

    def invoke_request(self, url: str, method: str = 'GET', bearer_token: bool = False) -> any:

        request = getattr(requests, method.lower())

        if bearer_token:
            response = request(
                url,
                headers={'Authorization': f'Bearer {self._access_token}'}
            )
            return response.json()

        response = request(url)
        return response.json()

    def getBaseUrl(self) -> str:
        return resolve_env(self._protocol) + '://' + resolve_env(self._tenant)

    def _fill_data(self) -> None:
        self._data = self.executeQuery()
