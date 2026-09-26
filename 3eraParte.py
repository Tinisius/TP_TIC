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
    

print("es compacto"if esCompacto(codigo, probsCod) else "NO es compacto")