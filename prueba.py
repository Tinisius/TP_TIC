from functions.functions import *
from functions.functions2 import *

entrada = "10111101100111101000001010100101"
salida = "GGHHIIGHGFFGIIFGHGGGGFGGFGGFGFFG"


def corregirParidad(mensaje):
    # armamos las 4 filas de 8 bits
    filas = []
    for i in range(0, len(mensaje), 8):             #por cada bloque de 8 bits
        filas.append([int(b) for b in mensaje[i:i+8]])

    lrc = filas[0]                                  #primera fila: paridad longitudinal
    datos = filas[1:]                               #resto: caracteres + bit VRC

    # filas con paridad VRC incorrecta (paridad par: la suma debe ser par)
    filasMal = []
    for i in range(len(datos)):                     #por cada FILA de datos
        if sum(datos[i]) % 2 != 0:
            filasMal.append(i)

    # columnas con paridad LRC incorrecta
    colsMal = []
    for j in range(8):                              #por cada COLUMNA
        suma = 0
        for i in range(len(datos)):                 #por cada fila de esa columna
            suma += datos[i][j]
        if suma % 2 != lrc[j]:
            colsMal.append(j)

    # error simple: la interseccion de fila y columna fallidas
    if len(filasMal) == 1 and len(colsMal) == 1:
        datos[filasMal[0]][colsMal[0]] ^= 1         #invertimos el bit

    # decodificamos los 7 bits de datos de cada fila a ASCII
    texto = ""
    for fila in datos:                              #por cada caracter
        bits = "".join(str(b) for b in fila[:7])
        texto += chr(int(bits, 2))
    return texto

print("mensaje corregido: ", corregirParidad(entrada))