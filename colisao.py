import math


def limitar_tela(entidade, largura=256, altura=256):

    if entidade.x - entidade.raio < 0:
        entidade.x = entidade.raio

    if entidade.x + entidade.raio > largura - 1:
        entidade.x = largura - 1 - entidade.raio

    if entidade.y - entidade.raio < 0:
        entidade.y = entidade.raio

    if entidade.y + entidade.raio > altura - 1:
        entidade.y = altura - 1 - entidade.raio


def distancia(a, b):

    dx = b.x - a.x
    dy = b.y - a.y

    return math.sqrt(dx**2 + dy**2)


def colidiu(a, b, margem=0):

    distancia_atual = distancia(a, b)

    distancia_minima = a.raio + b.raio + margem

    return distancia_atual < distancia_minima