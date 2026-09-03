class Entidade:
    def __init__(self, x, y, raio, vida):
        self.x = x
        self.y = y
        self.raio = raio
        
        self.vida = vida
        self.vida_max = vida
        
        
        #recebido
        self.ultimo_dano = 0
        self.tempo_dano = 0
    
    def receber_dano(self, dano):
        self.vida -= dano
        
        self.ultimo_dano = dano
        self.tempo_dano = 20
    
    def esta_vivo(self):
        return self.vida > 0
        