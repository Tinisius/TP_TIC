#from functions.functions import *
import math

def generarExtensionFuente(alfabeto, probabilidades, n):
    #recibe 2 listas (alfabeto y sus probabilidades(lista o dict, de preferencia lista)) 
    #y devuelve una extension de orden N a modo de 2 listas (alfabeto y sus probabilidades)
    alfabetoExtendido = []
    probabilidadesExtendido = []
    posiciones = [0] * n
    carry = 0
    q = len(alfabeto)

    while (carry != 1): #corta cuando i == -1 => carry == 1
        # construir la palabra extendida y la probabilidad
        palabra = ""
        prob = 1
        for pos in posiciones:
            palabra += alfabeto[pos]
            #el ternario distingue si probabilidades es un diccionario o un lista
            prob *= probabilidades[alfabeto[pos]] if isinstance(probabilidades, dict) else probabilidades[pos]

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

def informacionTexto(mensaje, r):
    probs = probabilidadesTexto(mensaje)
    informacion = {
        simbolo: round(-math.log(probs[simbolo], r), 4) for simbolo in probs    #compresion de listas
        #math.log(pow(NUM, -1), 2) 
        # ES LO MISMO QUE 
        #-math.log(NUM, 2)
    }
    return informacion 

def entropiaProbs(probs, r):
    entropia = 0
    for prob in probs:
        entropia += prob * -math.log(prob, r)

    return round(entropia, 4) 

def entropiaTexto(mensaje, r):

    probs = probabilidadesTexto(mensaje)
    info = informacionTexto(mensaje, r)
    entropia = 0
    for simbolo in probs:
        entropia += probs[simbolo] * info[simbolo]

    return round(entropia, 4)     #en formato int ej: 0.9183 

def probabilidadesTexto(mensaje):
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

def generarVectorEstacionario(mat, tolerancia=0.00001, maxIteraciones=100000):
    if not mat or any(len(fila) != len(mat) for fila in mat):
        raise ValueError("La matriz de transición debe ser cuadrada y no vacía")

    N = len(mat)
    matriz = []
    for fila in mat:
        suma = sum(fila)
        if suma == 0:
            raise ValueError("Cada fila debe tener al menos una transición saliente")
        matriz.append([prob / suma for prob in fila])   #normaliza la matriz (ya esta normalizada pero por si el redondeo la rompiera)

    vector = [1 / N] * N    #vector uniforme con suma = 1
    for _ in range(maxIteraciones):
        siguiente = [0] * N
        for j in range(N):
            siguiente[j] = sum(vector[i] * matriz[i][j] for i in range(N))  #suma(multiplicacion matricial)

        diferencia = sum(abs(siguiente[i] - vector[i]) for i in range(N)) #calcula la suma de todas las diferencias del vec respecto ant
        vector = siguiente
        if diferencia < tolerancia: #si el vector casi no cambia, corta
            return vector

    #si no corta antes de las iteraciones lanza error
    raise RuntimeError("El vector estacionario no convergió dentro del límite de iteraciones")


def esMemoriaNula(mensaje, tolerancia=0.001):
    mat = generarMatrizTransicion(mensaje)
    traspuesta = transponerMatriz(mat)   #traspone la matriz
    vec = []
    for fila in traspuesta:
        vec.append(max(fila) - min(fila))
    return max(vec) <= tolerancia

def generarAlfabeto(mensaje):
    return sorted(set(mensaje)) #en formato ["a", "b", "c"]

def transponerMatriz(mat):
    return [list(fila) for fila in zip(*mat)]

def generarMatrizTransicion(mensaje, HardCodedAlfabeto=None):
    if HardCodedAlfabeto is not None:
        #PARA MOSTRAR LA MATRIZ EN EL ORDEN QUE QUERRAMOS
        alfabeto = HardCodedAlfabeto
    else:
        alfabeto = generarAlfabeto(mensaje)

    N = len(alfabeto)
    mat = [[0 for _ in range(N)] for _ in range(N)] #INICIALIZO LA MATRIZ

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
    return mat

def escribirMatTrans(mensaje, HardCodedAlfabeto=None):
    mat = generarMatrizTransicion(mensaje, HardCodedAlfabeto)
    traspuesta = transponerMatriz(mat)   #traspone la matriz

    if HardCodedAlfabeto is not None:
        #PARA MOSTRAR LA MATRIZ EN EL ORDEN QUE QUERRAMOS
        alfabeto = HardCodedAlfabeto
    else:
        alfabeto = generarAlfabeto(mensaje)

    #significado de cada columna
    for i in range(len(alfabeto)):
        print("            " + alfabeto[i], end="")
    print("\n")

    #cada fila
    for charIndex in range(len(alfabeto)):
        print(alfabeto[charIndex] + " =  ", end="")
        for prob in traspuesta[charIndex]:
            print(f"[{prob:.8f}] ", end="")  
        print("\n") 


mensaje = "BBCCAABBCCAABBCCAABBCCAABBCCAA"

escribirMatTrans(mensaje)

print("memoria NULA" if esMemoriaNula(mensaje) else "memoria NO NULA (orden 1)")

print("vector estacionario: ", generarVectorEstacionario(generarMatrizTransicion(mensaje)))

alfabeto = generarAlfabeto(mensaje)
probs = probabilidadesTexto(mensaje)

alfabetoExt, probsExt = generarExtensionFuente(alfabeto, probs, 2)

print("Alfabeto fuente extendida:", alfabetoExt)
print("Probabilidades fuente extendida:", probsExt)

print("P( 'AA' ) = ", probsExt[alfabetoExt.index("AA")])
print("P( 'BA' ) = ", probsExt[alfabetoExt.index("BA")])
print("P( 'CB' ) = ", probsExt[alfabetoExt.index("CB")])

print("entropia de S: ", entropiaTexto(mensaje, 2))
print("entropia de S extendida: ", entropiaProbs(probsExt, 2))
