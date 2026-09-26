import os
import sys
# Añade el directorio padre (dos niveles arriba o ajustando los niveles) a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.functions import *

probsCod = [0.15, 0.25, 0.05, 0.45, 0.10]
codigo = ["/+", "*", "+-", "-", "*/", ]

r = len(generarAlfabetoCodigo(codigo))
print("entropia: ", entropiaProbs(probsCod, r))

print("longitud media: ", longMediaCod(codigo, probsCod))

print("inecuacion de Kraft-Mcmillan: ", inecKraft(codigo, probsCod,4))

print("clasificacion:", clasificacion(codigo))

print("es compacto"if esCompacto(codigo, probsCod) else "NO es compacto")