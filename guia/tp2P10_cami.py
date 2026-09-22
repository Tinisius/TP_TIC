import math
#import random
from functions.functions import *

def alfabetoYprob(cadena):
    #dado un STRING devuelve 2 arreglos paralelos ALF y PROB
    alfabeto = []
    repeticiones = []
    for char in cadena:
        if char in alfabeto:
            i = alfabeto.index(char)
            repeticiones[i] += 1
        else:
            alfabeto.append(char)
            repeticiones.append(1)

    probs = [count / len(cadena) for count in repeticiones]

    return alfabeto, probs

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