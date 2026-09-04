import math

probs = [0.20, 0.35, 0.15, 0.30]

def genListInf(listaProbs):
    listaInf = [math.log(pow(num, -1), 2) for num in listaProbs]
    return listaInf

def obtieneEntropia(listaProbs, listaInf):
    entropia = 0
    for i in range(len(listaProbs)):
        entropia = entropia + listaInf[i] * listaProbs[i]
    return entropia

informacion = genListInf(probs)

print("list de probs:")
print(probs)
print("list de info:")
print(informacion)
print("entropia:" + str(round(obtieneEntropia(probs, informacion), 2)))

