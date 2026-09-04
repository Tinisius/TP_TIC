import math

def informacion(cadena):
    probs = probabilidades(cadena)
    informacion = {
        simbolo: round(-math.log(probs[simbolo], 2), 4) for simbolo in probs
        #math.log(NUM, -1), 2) 
        # ES LO MISMO QUE 
        #-math.log(NUM, 2)
    }
    return informacion      #en formato {"a":1.5851, "b":0.4307}

def entropia(cadena):
    probs = probabilidades(cadena)
    info = informacion(cadena)
    entropia = 0
    for simbolo in probs:
        entropia += probs[simbolo] * info[simbolo]

    return round(entropia, 4)     #en formato int ej: 0.9183 

def probabilidades(cadena):
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

def alfabeto(cadena):
    alfabeto = []
    for char in cadena:
        if char not in alfabeto:
            alfabeto.append(char)

    return alfabeto #en formato ["a", "b", "c"]

print(informacion("100"))