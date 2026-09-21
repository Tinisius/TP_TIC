import math
#import random

def generarExtensionFuente(alfabeto, probabilidades, n):
    alfabetoExtendido = []
    probabilidadesExtendido = []
    posiciones = [0] * n
    carry = 0
    q = len(alfabeto)

    while (carry != 1):
        # construir la palabra extendida y la probabilidad
        print(posiciones)
        palabra = ""
        prob = 1
        for pos in posiciones:
            palabra += alfabeto[pos]
            prob *= probabilidades[pos]

        alfabetoExtendido.append(palabra)
        probabilidadesExtendido.append(prob)

        # avanzar la posición
        if (posiciones[n-1] + 1 < q):
            posiciones[n-1] += 1 
        else:
            posiciones[n-1] = 0
            carry = 1
            i = n - 2 
            while (carry == 1 and i >= 0):
                if (posiciones[i] + 1 < q):
                    posiciones[i] += 1
                    carry = 0
                else:
                    posiciones[i] = 0
                    carry = 1
                    i -= 1
            
    return alfabetoExtendido, probabilidadesExtendido

def generarFuente(cadena):
    alfabeto = []
    probabilidades = []
    for i in cadena:
        if (i not in alfabeto):
            alfabeto.append(i)
            probabilidades.append(0)
        probabilidades[alfabeto.index(i)] += 1
    probabilidades = [prob / len(cadena) for prob in probabilidades]

    return alfabeto, probabilidades

def generarListaInformaciones(probabilidades):
    return [math.log2(1/prob) if prob > 0 else 0 for prob in probabilidades]

def entropia(probabilidades, informaciones):
    suma = 0
    for x, y in zip(probabilidades, informaciones):
        suma += x*y
    return suma

print("\n\n\tEjercicio 10\n")
print("Ingrese cadena para generar fuente")
cadena = input()
alfabeto, probabilidades = generarFuente(cadena)
informaciones = generarListaInformaciones(probabilidades)
entr = entropia(probabilidades,informaciones)

print("Cadena:",cadena)
print("Largo de la cadena:",len(cadena))
print("Alfabeto:",alfabeto)
print("Probabilidades:",probabilidades)
print("Informaciones:",informaciones)
print("Entropía de la fuente:",entr)
print("\n\n")

print("Ingrese orden n de la extensión de la fuente")
n = input()
n = int(n)
alfabetoExtendido, probabilidadesExtendidas = generarExtensionFuente(alfabeto, probabilidades, n)
informacionesExtendidas = generarListaInformaciones(probabilidadesExtendidas)
entrExtendida = entropia(probabilidadesExtendidas,informacionesExtendidas)

#print()
#print("Fuente de extensión de orden",n)
print("Alfabeto de la fuente extendida:",alfabetoExtendido,"\n")
#print("Probabilidades de la fuente extendida",probabilidadesExtendidas,"\n")
#print("Lista de informaciones de la fuente extendida",informacionesExtendidas,"\n")
#print("Entropía de la fuente extendida: \nH(S^n) = ",entrExtendida,"\nH(S^n) = n * H(S) = ",n,"*",entr,"=",n*entr)
#print("\n\n\n\n")