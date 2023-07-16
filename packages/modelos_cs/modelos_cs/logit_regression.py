from pandas import DataFrame, Series, read_json
from .model import Model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class LogisticModelRegression(Model):

    driver = 'logistic-regression'

    model = LogisticRegression()

    x_entrenamiento = None
    x_prueba = None
    y_entrenamiento = None
    y_prueba = None

    def getModelParams(self) -> dict:
        return self.getModel().get_params()

    def getCoefficients(self) -> list:

        if self.coefficients == None:
            exogenous_names = self.getExogenous()
            coefficients = self.getModel().coef_[0]
            intercept = self.getModel().intercept_[0]

            # Create an array of dictionaries with the required schema
            coefficients_array = []
            for i in range(len(exogenous_names)):
                coefficients_array.append({
                    'label': 'B_' + exogenous_names[i],
                    'name': exogenous_names[i],
                    'type': 'coefficient',
                    'value': coefficients[i] or 0
                })

            # Add the intercept to the list
            coefficients_array.append({
                'label': 'B_0',
                'name': 'Intercepto',
                'type': 'intercept',
                'value': intercept or 0
            })

            #
            self.coefficients = coefficients_array
        #
        return self.coefficients

    def storeData(self) -> None:
        # Convierte el modelo en texto json
        self.getData().to_json(self.getDataFilePath(), orient='records')

    def loadData(self) -> None:
        # Convierte el modelo json en instancia de clase
        self.data = self.filterData(
            read_json(self.getDataFilePath(), orient='records'))

    def getDataFileExtension(self) -> str:
        return '.json'

    def boot(self) -> None:
        if self.model_params != None:
            self.getModel().set_params(self.config('params'))

        self.x_entrenamiento, self.x_prueba, self.y_entrenamiento, self.y_prueba = train_test_split(
            self.getData()[self.getExogenous()], self.getData()[self.getEndogenous()])

        self.getModel().fit(self.x_entrenamiento, self.y_entrenamiento)
