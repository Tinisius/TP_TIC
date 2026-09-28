import os
import sys
# Añade el directorio padre (dos niveles arriba o ajustando los niveles) a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.functions import *

codigo = ["*/", "/", "-+", "+", "*-", ]
probsCod = [0.15, 0.25, 0.05, 0.45, 0.10]

r = len(generarAlfabetoCodigo(codigo))
print("entropia: ", entropiaProbs(probsCod, r))

print("longitud media: ", longMediaCod(codigo, probsCod))

print("inecuacion de kraft-mcmillan: ", inecKraft(codigo, r))

print("clasificacion:: ", clasificacion(codigo))

print("Es compacto" if esCompacto(codigo, probsCod) else "NO es compacto")