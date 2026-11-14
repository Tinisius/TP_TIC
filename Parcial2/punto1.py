import os
import sys
# Añade el directorio padre (dos niveles arriba o ajustando los niveles) a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.functions import *
from functions.functions2 import *

# - - - - - - - - - - - - PARCIAL 2 - - - - - - - - - - - -

mensaje = "LJMMJLMJLJJMLMMLLKJL"

#CHECKEAR
#print("MN?:", esMemoriaNula(mensaje))

#print("entropia fuente: ", entropiaTexto(mensaje, 2))

#print("tasa de compresion: ", tasaCompresionTexto(mensaje))

#print("long media", longMediaCod(codificacion_huffman(mensaje), probabilidadesTexto(mensaje)))

#print("eficiencia: ", eficienciaHuffman(mensaje))

#print("redundancia: ", redundanciaHuffman(mensaje))

probabilidades = probabilidadesTexto(mensaje)
alfabeto = generarAlfabeto(mensaje)
fuenteExtendida, probabilidadesExtendidas = generarExtensionFuente(alfabeto, probabilidades, 3) #extendemos la fuente de orden 3

probabilidadesFuenteExtendida = dict(zip(fuenteExtendida, probabilidadesExtendidas))    #{'LLL': 0.04287499999999999, 'LLJ': 0.03674999999999999, 'LLM': 0.03674999999999999,

codigoHuffmanExtendido = codificacion_huffman_probabilidades(probabilidadesFuenteExtendida) #{'LLL': '0000', 'LLK': '0001000', 'LKL': '0001001',

longMediaExtension = longMediaCod(codigoHuffmanExtendido, probabilidadesFuenteExtendida)
entropiaExtension = entropiaProbs(probabilidadesExtendidas, 2)

print("long media extension:", longMediaExtension)

print("FUENTE cumple primer teorema de shannon:", cumplePrimerShannon(mensaje))
print("EXTENSION cumple primer teorema de shannon:", entropiaExtension <= longMediaExtension < entropiaExtension + 1,
)