import random

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


def generarCadena(N, alf, probs):
    acum = [probs[0]]
    for i in range(1, len(probs)):
        acum.append(acum[i-1] + probs[i])

    genStr = ""
    for i in range(N):
        j = 0
        while acum[j] < random.random():
            j = j + 1
        
        genStr = genStr + alf[j]

    return genStr



alfabeto, probs = alfabetoYprob("aaabbc")

cadenaGenerada = generarCadena(30, alfabeto, probs)

print(probs)
