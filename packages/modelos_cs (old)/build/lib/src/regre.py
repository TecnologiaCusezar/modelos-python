import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def mapear_datos_de_entrenamiento_y_prueba(x, y):
    x_entrenamiento, x_prueba, y_entrenamiento, y_prueba = train_test_split(x, y)
    return (x_entrenamiento, x_prueba, y_entrenamiento, y_prueba)

def modelo_regresion_lineal(x, y) -> LinearRegression:
    reg = LinearRegression()
    reg.fit(x,y)
    return reg

def estimar_coeficientes(x, y):
    # número de observaciones
    n = np.size(x)
  
    # promedio de vectores (x) y (y)
    m_x = np.mean(x)
    m_y = np.mean(y)
  
    # desviación cruzada y desviación estánda con respecto a (x)
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
  
    # coeficientes de regresion
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
  
    return (b_0, b_1)
  
def plot_regresion_lineal(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color = "m",
               marker = "o", s = 30)
  
    # predicted response vector
    y_pred = b[0] + b[1]*x
  
    # plotting the regression line
    plt.plot(x, y_pred, color = "g")
  
    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')
  
    # function to show plot
    plt.show()