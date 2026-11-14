from functions.functions import *
from functions.functions2 import *

entrada = "10111101100111101000001010100101"
salida = "GGHHIIGHGFFGIIFGHGGGGFGGFGGFGFFG"

def columnasProporcionales(matriz, j1, j2, tol=1e-3):
    filas = len(matriz)
    k = None            #constante de proporcionalidad

    for i in range(filas):          #por cada FILA comparamos las dos columnas
        a = matriz[i][j1]
        b = matriz[i][j2]

        if a == 0 and b == 0:           #ambos cero: no aporta restriccion
            continue
        if a == 0 or b == 0:            #uno cero y el otro no: no son proporcionales
            return False

        if k is None:
            k = a / b           #fijamos la constante con la primera fila util
        elif abs(a / b - k) > tol:          #otra fila con distinta razon
            return False

    return True

#[[0, 0, 0, 0], [0, 0, 0, 0]]
def matrizReducida(entrada, salida):
    matriz = generarMatrizCanal(entrada, salida)
    
    a = 0
    while a < len(matriz[0]):       #por cada columna a (el largo cambia al fusionar)
        b = a + 1
        while b < len(matriz[0]):       #todas las columnas por delante de a
            if columnasProporcionales(matriz, a, b):        #2 columnas proporcionales, juntamos
                for i in range(len(matriz)):        #por cada FILA sumamos b en a y borramos b
                    matriz[i][a] += matriz[i][b]
                    matriz[i].pop(b)
                #no avanzamos b: la columna siguiente ocupa ahora el lugar de b
            else:
                b += 1          #no se fusiono, pasamos a la siguiente
        a += 1          #pasamos a la siguiente columna base

    return matriz

print(matrizReducida(entrada, salida))