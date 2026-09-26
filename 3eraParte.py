from functions.functions import *

probsCod = [0.15, 0.25, 0.05, 0.45, 0.10]
codigo = ["/+", "*", "+-", "-", "*/", ]

print("entropia: ", entropiaProbs(probsCod, 4))

def longMediaCod(codigo, probsCod):
    L = 0
    for i in range(len(codigo)):
        L += len(codigo[i])*probsCod[i]
    return L

print("longitud media: ", longMediaCod(codigo, probsCod))

def inecKraft(codigo, probdCod, r):
    sum = 0
    for c in codigo:
        sum += r**(-len(c))
    return sum

print("inecuacion de Kraft-Mcmillan: ", inecKraft(codigo, probsCod,4))

def clasificacion(codigo):
    if not esNoSingular(codigo):
            return "bloque"
    if not esUnivoco(codigo):
            return "no Singular"
    if not esInstantaneo(codigo):
        return  "univocamente Decodificable"
    return "instantaneo"

print("clasificacion:", clasificacion(codigo))

def longHuffman(codigo, probsCod):
     return 0

def esCompacto(codigo, probsCod):
    return esUnivoco(codigo) and longMediaCod(codigo, probsCod) == longHuffman(codigo, probsCod)
    

print("es compacto"if esCompacto(codigo, probsCod) else "NO es compacto")