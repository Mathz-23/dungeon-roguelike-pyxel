import random

import pyxel

from inimigos import Inimigo
from itens import sortear_item


TAMANHO_TELA = 256
ESPESSURA_PAREDE = 8
TAMANHO_PORTA = 40
INICIO_PORTA = (TAMANHO_TELA - TAMANHO_PORTA) // 2
FIM_PORTA = INICIO_PORTA + TAMANHO_PORTA


class Sala:
    def __init__(self, linha, coluna, tipo, numero_andar):
        self.linha = linha
        self.coluna = coluna
        self.tipo = tipo
        self.visitada = tipo == "inicial"
        self.concluida = tipo in ("inicial", "item")
        self.item_coletado = False
        self.bau_aberto = False
        self.item = None
        self.chave_no_chao = False
        self.cor_chao = random.choice((1, 5, 13))
        self.portas = {
            "cima": linha > 0,
            "baixo": linha < 2,
            "esquerda": coluna > 0,
            "direita": coluna < 2,
        }
        self.inimigos = self.gerar_inimigos(numero_andar)

    def criar_inimigo(self, numero_andar, elite=False, boss=False):
        while True:
            x = random.randint(30, 216)
            y = random.randint(30, 216)
            if not (90 < x < 166 and 90 < y < 166):
                break

        inimigo = Inimigo(x, y)

        if elite:
            inimigo.vida = 20 + numero_andar * 5
            inimigo.vida_max = inimigo.vida
            inimigo.dano = 12 + numero_andar * 2
            inimigo.cor = 9

        if boss:
            inimigo.vida = 50 + numero_andar * 15
            inimigo.vida_max = inimigo.vida
            inimigo.dano = 15 + numero_andar * 3
            inimigo.cor = 8
            inimigo.largura = 16
            inimigo.altura = 16
            inimigo.velocidade = 0.7

        return inimigo

    def gerar_inimigos(self, numero_andar):
        if self.tipo in ("inicial", "item"):
            return []

        if self.tipo == "elite":
            return [self.criar_inimigo(numero_andar, elite=True)]

        if self.tipo == "chave":
            return [
                self.criar_inimigo(numero_andar, elite=True),
                self.criar_inimigo(numero_andar, elite=True),
            ]

        if self.tipo == "boss":
            return [self.criar_inimigo(numero_andar, boss=True)]

        minimo = numero_andar + 1
        maximo = numero_andar * 2 + 1
        quantidade = random.randint(minimo, maximo)
        return [self.criar_inimigo(numero_andar) for _ in range(quantidade)]

    def draw(self, tem_chave):
        pyxel.cls(self.cor_chao)
        cor_parede = 6

        self.desenhar_parede_horizontal(0, "cima", cor_parede)
        self.desenhar_parede_horizontal(
            TAMANHO_TELA - ESPESSURA_PAREDE, "baixo", cor_parede
        )
        self.desenhar_parede_vertical(0, "esquerda", cor_parede)
        self.desenhar_parede_vertical(
            TAMANHO_TELA - ESPESSURA_PAREDE, "direita", cor_parede
        )

        if self.tipo == "item":
            if self.bau_aberto:
                pyxel.blt(120, 120, 1, 88, 108, 16, 16, 7)
            else:
                pyxel.blt(120, 124, 1, 69, 112, 16, 12, 7)
                pyxel.text(106, 142, "Pressione E", 7)

        if self.chave_no_chao:
            pyxel.blt(124, 124, 1, 70, 100, 8, 3, 7)

        if self.tipo == "boss" and self.concluida:
            cor_passagem = 11 if tem_chave else 8
            pyxel.circ(128, 128, 12, cor_passagem)
            pyxel.text(106, 145, "Pressione E", 7)

    def desenhar_parede_horizontal(self, y, direcao, cor):
        if self.portas[direcao]:
            pyxel.rect(0, y, INICIO_PORTA, ESPESSURA_PAREDE, cor)
            pyxel.rect(
                FIM_PORTA, y, TAMANHO_TELA - FIM_PORTA, ESPESSURA_PAREDE, cor
            )
        else:
            pyxel.rect(0, y, TAMANHO_TELA, ESPESSURA_PAREDE, cor)

    def desenhar_parede_vertical(self, x, direcao, cor):
        if self.portas[direcao]:
            pyxel.rect(x, 0, ESPESSURA_PAREDE, INICIO_PORTA, cor)
            pyxel.rect(
                x, FIM_PORTA, ESPESSURA_PAREDE, TAMANHO_TELA - FIM_PORTA, cor
            )
        else:
            pyxel.rect(x, 0, ESPESSURA_PAREDE, TAMANHO_TELA, cor)

class Andar:
    def __init__(self, numero, posicao_inicial):
        self.numero = numero
        self.posicao_inicial = posicao_inicial

        posicoes_livres = list(range(9))
        posicoes_livres.remove(posicao_inicial)
        random.shuffle(posicoes_livres)

        tipos = [
            "boss",
            "chave",
            "elite",
            "comum",
            "comum",
            "comum",
            "item",
            "item",
        ]

        tipos_por_posicao = {posicao_inicial: "inicial"}
        for posicao, tipo in zip(posicoes_livres, tipos):
            tipos_por_posicao[posicao] = tipo

        self.posicao_boss = next(
            posicao
            for posicao, tipo in tipos_por_posicao.items()
            if tipo == "boss"
        )

        self.salas = []
        for linha in range(3):
            fileira = []
            for coluna in range(3):
                posicao = linha * 3 + coluna
                tipo = tipos_por_posicao[posicao]
                fileira.append(Sala(linha, coluna, tipo, numero))
            self.salas.append(fileira)


class Mapa:
    def __init__(self):
        self.numero_andar = 1
        self.andares = []
        self.tem_chave = False
        self.jogo_concluido = False
        self.tempo_mensagem_chave = 0
        self.tempo_mensagem_item = 0
        self.mensagem_item = ""

        posicao_inicial = random.randint(0, 8)

        for numero in range(1, 6):
            andar = Andar(numero, posicao_inicial)
            self.andares.append(andar)
            posicao_inicial = andar.posicao_boss

        self.entrar_no_inicio_do_andar()

    @property
    def andar_atual(self):
        return self.andares[self.numero_andar - 1]

    @property
    def sala_atual(self):
        return self.andar_atual.salas[self.linha_atual][self.coluna_atual]

    def entrar_no_inicio_do_andar(self):
        posicao = self.andar_atual.posicao_inicial
        self.linha_atual = posicao // 3
        self.coluna_atual = posicao % 3
        self.sala_atual.visitada = True

    def tentar_mudar_sala(self, jogador):
        centro_x = jogador.x + jogador.largura / 2
        centro_y = jogador.y + jogador.altura / 2
        dentro_porta_x = INICIO_PORTA <= centro_x <= FIM_PORTA
        dentro_porta_y = INICIO_PORTA <= centro_y <= FIM_PORTA
        margem_entrada = ESPESSURA_PAREDE + 2

        if jogador.y <= 0 and jogador.dy < 0 and dentro_porta_x and self.sala_atual.portas["cima"]:
            self.linha_atual -= 1
            jogador.y = TAMANHO_TELA - jogador.altura - margem_entrada
        elif jogador.y + jogador.altura >= TAMANHO_TELA and jogador.dy > 0 and dentro_porta_x and self.sala_atual.portas["baixo"]:
            self.linha_atual += 1
            jogador.y = margem_entrada
        elif jogador.x <= 0 and jogador.dx < 0 and dentro_porta_y and self.sala_atual.portas["esquerda"]:
            self.coluna_atual -= 1
            jogador.x = TAMANHO_TELA - jogador.largura - margem_entrada
        elif jogador.x + jogador.largura >= TAMANHO_TELA and jogador.dx > 0 and dentro_porta_y and self.sala_atual.portas["direita"]:
            self.coluna_atual += 1
            jogador.x = margem_entrada
        else:
            self.bloquear_paredes(jogador, dentro_porta_x, dentro_porta_y)
            return False

        self.sala_atual.visitada = True
        return True

    def bloquear_paredes(self, jogador, dentro_porta_x, dentro_porta_y):
        sala = self.sala_atual
        limite = TAMANHO_TELA - ESPESSURA_PAREDE

        if jogador.y < ESPESSURA_PAREDE and not (sala.portas["cima"] and dentro_porta_x):
            jogador.y = ESPESSURA_PAREDE
        if jogador.y + jogador.altura > limite and not (sala.portas["baixo"] and dentro_porta_x):
            jogador.y = limite - jogador.altura
        if jogador.x < ESPESSURA_PAREDE and not (sala.portas["esquerda"] and dentro_porta_y):
            jogador.x = ESPESSURA_PAREDE
        if jogador.x + jogador.largura > limite and not (sala.portas["direita"] and dentro_porta_y):
            jogador.x = limite - jogador.largura

    def concluir_sala(self):
        sala = self.sala_atual

        if sala.concluida or sala.inimigos:
            return False

        sala.concluida = True

        if sala.tipo == "chave":
            sala.chave_no_chao = True

        return sala.tipo in ("comum", "elite", "chave", "boss")

    def abrir_bau(self, jogador):
        sala = self.sala_atual

        if self.tempo_mensagem_item > 0:
            self.tempo_mensagem_item -= 1

        if sala.tipo != "item" or sala.bau_aberto:
            return

        jogador_direita = jogador.x + jogador.largura
        jogador_baixo = jogador.y + jogador.altura
        perto_do_bau = (
            jogador.x < 140
            and jogador_direita > 116
            and jogador.y < 140
            and jogador_baixo > 116
        )

        if perto_do_bau and pyxel.btnp(pyxel.KEY_E):
            sala.bau_aberto = True
            sala.item = sortear_item(jogador)
            sala.item_coletado = sala.item.pegar(jogador)
            self.tempo_mensagem_item = 90

            if sala.item_coletado:
                self.mensagem_item = getattr(
                    sala.item,
                    "mensagem",
                    "Voce encontrou: " + sala.item.nome,
                )
            else:
                self.mensagem_item = "Voce ja possui este item"

    def coletar_chave(self, jogador):
        sala = self.sala_atual

        if not sala.chave_no_chao:
            return

        jogador_direita = jogador.x + jogador.largura
        jogador_baixo = jogador.y + jogador.altura

        encostou_na_chave = (
            jogador.x < 133
            and jogador_direita > 124
            and jogador.y < 133
            and jogador_baixo > 124
        )

        if encostou_na_chave:
            sala.chave_no_chao = False
            self.tem_chave = True

    def tentar_proximo_andar(self, jogador):
        sala = self.sala_atual

        if self.tempo_mensagem_chave > 0:
            self.tempo_mensagem_chave -= 1

        if sala.tipo != "boss" or not sala.concluida:
            return False

        jogador_direita = jogador.x + jogador.largura
        jogador_baixo = jogador.y + jogador.altura
        perto_da_passagem = (
            jogador.x < 140
            and jogador_direita > 116
            and jogador.y < 140
            and jogador_baixo > 116
        )

        if not perto_da_passagem:
            return False

        if not pyxel.btnp(pyxel.KEY_E):
            return False

        if not self.tem_chave:
            self.tempo_mensagem_chave = 90
            return False

        if self.numero_andar == 5:
            self.jogo_concluido = True
            return True

        self.numero_andar += 1
        self.tem_chave = False
        self.entrar_no_inicio_do_andar()
        jogador.x = 123
        jogador.y = 123
        return True

    def draw(self):
        self.sala_atual.draw(self.tem_chave)

        if self.tempo_mensagem_chave > 0:
            mensagem = "A porta esta trancada, a chave esta com algum dos guardas"
            pyxel.rect(5, 173, 246, 15, 0)
            pyxel.text(11, 178, mensagem, 7)

        if self.tempo_mensagem_item > 0:
            pyxel.rect(35, 173, 186, 15, 0)
            pyxel.text(43, 178, self.mensagem_item, 7)

    def draw_minimapa(self):
        tamanho = 5
        espacamento = 1
        inicio_x = 234
        inicio_y = 6

        for linha, fileira in enumerate(self.andar_atual.salas):
            for coluna, sala in enumerate(fileira):
                if not sala.visitada:
                    continue

                cor = 10 if linha == self.linha_atual and coluna == self.coluna_atual else 7
                x = inicio_x + coluna * (tamanho + espacamento)
                y = inicio_y + linha * (tamanho + espacamento)
                pyxel.rect(x, y, tamanho, tamanho, cor)

        pyxel.text(202, 27, "Andar " + str(self.numero_andar), 7)
