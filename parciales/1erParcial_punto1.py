import os
import sys
# Añade el directorio padre (dos niveles arriba o ajustando los niveles) a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.functions import *

# - - - - - - - - - - - - PARCIAL 1 - - - - - - - - - - - -

#____________________________________________________________________________________________________
#MENSAJE 1
mensaje = ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"

#probs:
print("\n PROBABILIDADES:")
probs = probabilidadesTexto(mensaje)
print("P(,) = " + str(probs[","]))
print("P(.) = " + str(probs["."]))
print("P(:) = " + str(probs[":"]))
print("P(;) = " + str(probs[";"]))

#matriz de transicion
escribirMatTrans(mensaje, [",",".",":",";"])  #genera y muestra la mat de trans

#tipo de memoria
print("tipo de memoria de la fuente: ", "Memoria Nula" if esMemoriaNula(mensaje) else "Memoria NO nula (orden 1)")

#entropia
print("entropia: ", entropiaTexto(mensaje))

#extension
alfabeto = generarAlfabeto(mensaje)
probabilidades = probabilidadesTexto(mensaje)
alfabetoExtendido, probabilidadesExtendido = generarExtensionFuente(alfabeto, probabilidades, 2)

P1_INDEX = alfabetoExtendido.index(",;")
P2_INDEX = alfabetoExtendido.index(":.")

print("P(,;) = " + str(probabilidadesExtendido[P1_INDEX]))
print("P(:.) = " + str(probabilidadesExtendido[P2_INDEX]))
print("entropia extension: ", entropiaProbs(probabilidadesExtendido))
