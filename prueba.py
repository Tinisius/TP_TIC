def afa(cadena):
    repeticiones = {}

    for char in cadena:
        print(char)
        repeticiones[char] = repeticiones.get(char, 0) + 1

    print(repeticiones)

cad = "aaaaab"
afa(cad)