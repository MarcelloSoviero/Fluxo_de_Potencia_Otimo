class Barra:
    def __init__(self, indice, tipo_barra, P, Q, V, theta, conexoes, shunts):
        self.indice = indice
        self.tipo_barra = tipo_barra
        self.P = P
        self.Q = Q
        self.V = V
        self.theta = theta
        self.conexoes = conexoes
        self.shunts = shunts
        self.delta_P = None
        self.delta_Q = None
        self.P_calculado = None
        self.Q_calculado = None

    def minha_func(self):
        self.indice
        
    def __str__(self):
        return "Barra {} de indice {}".format(self.tipo_barra,self.indice)