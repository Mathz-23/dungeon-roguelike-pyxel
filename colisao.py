import math


def limitar_tela(entidade, largura=256, altura=256):

    if entidade.x < 0:
        entidade.x = 0

    if entidade.x + entidade.largura > largura:
        entidade.x = largura - entidade.largura

    if entidade.y < 0:
        entidade.y = 0

    if entidade.y + entidade.altura > altura:
        entidade.y = altura - entidade.altura


def distancia(a, b):
    centro_ax = a.x + a.largura / 2
    centro_ay = a.y + a.altura / 2
    
    centro_bx = b.x + b.largura / 2
    centro_by = b.y + b.altura / 2


    dx = centro_bx - centro_ax
    dy = centro_by - centro_ay

    return math.sqrt(dx**2 + dy**2)


def colidiu(a, b, margem=0):
    return(
        a.x < b.x + b.largura + margem 
        and a.x + a.largura + margem > b.x 
        and a.y < b.y + b.altura + margem 
        and a.y + a.altura + margem > b.y
    )
    
def ataque_colidiu(area, entidade):
    x, y, largura, altura = area
    return(
        x < entidade.x + entidade.largura
        and x + largura > entidade.x
        and y < entidade.y + entidade.altura
        and y + altura > entidade.y
    )
