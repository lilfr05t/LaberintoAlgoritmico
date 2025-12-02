import pygame
import sys
import time
from configuracion import *
from modelos import Boton, crear_grid
from ui import dibujar_ventana_completa, dibujar_tabla_ranking, mostrar_mensaje
from data import obtener_ranking, guardar_datos
from algoritmos import algoritmo_dijkstra, algoritmo_a_star, generar_laberinto
from modelos import Nodo


def interpolar_puntos(p1, p2):
    """Genera una lista de coordenadas (fila, col) entre dos puntos."""
    f1, c1 = p1
    f2, c2 = p2
    puntos = []

    # Distancia en ambos ejes
    df = f2 - f1
    dc = c2 - c1

    # Cuántos pasos necesitamos (el máximo de las dos distancias)
    pasos = max(abs(df), abs(dc))

    if pasos == 0: return []

    for i in range(1, pasos + 1):
        # Fórmula de interpolación lineal (Lerp)
        t = i / pasos
        f = int(f1 + df * t)
        c = int(c1 + dc * t)
        puntos.append((f, c))

    return puntos

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
            boton_jugar.texto = "ABANDONAR"
            boton_jugar.color = ROJO
            start_time = time.time()
            for f in grid:
                for n in f:
                    if not n.es_muro() and not n.es_inicio() and not n.es_fin(): n.reset()
        else:
            boton_jugar.texto = "JUGAR"
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

    nodo_previo = None
    corriendo = True
    while corriendo:
        t_trans = time.time() - start_time if jugando else 0

        dibujar_ventana_completa(VENTANA, grid, botones, jugando, FUENTES, t_trans, actualizar=not viendo_ranking)
        if viendo_ranking: dibujar_tabla_ranking(VENTANA, ranking_data, FUENTES)
        if not pygame.mouse.get_pressed()[0]:
            nodo_previo = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT: corriendo = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x_click, y_click = pos
                if pos[0] < ANCHO_MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if jugando:
                            boton_jugar.es_click(pos)
                        else:
                            for b in botones: b.es_click(pos)
                elif not viendo_ranking:
                    f, c = get_pos_click(pos, filas_actuales, ancho_nodo)
                    if 0 <= f < filas_actuales and 0 <= c < filas_actuales:
                        nodo_actual = grid[f][c]
                        if jugando:

                            nodos_a_pintar = []
                            if nodo_previo and nodo_previo != nodo_actual:
                                coordenadas = interpolar_puntos(nodo_previo.get_pos(), nodo_actual.get_pos())
                                for cf, cc in coordenadas:
                                    nodos_a_pintar.append(grid[cf][cc])
                            else:
                                nodos_a_pintar.append(nodo_actual)

                                # Procesamos cada nodo de la lista (pintar o ganar)
                            for nodo in nodos_a_pintar:
                                # TU VALIDACIÓN ORIGINAL DE VECINOS Y PAREDES
                                # (Adaptada para chequear cada nodo de la línea)
                                if nodo.es_muro(): continue  # No atravesar muros

                                # Verificamos si podemos conectar (adyacencia)
                                es_valido = False
                                for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                    nf, nc = nodo.fila + df, nodo.col + dc
                                    if 0 <= nf < filas_actuales and 0 <= nc < filas_actuales:
                                        vecino = grid[nf][nc]
                                        # Conectamos si el vecino es inicio, camino o el nodo previo recién pintado
                                        if vecino.color in [ROJO, NARANJA]:
                                            es_valido = True
                                            break

                                if es_valido:
                                    if nodo == fin:
                                        # ... (TU CÓDIGO DE VICTORIA) ...
                                        t_fin = time.time() - start_time
                                        if generado: guardar_datos("Humano", filas_actuales, t_fin, 0,
                                                                   current_maze_id)  # Ajusta nodos si quieres
                                        mostrar_mensaje(VENTANA, f"Ganaste: {t_fin:.2f}s", FUENTES)
                                        toggle_juego()
                                        nodo_previo = None  # Reset
                                        break  # Salir del for
                                    elif nodo != inicio:
                                        nodo.hacer_camino_usuario()

                                # Guardamos el último nodo procesado como el previo para el siguiente frame
                            if jugando:  # Chequeo extra por si ganó en el bucle
                                nodo_previo = nodo_actual
                        else:
                            # Logica Editor
                            if not inicio and nodo_actual != fin:
                                inicio = nodo_actual
                                inicio.hacer_inicio()
                            elif not fin and nodo_actual != inicio:
                                fin = nodo_actual
                                fin.hacer_fin()
                            elif nodo_actual != fin and nodo_actual != inicio:
                                nodo_actual.hacer_muro()
                                generado = False

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

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()