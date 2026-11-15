
#from functions.functions import *
import math

def generarAlfabetoCodigo(codigo):
    alfabetoCodigo = []
    for c in codigo:
        for simbolo in c:
            if simbolo not in alfabetoCodigo:
                alfabetoCodigo.append(simbolo)
    return alfabetoCodigo

def inecKraft(codigo, r):
    sum = 0
    for c in codigo:
        sum += r**(-len(c))
    return sum

def entropiaProbs(probs, r):
    #recibe una lista de probabilidades y calcula la entropia total de la fuente
    entropia = 0
    for prob in probs:
        entropia += prob * -math.log(prob, r)

    return round(entropia, 4)

def longMediaCod(codigo, probsCod):
    L = 0
    for i in range(len(codigo)):
        L += len(codigo[i])*probsCod[i]
    return L

def esCompacto(codigo, probsCod, r):
    return esUnivoco(codigo) and cumpleCotaCompactitud(codigo, probsCod, r)

def cumpleCotaCompactitud(codigo, probs, r):
    for S in codigo:
        index = codigo.index(S)
        if len(S) > math.ceil(-math.log(probs[index], r)):
            return False
    return True

def esUnivoco(codigo):
    #recibe una lista de palabras codigo (formato ["100", "101", "10"]) y determina si es Univocamente Decodificable (UD)

    vistos = []  #es un set de conjuntos S, porsi un conjunto se repite no entrar en bucle infinito
    S = set()   # inicialmente S1, representa solos los Sn

    #comparo el codigo con consigo mismo y genero el S1
    for x in codigo:
        for y in codigo:
            if x != y:
                if x.startswith(y):
                    S.add(x[len(y):])  #x[len(y):] extre el sufijo 
                elif y.startswith(x):
                    S.add(y[len(x):])

    while True:
        # Si aparece epsilon, no es UD
        if "" in S:
            return False

        # Si ya habíamos visto este conjunto, no aparecerá epsilon (conjunto vacio o "")
        if S in vistos: 
            return True

        vistos.append(S)

        S_nuevo = set()

        # Comparar los elementos de S con las palabras del código
        for s in S:
            for c in codigo:
                if s.startswith(c):
                    S_nuevo.add(s[len(c):])
                elif c.startswith(s):
                    S_nuevo.add(c[len(s):])

        S = S_nuevo

codigo = ["CA", "C", "AB", "BC", "A"]
probsCod = [1/9, 1/3, 1/9, 1/9, 1/3]
r = len(generarAlfabetoCodigo(codigo))

print("inecuacion de kraft", inecKraft(codigo, r))

print("entropia: ", entropiaProbs(probsCod, r))

print("logitud media: ", longMediaCod(codigo, probsCod))

print("es compacto" if esCompacto(codigo, probsCod, r) else "no es compacto")
