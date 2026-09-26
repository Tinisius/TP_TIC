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

def entropiaTextoMarkov(mensaje):
    entropia=0
    alfabeto = generarAlfabeto(mensaje)
    matTrans = generarMatrizTrans(mensaje)
    vectorEst = generarVectorEstacionario(matTrans)
    for i in range(len(alfabeto)):
        Hi = 0
        for j in range(len(alfabeto)):
            if matTrans[i][j] != 0:
                Hi += matTrans[i][j] * -math.log(matTrans[i][j], 2)
        entropia += vectorEst[i] * Hi

    return entropia


def entropiaTexto(mensaje):
    #recibe un string y calcula la entropia del mensaje

    if not esMemoriaNula(mensaje):
        return entropiaTextoMarkov(mensaje)

    probs = probabilidadesTexto(mensaje)
    info = informacionTexto(mensaje)
    entropia = 0
    for simbolo in probs:
        entropia += probs[simbolo] * info[simbolo]

    return round(entropia, 4)     #en formato int ej: 0.9183 


def generarAlfabeto(mensaje):
    #recibe un string y lista todos sus simbolos fuente
    alfabeto = []
    for char in mensaje:
        if char not in alfabeto:
            alfabeto.append(char)

    return alfabeto #en formato ["a", "b", "c"]

# PARA LISTA DE PROBABILIDADES

def informacionProbs(probs, base=2):
    #DEPRECADA
    #recibe una lista de probabilidades y calcula la informacion total asumniendo que cada simbolo sale 1 vez?
    informacion = 0
    for prob in probs:
        informacion += -math.log(prob, base)
    return round(informacion, 4)      #en formato 1.5337

def entropiaProbs(probs, r):
    #recibe una lista de probabilidades y calcula la entropia total de la fuente
    entropia = 0
    for prob in probs:
        entropia += prob * -math.log(prob, r)

    return round(entropia, 4)     #en formato int ej: 0.9183 BITS/SIMBOLO


# PARA GENERAR EXTENSION

def generarExtensionFuente(alfabeto, probabilidades, n):
    #recibe 2 listas (alfabeto y sus probabilidades(lista o dict, de preferencia lista)) 
    #y devuelve una extension de orden N a modo de 2 listas (alfabeto y sus probabilidades)
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

# GENERAR MATRIZ DE TRANSICION

def generarMatrizTrans(mensaje, HardCodedAlfabeto=None):
    if HardCodedAlfabeto is not None:
        #PARA MOSTRAR LA MATRIZ EN EL ORDEN QUE QUERRAMOS
        alfabeto = HardCodedAlfabeto
    else:
        alfabeto = generarAlfabeto(mensaje)

    N = len(alfabeto)
    mat = [[0 for _ in range(N)] for _ in range(N)]

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

    # MOSTRAR MATRIZ
    #for charIndex in range(len(generarAlfabeto(mensaje))):
    #    print(alfabeto[charIndex] + " = ", traspuesta[charIndex])

    return mat

def generarVectorEstacionario(matTrans, tolerancia=1e-12, maxIteraciones=100000):
    if not matTrans or any(len(fila) != len(matTrans) for fila in matTrans):
        raise ValueError("La matriz de transición debe ser cuadrada y no vacía")

    N = len(matTrans)
    matriz = []
    for fila in matTrans:
        if any(not math.isfinite(prob) or prob < 0 for prob in fila):
            raise ValueError("Las probabilidades deben ser finitas y no negativas")
        suma = math.fsum(fila)
        if suma == 0:
            raise ValueError("Cada fila debe tener al menos una transición saliente")
        matriz.append([prob / suma for prob in fila])   #normaliza la matriz (ya esta normalizada pero por si el redondeo la rompiera)

    vector = [1 / N] * N    #vector uniforme con suma = 1
    for _ in range(maxIteraciones):
        siguiente = []
        for j in range(N):
            prob = math.fsum(vector[i] * matriz[i][j] for i in range(N))
            siguiente.append((vector[j] + prob) / 2)

        diferencia = math.fsum(abs(siguiente[i] - vector[i]) for i in range(N))
        vector = siguiente
        if diferencia < tolerancia: #si el vector casi no cambia, corta
            return vector

    #si no corta antes de las iteraciones lanza error
    raise RuntimeError("El vector estacionario no convergió dentro del límite de iteraciones")

def escribirMatTrans(mensaje, HardCodedAlfabeto=None):
    #recibe el mensaje, genera la matriz y la muestra
    mat = generarMatrizTrans(mensaje, HardCodedAlfabeto)
    traspuesta = [list(fila) for fila in zip(*mat)]   #traspone la matriz

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


def esMemoriaNula(mensaje):
    mat = generarMatrizTrans(mensaje)
    N = len(generarAlfabeto(mensaje))
    for i in range(N):
        val = mat[i][1]
        for j in range(N):
            if (val != mat [i][j]):
                return False
    return True

# COMPACTITUD

def longMediaCod(codigo, probsCod):
    L = 0
    for i in range(len(codigo)):
        L += len(codigo[i])*probsCod[i]
    return L

def inecKraft(codigo, r):
    sum = 0
    for c in codigo:
        sum += r**(-len(c))
    return sum

def clasificacion(codigo):
    if not esNoSingular(codigo):
            return "Codigo Bloque"
    if not esUnivoco(codigo):
            return "Codigo NO Singular"
    if not esInstantaneo(codigo):
        return  "Codigo Univocamente Decodificable (UD)"
    return "Codigo Instantaneo"

def generarAlfabetoCodigo(codigo):
    alfabetoCodigo = []
    for c in codigo:
        for simbolo in c:
            if simbolo not in alfabetoCodigo:
                alfabetoCodigo.append(simbolo)
    return alfabetoCodigo

def longMediaMinimaHuffman(codigo, probsCod):
    alfabetoCodigo = generarAlfabetoCodigo(codigo)  #["/", "+", "-", "*", ]
    probsSorted = sorted(probsCod, reverse=True)  #ordena las probabilidades de mayor a menor
    r = len(alfabetoCodigo) #cantidad de simbolos codigo
    q = len(probsCod)    #cantidad de simbolos fuente
    L = 0
    for i in range(q):
        longPalabraCod = math.floor(i / (r - 1)) + 1
        if i % (r-1) == 0 and i == q-1: #no hacia falta aumentar la long en el ultimo, si es que la aumentó
             longPalabraCod -= 1
        L += probsSorted[i] * longPalabraCod
    return L

def esCompacto(codigo, probsCod, tolerancia=0.000000001):
    esMin =  (longMediaCod(codigo, probsCod) - longMediaMinimaHuffman(codigo, probsCod)) < tolerancia
    return esUnivoco(codigo) and esMin
    