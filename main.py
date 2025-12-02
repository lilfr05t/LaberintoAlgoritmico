import pygame
import sys
import time
from configuracion import *
from modelos import Boton, crear_grid
from ui import dibujar_ventana_completa, dibujar_tabla_ranking, mostrar_mensaje
from data import obtener_ranking, guardar_datos
from algoritmos import algoritmo_dijkstra, algoritmo_a_star, generar_laberinto
from modelos import Nodo


def get_pos_click(pos, filas, ancho):
    x, y = pos
    if x < ANCHO_MENU: return -1, -1
    return y // ancho, (x - ANCHO_MENU) // ancho


def main():
    pygame.init()
    VENTANA = pygame.display.set_mode((ANCHO_TOTAL, ALTO_VENTANA))
    pygame.display.set_caption("Visualizador Final")
    FUENTES = init_fuentes()

    filas_actuales = FILAS_INICIALES
    ancho_nodo = ANCHO_NODO_INICIAL

    grid = crear_grid(filas_actuales, ancho_nodo)
    inicio = None;
    fin = None
    jugando = False;
    generado = False;
    viendo_ranking = False
    ranking_data = []
    start_time = 0
    current_maze_id = "Manual"

    def cambiar_tamano():
        nonlocal grid, inicio, fin, filas_actuales, ancho_nodo
        if jugando: return

        filas_actuales = 20 if filas_actuales > 50 else filas_actuales + 10
        ancho_nodo = ANCHO_GRID // filas_actuales

        grid = crear_grid(filas_actuales, ancho_nodo)
        inicio = None;
        fin = None
        boton_tamano.texto = f"Grid: {filas_actuales}x{filas_actuales}"

    def toggle_juego():
        nonlocal jugando, start_time
        if not inicio or not fin:
            mostrar_mensaje(VENTANA, "¡Falta Inicio/Fin!", FUENTES)
            return

        jugando = not jugando
        if jugando:
            boton_jugar.texto = "ABANDONAR";
            boton_jugar.color = ROJO
            start_time = time.time()
            for f in grid:
                for n in f:
                    if not n.es_muro() and not n.es_inicio() and not n.es_fin(): n.reset()
        else:
            boton_jugar.texto = "JUGAR";
            boton_jugar.color = VERDE_BOTON

    def toggle_ranking():
        nonlocal viendo_ranking, ranking_data
        if jugando: return
        viendo_ranking = not viendo_ranking
        if viendo_ranking:
            ranking_data = obtener_ranking()
            boton_ranking.texto = "VOLVER"
        else:
            boton_ranking.texto = "RANKING"

    boton_tamano = Boton(20, 150, 200, 50, f"Grid: {filas_actuales}x{filas_actuales}", cambiar_tamano)
    boton_jugar = Boton(20, 230, 200, 50, "JUGAR", toggle_juego)
    boton_jugar.color = VERDE_BOTON
    boton_ranking = Boton(20, 310, 200, 50, "RANKING", toggle_ranking)
    botones = [boton_tamano, boton_jugar, boton_ranking]

    corriendo = True
    while corriendo:
        t_trans = time.time() - start_time if jugando else 0

        dibujar_ventana_completa(VENTANA, grid, botones, jugando, FUENTES, t_trans, actualizar=not viendo_ranking)
        if viendo_ranking: dibujar_tabla_ranking(VENTANA, ranking_data, FUENTES)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: corriendo = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] < ANCHO_MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if jugando:
                            boton_jugar.es_click(pos)
                        else:
                            for b in botones: b.es_click(pos)
                elif not viendo_ranking:
                    f, c = get_pos_click(pos, filas_actuales, ancho_nodo)
                    if 0 <= f < filas_actuales and 0 <= c < filas_actuales:
                        nodo = grid[f][c]
                        if jugando:
                            # Logica Humano (simplificada aqui)
                            valido = False
                            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                nf, nc = f + df, c + dc
                                if 0 <= nf < filas_actuales and 0 <= nc < filas_actuales:
                                    if grid[nf][nc].color in [ROJO, NARANJA]: valido = True

                            if valido:
                                if nodo == fin:
                                    t_fin = time.time() - start_time
                                    nodos_recorridos = 0
                                    for row in grid:
                                        for n in row:

                                            if n.color == ROJO:
                                                nodos_recorridos += 1
                                    if generado: guardar_datos("Humano", filas_actuales, t_fin, nodos_recorridos, current_maze_id)
                                    mostrar_mensaje(VENTANA, f"Ganaste: {t_fin:.2f}s", FUENTES)
                                    toggle_juego()
                                elif not nodo.es_muro() and nodo != inicio:
                                    nodo.hacer_camino_usuario()
                        else:
                            # Logica Editor
                            if not inicio and nodo != fin:
                                inicio = nodo; inicio.hacer_inicio()
                            elif not fin and nodo != inicio:
                                fin = nodo; fin.hacer_fin()
                            elif nodo != fin and nodo != inicio:
                                nodo.hacer_muro(); generado = False

            elif pygame.mouse.get_pressed()[2]:  # Clic Derecho (Borrar)
                if not jugando and not viendo_ranking:
                    pos = pygame.mouse.get_pos()
                    f, c = get_pos_click(pos, filas_actuales, ancho_nodo)

                    # Verificar que el clic sea válido dentro del grid
                    if 0 <= f < filas_actuales and 0 <= c < filas_actuales:
                        nodo = grid[f][c]
                        nodo.reset()  # Borrar (poner en blanco)

                        # Si borramos inicio o fin, reseteamos las referencias
                        if nodo == inicio:
                            inicio = None
                        elif nodo == fin:
                            fin = None

                        # Si modificamos manualmente, ya no es un laberinto generado
                        generado = False

            if event.type == pygame.KEYDOWN and not jugando and not viendo_ranking:
                if inicio and fin:
                    draw_func = lambda t=0: dibujar_ventana_completa(VENTANA, grid, botones, jugando, FUENTES, t)
                    for f in grid:
                        for n in f: n.actualizar_vecinos(grid, filas_actuales)

                    if event.key == pygame.K_SPACE:

                        algoritmo_dijkstra(draw_func, grid, inicio, fin, time.time(), FUENTES, VENTANA, generado,
                                           current_maze_id)
                    if event.key == pygame.K_a:
                        algoritmo_a_star(draw_func, grid, inicio, fin, time.time(), FUENTES, VENTANA, generado,
                                         current_maze_id)

                if event.key == pygame.K_g:
                    generado = True;
                    inicio = None;
                    fin = None
                    inicio, fin, current_maze_id = (generar_laberinto(
                        lambda: dibujar_ventana_completa(VENTANA, grid, botones, jugando, FUENTES), grid, filas_actuales))

                if event.key == pygame.K_c:
                    generado = False;
                    inicio = None;
                    fin = None
                    current_maze_id = "Manual"
                    grid = crear_grid(filas_actuales, ancho_nodo)

    pygame.quit();
    sys.exit()


if __name__ == "__main__":
    main()