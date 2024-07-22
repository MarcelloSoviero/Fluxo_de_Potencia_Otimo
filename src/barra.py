class Barra:
    def __init__(self, indice, tipo_barra, dado1, dado2, conexoes, shunts):
        self.indice = indice
        self.tipo_barra = tipo_barra
        self.dado1 = dado1
        self.dado2 = dado2
        self.conexoes = conexoes
        self.shunts = shunts

    def minha_func(self):
        self.indice
        
    def __str__(self):
        return "Barra {} de indice {}".format(self.tipo_barra,self.indice)