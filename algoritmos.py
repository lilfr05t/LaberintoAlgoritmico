import pygame
import heapq
import random
import sys
import time
from ui import mostrar_mensaje
from data import guardar_datos


def h(p1, p2):  # Heurística Manhattan
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def reconstruir_camino(came_from, actual, draw):
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        draw()


def algoritmo_base(tipo, draw, grid, inicio, fin, start_time, fuentes, win, guardar=False):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, inicio))
    came_from = {}

    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0

    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = h(inicio.get_pos(), fin.get_pos())

    open_set_hash = {inicio}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        actual = heapq.heappop(open_set)[2]
        open_set_hash.remove(actual)

        if actual == fin:
            end_time = time.time()
            total_time = end_time - start_time
            reconstruir_camino(came_from, fin, draw)
            fin.hacer_fin()
            if guardar: guardar_datos(f"Algoritmo {tipo}", len(grid), total_time)
            mostrar_mensaje(win, f"{tipo}: {total_time:.2f}s", fuentes)
            return True

        for vecino in actual.vecinos:
            temp_g = g_score[actual] + 1
            if temp_g < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = temp_g

                prioridad = temp_g  # Default Dijkstra
                if tipo == "A*":
                    f_score[vecino] = temp_g + h(vecino.get_pos(), fin.get_pos())
                    prioridad = f_score[vecino]

                if vecino not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (prioridad, count, vecino))
                    open_set_hash.add(vecino)
                    vecino.hacer_abierto()

        draw(time.time() - start_time)
        if actual != inicio: actual.hacer_cerrado()
    return False


def algoritmo_dijkstra(draw, grid, inicio, fin, start, fuentes, win, guardar):
    return algoritmo_base("Dijkstra", draw, grid, inicio, fin, start, fuentes, win, guardar)


def algoritmo_a_star(draw, grid, inicio, fin, start, fuentes, win, guardar):
    return algoritmo_base("A*", draw, grid, inicio, fin, start, fuentes, win, guardar)


def generar_laberinto(draw, grid, filas):
    for fila in grid:
        for nodo in fila: nodo.hacer_muro()
    draw()
    actual = grid[1][1];
    actual.reset()
    stack = [actual]

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        actual = stack[-1]
        vecinos = []
        for df, dc in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
            nf, nc = actual.fila + df, actual.col + dc
            if 0 <= nf < filas and 0 <= nc < filas:
                v = grid[nf][nc]
                if v.es_muro(): vecinos.append(v)

        if vecinos:
            sig = random.choice(vecinos)
            grid[(actual.fila + sig.fila) // 2][(actual.col + sig.col) // 2].reset()
            sig.reset()
            stack.append(sig)
            # draw()
        else:
            stack.pop()
    draw()

    celdas = [n for fila in grid for n in fila if not n.es_muro()]
    if not celdas: return None, None
    inicio = random.choice(celdas);
    inicio.hacer_inicio()

    cand = sorted([(abs(n.fila - inicio.fila) + abs(n.col - inicio.col), n) for n in celdas if n != inicio],
                  key=lambda x: x[0], reverse=True)
    fin = cand[random.randint(0, max(0, len(cand) // 10))][1]
    fin.hacer_fin()
    draw()
    return inicio, fin