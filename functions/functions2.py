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

#probabilidades es un diccionario {"a":0.30, "b":0.15, ...}
def codificacion_huffman_probabilidades(probabilidades):
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

def eficienciaHuffman(mensaje):
    entropia = entropiaTexto(mensaje,2)
    longMediaHuffman = longMediaCod(codificacion_huffman(mensaje), probabilidadesTexto(mensaje))
    return entropia / longMediaHuffman

def redundanciaHuffman(mensaje):
    return 1 - eficienciaHuffman(mensaje)

def cumplePrimerShannon(mensaje):
    probabilidades = probabilidadesTexto(mensaje)
    longMedia = longMediaCod(codificacion_huffman(mensaje), probabilidades)
    entropia = entropiaTexto(mensaje, 2)
    return entropia <= longMedia < entropia + 1

#def cumplePrimerShannonProbs():