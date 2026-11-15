import os
import sys
# Añade el directorio padre (dos niveles arriba o ajustando los niveles) a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.functions import *

mensaje = ".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::."

probs = probabilidadesTexto(mensaje)

print("P(',') = ", probs[","])
print("P('.') = ", probs["."])
print("P(':') = ", probs[":"])
print("P(';') = ", probs[";"])

escribirMatTrans(mensaje, sorted(set(mensaje)))

print("memoria: ", "NULA" if esMemoriaNula(mensaje) else "NO NULA (orden 1)")

print("entropia: ", entropiaTexto(mensaje, 2))

print(generarVectorEstacionario(generarMatrizTransicion(mensaje, sorted(set(mensaje)))))