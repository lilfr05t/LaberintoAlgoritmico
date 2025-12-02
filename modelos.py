import pygame
from configuracion import *

class Boton:
    def __init__(self, x, y, ancho, alto, texto, funcion_callback=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = GRIS_BOTON
        self.funcion = funcion_callback

    def dibujar(self, win, fuente):
        pygame.draw.rect(win, self.color, self.rect, border_radius=5)
        pygame.draw.rect(win, BLANCO, self.rect, 2, border_radius=5)
        texto_render = fuente.render(self.texto, True, BLANCO)
        x_txt = self.rect.x + (self.rect.width - texto_render.get_width()) // 2
        y_txt = self.rect.y + (self.rect.height - texto_render.get_height()) // 2
        win.blit(texto_render, (x_txt, y_txt))

    def es_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.funcion: self.funcion()
            return True
        return False

class Nodo:
    def __init__(self, fila, col, ancho):
        self.fila = fila
        self.col = col
        self.x = (col * ancho) + ANCHO_MENU
        self.y = fila * ancho
        self.color = BLANCO
        self.vecinos = []
        self.ancho = ancho

    def get_pos(self): return self.fila, self.col
    def es_muro(self): return self.color == NEGRO
    def es_inicio(self): return self.color == NARANJA
    def es_fin(self): return self.color == TURQUESA
    def hacer_inicio(self): self.color = NARANJA
    def hacer_muro(self): self.color = NEGRO
    def hacer_fin(self): self.color = TURQUESA
    def hacer_cerrado(self): self.color = ROJO
    def hacer_abierto(self): self.color = VERDE
    def hacer_camino(self): self.color = MORADO
    def hacer_camino_usuario(self):
        if not self.es_muro() and not self.es_inicio(): self.color = ROJO
    def reset(self): self.color = BLANCO
    def dibujar(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid, total_filas):
        self.vecinos = []
        if self.fila < total_filas - 1 and not grid[self.fila + 1][self.col].es_muro(): # Abajo
            self.vecinos.append(grid[self.fila + 1][self.col])
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_muro(): # Arriba
            self.vecinos.append(grid[self.fila - 1][self.col])
        if self.col < total_filas - 1 and not grid[self.fila][self.col + 1].es_muro(): # Der
            self.vecinos.append(grid[self.fila][self.col + 1])
        if self.col > 0 and not grid[self.fila][self.col - 1].es_muro(): # Izq
            self.vecinos.append(grid[self.fila][self.col - 1])

def crear_grid(filas, ancho):
    grid = []
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho)
            grid[i].append(nodo)
    return grid