import os
import sys
# Añade el directorio padre (dos niveles arriba o ajustando los niveles) a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.functions import *

# - - - - - - - - - - - - PARCIAL 1 - - - - - - - - - - - -

#____________________________________________________________________________________________________
#MENSAJE 2

mensaje = ".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::."

probs = probabilidadesTexto(mensaje)

print("P(,)= ", probs[","])
print("P(.)= ", probs["."])
print("P(:)= ", probs[":"])
print("P(;)= ", probs[";"])

escribirMatTrans(mensaje, [",",".",":",";",])

print("tipo de memoria de la fuente: ", "Memoria Nula" if esMemoriaNula(mensaje) else "Memoria NO nula (orden 1)")

print("entropia: ", entropiaTextoMarkov(mensaje))