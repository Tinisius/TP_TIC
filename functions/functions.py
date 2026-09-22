import math

# PARA TEXTO / MENSAJE

def probabilidadesTexto(mensaje):
    #recibe un string y calcula la prob de cada simbolo a modo de diccionario
    alfabeto = []
    repeticiones = []
    for char in mensaje:
        if char in alfabeto:
            i = alfabeto.index(char)
            repeticiones[i] += 1
        else:
            alfabeto.append(char)
            repeticiones.append(1)

    probs = [round(count / len(mensaje), 4) for count in repeticiones]

    return dict(zip(alfabeto, probs))   #en formato {"a":0.2346, "b":0.4307}


def informacionTexto(mensaje):
    #recibe un string y calcula la informacion de cada simbolo a modo de diccionario
    probs = probabilidadesTexto(mensaje)
    informacion = {
        simbolo: round(-math.log(probs[simbolo], 2), 4) for simbolo in probs    #compresion de listas
        #math.log(pow(NUM, -1), 2) 
        # ES LO MISMO QUE 
        #-math.log(NUM, 2)
    }
    return informacion      #en formato {"a":1.5851, "b":0.4307}

def entropiaTexto(mensaje):
    #recibe un string y calcula la entropia del mensaje
    probs = probabilidadesTexto(mensaje)
    info = informacionTexto(mensaje)
    entropia = 0
    for simbolo in probs:
        entropia += probs[simbolo] * info[simbolo]

    return round(entropia, 4)     #en formato int ej: 0.9183 


def GenerarAlfabeto(mensaje):
    #recibe un string y lista todos sus simbolos fuente
    alfabeto = []
    for char in mensaje:
        if char not in alfabeto:
            alfabeto.append(char)

    return alfabeto #en formato ["a", "b", "c"]

# PARA LISTA DE PROBABILIDADES

def informacionProbs(probs):
    #DEPRECADA
    #recibe una lista de probabilidades y calcula la informacion total asumniendo que csa simbolo sale 1 vez?
    informacion = 0
    for prob in probs:
        informacion += -math.log(prob, 2)
    return round(informacion, 4)      #en formato 1.5337

def entropiaProbs(probs):
    #recibe una lista de probabilidades y calcula la entropia total de la fuente
    entropia = 0
    for prob in probs:
        entropia += prob * -math.log(prob, 2)

    return round(entropia, 4)     #en formato int ej: 0.9183 BITS/SIMBOLO


# PARA GENERAR EXTENSION

def generarExtensionFuente(alfabeto, probabilidades, n):
    #recibe 2 listas (alfabeto y sus probabilidades) y devuelve una extension de orden N a modo de 2 listas (alfabeto y sus probabilidades)
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

# CALIDAD DE CODIFICACION

def esNoSingular(codigo):
    #recibe una lista de palabras codigo (formato ["100", "101", "10"]) y determina si es NoSingular
    return len(codigo) == len(set(codigo))  #set elimina duplicados

def esInstantaneo(codigo):
    #recibe una lista de palabras codigo (formato ["100", "101", "10"]) y determina si es Instantaneo

    if not esNoSingular(codigo):    #preguntar si hace falta
        return False
    
    for S1 in codigo:
        for S2 in codigo:
            if S1 != S2 and S2.startswith(S1):  #verifica que un codigo no sea prefijo de otro, omite si son el mismo
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

        vistos.add(S)

        S_nuevo = set()

        # Comparar los elementos de S con las palabras del código
        for s in S:
            for c in codigo:
                if s.startswith(c):
                    S_nuevo.add(s[len(c):])
                elif c.startswith(s):
                    S_nuevo.add(c[len(s):])

        S = S_nuevo


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