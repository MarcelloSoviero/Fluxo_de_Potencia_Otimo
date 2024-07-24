import pandas as pd
import os
from math import cos, sin
import barra

root_dir = os.path.dirname(os.path.abspath(__file__))[:-4]
path_barras = os.path.join(root_dir, "tabela_barras.csv")
path_conexoes = os.path.join(root_dir, "tabela_conexoes.csv")

class Mundo:
    def __init__(self):
        self.tabela_barras = pd.read_csv(path_barras)
        self.tabela_conexoes = pd.read_csv(path_conexoes)
        self.ybarra = None

    def gerar_Ybarra(self):
        linha = [0]*len(self.tabela_barras)
        ybarra = []
        for _ in range(len(self.tabela_barras)):
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
        linha = [0]*len(self.tabela_barras)
        for _ in range(len(self.tabela_barras)):
            B.append(linha[:])
            G.append(linha[:])

        for il, linha in enumerate(self.ybarra):
            for ic, coluna in enumerate(linha):
                B[il][ic] = coluna.imag
                G[il][ic] = coluna.real

        self.G = G
        self.B = B


    def ler_tab_barras(self):
        self.barras = []
        for n in range(len(self.tabela_barras)):
            infos_barra = self.tabela_barras.iloc[n]
            self.barras.append(barra.Barra(int(infos_barra["Indice"]),infos_barra["Tipo"],float(infos_barra["P"]),float(infos_barra["Q"]),
                                           float(infos_barra["V"]),float(infos_barra["Theta"]), 0, 0))


    def Pkm(self, barra_k, barra_m):
        k = barra_k.indice
        m = barra_m.indice
        return (self.G[k][m]*cos(barra_k.theta-barra_m.theta) + self.B[k][m]*sin(barra_k.theta-barra_m.theta))*barra_m.V*barra_k.V
    
    def Qkm(self, barra_k, barra_m):
        k = barra_k.indice
        m = barra_m.indice
        return (self.G[k][m]*sin(barra_k.theta-barra_m.theta) - self.B[k][m]*cos(barra_k.theta-barra_m.theta))*barra_m.V*barra_k.V


    def P_e_Q(self):
        tol = 0.003
        repetir = False
        for barra_k in self.barras:
            if barra_k.tipo_barra == "PQ":
                #Pk = Vk*(Vm*(Gkm*cos(theta_km) + Bkm*sin(theta_km)))  para todo m pertencente às barras (incluindo k)
                Pk_temp = 0
                Qk_temp = 0
                for barra_m in self.barras:
                    Pk_temp += self.Pkm(barra_k, barra_m)
                    Qk_temp += self.Qkm(barra_k, barra_m)

                barra_k.P_calculado = Pk_temp
                barra_k.Q_calculado = Qk_temp
                barra_k.delta_P = barra_k.P - Pk_temp
                barra_k.delta_Q = barra_k.Q - Qk_temp
                if not repetir and (abs(barra_k.delta_P) > tol or abs(barra_k.delta_Q) > tol):
                    repetir = True
            
            elif barra_k.tipo_barra == "PV":
                Pk_temp = 0
                Qk_temp = 0
                for barra_m in self.barras:
                    Pk_temp += self.Pkm(barra_k, barra_m)
                    Qk_temp += self.Qkm(barra_k, barra_m)

                barra_k.P_calculado = Pk_temp
                barra_k.Q_calculado = Qk_temp
                barra_k.delta_P = barra_k.P - Pk_temp
                if not repetir and abs(barra_k.delta_P) > tol:
                    repetir = True

            else:
                pass
        

    def criar_jacobiano_base(self):
        linha = [0]*len(self.barras)*2
        jacobiano = []
        for barra in self.barras:
            jacobiano.append(linha[:])
            jacobiano.append(linha[:])

        self.jacobiano_base = jacobiano


    def Hkm(self, barra_k, barra_m):
        k = barra_k.indice
        m = barra_m.indice
        if barra_k.tipo_barra != "VT" and barra_m.tipo_barra != "VT":
            if k != m:
                return (self.G[k][m]*sin(barra_k.theta-barra_m.theta) - self.B[k][m]*cos(barra_k.theta-barra_m.theta))*barra_m.V*barra_k.V

            elif k == m:
                print(barra_k)
                return -barra_m.V*barra_k.V*self.B[k][m] - barra_k.Q_calculado
            
        else:
            return 0
        
    def Nkm(self, barra_k, barra_m):
        k = barra_k.indice
        m = barra_m.indice
        if barra_k.tipo_barra != "VT" and barra_m.tipo_barra != "VT" and barra_m.tipo_barra != "PV":
            if k != m:
                return (self.G[k][m]*cos(barra_k.theta-barra_m.theta) + self.B[k][m]*sin(barra_k.theta-barra_m.theta))*barra_k.V

            elif k == m:
                return barra_k.V*self.G[k][m] + barra_k.P_calculado
            
        else:
            return 0
        
    def Lkm(self, barra_k, barra_m):
        k = barra_k.indice
        m = barra_m.indice
        if barra_k.tipo_barra != "VT" and barra_k.tipo_barra != "PV" and barra_m.tipo_barra != "VT" and barra_m.tipo_barra != "PV":
            if k != m:
                return (self.G[k][m]*sin(barra_k.theta-barra_m.theta) - self.B[k][m]*cos(barra_k.theta-barra_m.theta))*barra_k.V

            elif k == m:
                return -barra_k.V*self.B[k][m] + barra_k.Q_calculado
            
        else:
            return 0

    def popular_jacobiano(self):
        bus = len(self.barras)
        for barra_k in self.barras:
            for barra_m in self.barras:
                h = self.Hkm(barra_k,barra_m)
                n = self.Nkm(barra_k,barra_m)
                l = self.Lkm(barra_k,barra_m)
                k = barra_k.indice
                m = barra_m.indice

                self.jacobiano_base[k][m] = h
                self.jacobiano_base[k][m + bus] = n
                self.jacobiano_base[k + bus][m] = n
                self.jacobiano_base[k + bus][m + bus] = l

        print(self.jacobiano_base)
                




mu = Mundo()
mu.gerar_Ybarra()
mu.gerar_B_e_G()
mu.ler_tab_barras()
mu.P_e_Q()
mu.criar_jacobiano_base()
mu.popular_jacobiano()