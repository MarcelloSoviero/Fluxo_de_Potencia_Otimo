import pandas as pd

class Mundo:
    def __init__(self):
        self.tabela_barras = pd.read_csv("tabela_barras.csv")
        self.tabela_conexoes = pd.read_csv("tabela_conexoes.csv")
        self.ybarra = None

    def gerar_Ybarra(self):
        linha = [0]*len(self.tabela_conexoes)
        ybarra = []
        for _ in range(len(self.tabela_conexoes)):
            ybarra.append(linha[:])

        for n in range(len(self.tabela_conexoes)):
            impedancia = complex(self.tabela_conexoes.iloc[n]["Impedancia"])
            lista_barras_afetadas = self.tabela_conexoes.iloc[n]["Conexao"].split("-")
            ybarra[int(lista_barras_afetadas[0])][int(lista_barras_afetadas[1])] = -1/impedancia
            ybarra[int(lista_barras_afetadas[1])][int(lista_barras_afetadas[0])] = -1/impedancia
            for barra_afetada in lista_barras_afetadas:
                ybarra[int(barra_afetada)][int(barra_afetada)] += 1/impedancia + complex(self.tabela_conexoes.iloc[n]["Shunt"])/2

        for linha in ybarra:
            print(linha)
        
        self.ybarra = ybarra

    def gerar_B_e_G(self):
        B = []
        G = []
        linha = [0]*len(self.tabela_conexoes)
        for _ in range(len(self.tabela_conexoes)):
            B.append(linha[:])
            G.append(linha[:])

        for il, linha in enumerate(self.ybarra):
            for ic, coluna in enumerate(linha):
                B[il][ic] = coluna.imag
                G[il][ic] = coluna.real

        for linha in B:
            print(linha)
        for linha in G:
            print(linha)



mu = Mundo()
mu.gerar_Ybarra()
mu.gerar_B_e_G()