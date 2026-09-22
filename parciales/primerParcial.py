import os
import sys
# Añade el directorio padre (dos niveles arriba o ajustando los niveles) a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.functions import *

mensaje = ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"

#probs:
print("\n PROBABILIDADES:")
probs = probabilidadesTexto(mensaje)
print("P(,) = " + str(probs[","]))
print("P(.) = " + str(probs["."]))
print("P(:) = " + str(probs[":"]))
print("P(;) = " + str(probs[";"]))

#matriz de transicion:

def generarMatrizTrans(mensaje):
    alfabeto = GenerarAlfabeto(mensaje)
    N = len(alfabeto)
    mat = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(len(mensaje)):
        if (i != 0):
            simbolo = mensaje[i]
            AntSimbolo = mensaje[i-1]
            mat[alfabeto.index(AntSimbolo)][alfabeto.index(simbolo)] += 1

    for i in range(N):
        acumFila = sum(mat[i])
        if acumFila > 0:
            for j in range(N):
                mat[i][j] = round((mat[i][j]) / acumFila, 8)
    traspuesta = [list(fila) for fila in zip(*mat)]   #traspone la matriz

    # MOSTRAR MATRIZ
    #for charIndex in range(len(GenerarAlfabeto(mensaje))):
    #    print(alfabeto[charIndex] + " = ", traspuesta[charIndex])

    return traspuesta
print("\n MATRIZ TRANSICION:")

mat = generarMatrizTrans(mensaje)