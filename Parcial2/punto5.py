import os
import sys
# Añade el directorio padre (dos niveles arriba o ajustando los niveles) a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.functions import *
from functions.functions2 import *

# - - - - - - - - - - - - PARCIAL 2 - - - - - - - - - - - -

entrada = "10111101100111101000001010100101"
salida = "GGHHIIGHGFFGIIFGHGGGGFGGFGGFGFFG"

print("prob a priori de 0: ", probabilidadesTexto(entrada)["0"])    #las de toda la vida
print("prob a priori de 1: ", probabilidadesTexto(entrada)["1"])

mostrarMatrizCanal(entrada, salida)

mat = generarMatrizCanal(entrada, salida)

print("clasificacion del canal: ", clasificarCanal(mat))

print("H(A/B) (equivocacion): ", equivocacionCanal(mat, entrada))

print("H(B/A) (perdida): ", perdidaCanal(mat, entrada))

print("I(A,B) (informacion mutua): ", informacionMutua(mat, entrada))

mostrarMatrizReducida(entrada, salida)

capacidadYMaxX = capacidadCanal2x2(matrizReducida(entrada, salida))

print("capacidad del canal reducido: ", capacidadYMaxX[0])

print("P(0): ", capacidadYMaxX[1])

print("P(1): ", capacidadYMaxX[2])

print("P(e) (prob de error): ", probabilidadError(mat, entrada))