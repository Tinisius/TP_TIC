from functions.functions import *

def tasaCompresionTexto(mensaje):
    sinComprimir = len(mensaje)*8
    
    huffman = codificacion_huffman(mensaje)
    comprimido = 0
    for char in mensaje:
        comprimido += len(huffman[char])
    return sinComprimir/comprimido


def codificacion_huffman(mensaje):
    if not mensaje:
        return {}

    return codificacion_huffman_probabilidades(probabilidadesTexto(mensaje))

#transforma {"aa": 0.1, "ab": 0.5, "ac": 0.4} en => {'ac': '0', 'aa': '10', 'ab': '11'}
def codificacion_huffman_probabilidades(probabilidades: dict):
    if not probabilidades:
        return {}

    # caso especial, hay un unico simbolo
    if len(probabilidades) == 1:
        return {next(iter(probabilidades)): "0"}

    grupos = []
    for simbolo, probabilidad in probabilidades.items():
        grupos.append([probabilidad, {simbolo: ""}])

    # Unimos siempre los dos grupos de menor frecuencia
    while len(grupos) > 1:
        #g[0] es la frecuencia de cada gupo, ordena por ese criterio
        grupos.sort(key=lambda g: g[0])
        menor = grupos.pop(0)
        segundo = grupos.pop(0)

        for simbolo in menor[1]:
            menor[1][simbolo] = "0" + menor[1][simbolo]
        for simbolo in segundo[1]:
            segundo[1][simbolo] = "1" + segundo[1][simbolo]

        menor[1].update(segundo[1])
        grupos.append([menor[0] + segundo[0], menor[1]])

    return grupos[0][1]

# - - - - - - - - - - - - EFICIENCIA Y REDUNDANCIA

def eficienciaHuffman(mensaje):
    entropia = entropiaTexto(mensaje,2)
    longMediaHuffman = longMediaCod(codificacion_huffman(mensaje), probabilidadesTexto(mensaje))
    return entropia / longMediaHuffman

def redundanciaHuffman(mensaje):
    return 1 - eficienciaHuffman(mensaje)

def eficienciaHuffmanProbs(probs:dict, cod:dict):
    longMedia = longMediaCod(cod, probs)
    entropia = entropiaProbs(probs, 2)
    return entropia / longMedia

def redundanciaHuffmanProbs(probs:dict, cod:dict):
    return 1 - eficienciaHuffmanProbs(probs, cod)

# - - - - - - - - - - - - PRIMER TEOREMA SHANNON

def cumplePrimerShannon(mensaje):
    probabilidades = probabilidadesTexto(mensaje)
    longMedia = longMediaCod(codificacion_huffman(mensaje), probabilidades)
    entropia = entropiaTexto(mensaje, 2)
    return entropia <= longMedia < entropia + 1

def cumplePrimerShannonProbs(probs:dict, cod:dict):
    longMedia = longMediaCod(cod, probs)
    entropia = entropiaProbs(probs, 2)
    return entropia <= longMedia < entropia + 1

# - - - - - - - - - - - - CANALES DE TRANSMISION

#entrada = "10111101100111101000001010100101"
#salida = "GGHHIIGHGFFGIIFGHGGGGFGGFGGFGFFG"
def generarMatrizCanal(entrada, salida):
    alfEntrada = sorted(generarAlfabeto(entrada))    #['0', '1']
    alfSalida = sorted(generarAlfabeto(salida))    #['F', 'G', 'H', 'I']

    #[[0, 0, 0, 0], [0, 0, 0, 0]]
    mat = [[0 for _ in range(len(alfSalida))] for _ in range(len(alfEntrada))]

    for i in range(len(entrada)):
        mat[alfEntrada.index(entrada[i])][alfSalida.index(salida[i])] += 1

    for i in range(len(alfEntrada)):
        sumaFila = sum(mat[i])
        for j in range(len(alfSalida)):
            mat[i][j] /= sumaFila
    return mat  #[[0.3333, 0.6666, 0.0, 0.0], [0.1764, 0.3529, 0.2352, 0.2352]]

def mostrarMatrizCanal(entrada, salida):
    alfEntrada = sorted(generarAlfabeto(entrada))    #['0', '1']
    alfSalida = sorted(generarAlfabeto(salida))    #['F', 'G', 'H', 'I']
    mat = generarMatrizCanal(entrada, salida)
    
    print("\nMATRIZ DEL CANAL:")
    for c in alfSalida:
        print("         " + c, end="")
    print("\n")

    for i in range(len(alfEntrada)):
        print(alfEntrada[i], "= ", end="")
        for prob in mat[i]:
            print(" | ", format(prob, ".4f"), end="")
        print("\n")

    print("\n")


def clasificarCanal(matriz, tol=0.000000001):
    filas = len(matriz)     #cantidad de filas
    cols = len(matriz[0])   #cantidad de columnas

    sin_ruido = True
    for j in range(cols):   #por cada COLUMNA nos fijamos que solo tenga un elemento no nulo
        no_nulos = 0
        for i in range(filas):  #iteramos por cada fila de esa columna  
            if abs(matriz[i][j]) > tol:
                no_nulos += 1
        if no_nulos != 1:
            sin_ruido = False

    determinante = True
    for i in range(filas):  #por cada FILA nos fijamos que solo tenga un elemento no nulo
        no_nulos = 0
        for j in range(cols):       #iteramos por cada columna de esa fila
            if abs(matriz[i][j]) > tol:
                no_nulos += 1
        if no_nulos != 1:
            determinante = False

    if sin_ruido and determinante:
        return "ambos"
    if sin_ruido:
        return "sin ruido"
    if determinante:
        return "determinante"
    return "ninguna"

# - - - - - - - - - - - - METRICAS DEL CANAL

def entropiaAprioriA(matriz, entrada: str):
    filas = len(matriz) #R
    probsEntrada = [p for _, p in sorted(probabilidadesTexto(entrada).items())]   #ordenado por simbolo
    entropia = 0

    for i in range(filas):
        if probsEntrada[i] > 0:
            entropia += probsEntrada[i] *  math.log(1 / probsEntrada[i], 2)
    return entropia


#H(A/B)
def equivocacionCanal(matriz, entrada: str):
    probsEntrada = [p for _, p in sorted(probabilidadesTexto(entrada).items())]   #ordenado por simbolo
    filas = len(matriz)
    cols = len(matriz[0])
    equivocacion = 0

    for j in range(cols):   # por cada COLUMNA (salida bj) => P(bj) = suma de P(ai) * P(bj/ai)
        probSalida = 0
        for i in range(filas):      #iteramos por cada fila de esa columna 
            probSalida += probsEntrada[i] * matriz[i][j]

        if probSalida == 0:    # salida imposible, no aporta
            continue

        # H(A/bj) = suma de P(ai/bj) * log2(1/P(ai/bj))
        entropiaColumna = 0
        for i in range(filas):
            pPosteriori = probsEntrada[i] * matriz[i][j] / probSalida   # teorema de bayes
            if pPosteriori > 0: #valido division por 0
                entropiaColumna += pPosteriori * math.log(1 / pPosteriori, 2)

        equivocacion += probSalida * entropiaColumna

    return equivocacion

#H(B/A)
def perdidaCanal(matriz, entrada: str):
    probsEntrada = [p for _, p in sorted(probabilidadesTexto(entrada).items())]   #ordenado por simbolo
    perdida = 0
    for i in range(len(matriz)):        # por cada FILA (entrada ai)
        entropiaFila = 0
        for j in range(len(matriz[0])):     #iteramos por cada columna de esa fila
            p = matriz[i][j]
            if p > 0:
                entropiaFila += p * math.log(1 / p, 2)
        perdida += probsEntrada[i] * entropiaFila
    return perdida

#I(A,B)
def informacionMutua(matriz, entrada: str):
    return entropiaAprioriA(matriz, entrada) - equivocacionCanal(matriz, entrada)

# - - - - - - - - - - - - CANAL REDUCIDO

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

def mostrarMatrizReducida(entrada, salida):
    matRed = matrizReducida(entrada, salida)
    alfEntrada = sorted(generarAlfabeto(entrada))    #['0', '1']
    print("\nCANAL REDUCIDO: ")
    for i in range(len(alfEntrada)):
        print(alfEntrada[i], "= ", end="")
        for prob in matRed[i]:
            print(" | ", format(prob, ".4f"), end="")
        print("\n")
    print("\n")









