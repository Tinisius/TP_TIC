import math

# PARA TEXTO / MENSAJE

def probabilidadesTexto(cadena):
    alfabeto = []
    repeticiones = []
    for char in cadena:
        if char in alfabeto:
            i = alfabeto.index(char)
            repeticiones[i] += 1
        else:
            alfabeto.append(char)
            repeticiones.append(1)

    probs = [round(count / len(cadena), 4) for count in repeticiones]

    return dict(zip(alfabeto, probs))   #en formato {"a":0.2346, "b":0.4307}


def informacionTexto(cadena):
    probs = probabilidadesTexto(cadena)
    informacion = {
        simbolo: round(-math.log(probs[simbolo], 2), 4) for simbolo in probs
        #math.log(pow(NUM, -1), 2) 
        # ES LO MISMO QUE 
        #-math.log(NUM, 2)
    }
    return informacion      #en formato {"a":1.5851, "b":0.4307}

def entropiaTexto(cadena):
    probs = probabilidadesTexto(cadena)
    info = informacionTexto(cadena)
    entropia = 0
    for simbolo in probs:
        entropia += probs[simbolo] * info[simbolo]

    return round(entropia, 4)     #en formato int ej: 0.9183 


def alfabeto(cadena):
    alfabeto = []
    for char in cadena:
        if char not in alfabeto:
            alfabeto.append(char)

    return alfabeto #en formato ["a", "b", "c"]

# PARA LISTA DE PROBABILIDADES

def informacionProbs(probs):
    informacion = 0
    for prob in probs:
        informacion += -math.log(prob, 2)
    return informacion      #en formato {"a":1.5851, "b":0.4307}

def entropiaProbs(probs):
    entropia = 0

    for prob in probs:
        entropia += prob * -math.log(prob, 2)

    return round(entropia, 4)     #en formato int ej: 0.9183 


# PARA GENERAR EXTENSION

def generarExtensionFuente(alfabeto, probabilidades, n):
    alfabetoExtendido = []
    probabilidadesExtendido = []
    posiciones = [0] * n
    carry = 0
    q = len(alfabeto)

    while (carry != 1):
        # construir la palabra extendida y la probabilidad
        palabra = ""
        prob = 1
        for pos in posiciones:
            palabra += alfabeto[pos]
            prob *= probabilidades[pos]

        alfabetoExtendido.append(palabra)
        probabilidadesExtendido.append(round(prob, 4))

        # avanzar la posición
        carry = 1
        i = n - 1
        while (carry == 1 and i >= 0):
            if (posiciones[i] + 1 < q): #si encuentra una pos que no esta en su ultimo caracter
                posiciones[i] += 1
                carry = 0
            else:
                posiciones[i] = 0
                carry = 1
                i -= 1
        
    return alfabetoExtendido, probabilidadesExtendido

# DETECTAR SI ES NO SINGULAR

def esNoSingular(codigo):
    return len(codigo) == len(set(codigo))  #set elimina duplicados

# DETECTAR SI ES INSTANTANEO

def esInstantaneo(codigo):
    inst = True
    for S1 in codigo:
        for S2 in codigo:
            if S1 == S2:
                pass
            inst = not S2.startswith(S1)
            if not inst:
                break
    return inst


#MAIN TESTER

TEXTO = "A"

#print("PROBS TEXTO: " + str(probabilidadesTexto(TEXTO)))
#print("ENTROPIA TEXTO: " + str(entropiaTexto(TEXTO)) + "bits")

w = 0.75
PROBS = [w, 1-w]

#print("ENTROPIA LISTA PROBS: " + str(entropiaProbs(PROBS)) + " bits")

# P11
alfabeto_orig = ["x", "y", "z"]
probs_orig = [0.5, 0.1, 0.4]
N = 3

"""
alf_ext, p_ext = generarExtensionFuente(alfabeto_orig, probs_orig, N)
print("Alfabeto extendido:", alf_ext)
print("Probabilidades:", p_ext)

print("EntropiaBASE:", str(entropiaProbs(probs_orig)), " bits")
print("EntropiaExt:", str(entropiaProbs(p_ext)), " bits")

print("comp:", str(entropiaProbs(p_ext)), str(entropiaProbs(probs_orig*N)))


codigo = ["100", "101", "10"]

print("es no singular (bueno): " + str(esNoSingular(codigo)))
"""

fuente = ["a", "bc", "cd", "d"]

print(esInstantaneo(fuente))