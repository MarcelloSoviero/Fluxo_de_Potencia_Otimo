import barra


barras = []
for n in range(3):
    barras.append(barra.Barra(n, "PV", 1, 0, {1: 1+2j, 2: 2+1j}, [2j]))


PVs = []
PQs = []
VTs = []
for b in barras:
    if b.tipo_barra == "PV":
        PVs.append(b.indice)
    
    elif b.tipo_barra == "PQ":
        PQs.append(b.indice)

    else:
        VTs.append(b.indice)























for b in barras:
    print(b)