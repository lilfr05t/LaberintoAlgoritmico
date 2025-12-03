import pygame
from configuracion import *


def dibujar_grid_lineas(win, filas, ancho):
    for i in range(filas + 1):
        pygame.draw.line(win, GRIS_CLARO, (ANCHO_MENU, i * ancho), (ANCHO_TOTAL, i * ancho))
        x_pos = (i * ancho) + ANCHO_MENU
        pygame.draw.line(win, GRIS_CLARO, (x_pos, 0), (x_pos, ALTO_VENTANA))


def mostrar_mensaje(win, texto, fuentes):
    superficie = fuentes['exito'].render(texto, True, (50, 50, 50))
    centro_x = ANCHO_MENU + (ANCHO_GRID // 2)
    centro_y = ALTO_VENTANA // 2
    rect = superficie.get_rect(center=(centro_x, centro_y))

    s = pygame.Surface((ANCHO_GRID, 100))
    s.set_alpha(200)
    s.fill(GRIS_CLARO)
    win.blit(s, (ANCHO_MENU, centro_y - 50))
    win.blit(superficie, rect)
    pygame.display.update()
    pygame.time.delay(2000)


def dibujar_ventana_completa(win, grid, botones, modo_juego, fuentes, tiempo_actual=0, actualizar=True):
    win.fill(BLANCO)
    for fila in grid:
        for nodo in fila: nodo.dibujar(win)
    dibujar_grid_lineas(win, len(grid), grid[0][0].ancho)

    # Panel Lateral
    pygame.draw.rect(win, GRIS_OSCURO, (0, 0, ANCHO_MENU, ALTO_VENTANA))
    win.blit(fuentes['titulo'].render("CONTROLES", True, BLANCO), (20, 380))

    # Timer
    pygame.draw.rect(win, NEGRO, (20, 70, 160, 40), border_radius=5)
    win.blit(fuentes['boton'].render(f"T: {tiempo_actual:.2f} s", True, BLANCO), (35, 80))

    # Estado
    est = "MODO: JUEGO" if modo_juego else "MODO: EDITOR"
    col = AMARILLO if modo_juego else TURQUESA
    win.blit(fuentes['modo'].render(est, True, col), (17, 30))

    # Instrucciones
    instrucciones = ["Click Izq: Pintar", "  (Naranja:Inicio | Azul:Final)", "Click Der: Borrar", "Espacio: Dijkstra", "A: A* (Star)",
                     "G: Generar Laberinto", "C: Limpiar Todo"]
    y_off = 420
    for linea in instrucciones:
        win.blit(fuentes['texto'].render(linea, True, BLANCO), (20, y_off))
        y_off += 25

    for boton in botones: boton.dibujar(win, fuentes['boton'])

    if actualizar: pygame.display.update()


def dibujar_tabla_ranking(win, page_data, pag_actual, total_pags, botones_nav, confirmando, botones_conf, fuentes):
    rect = pygame.Rect(ANCHO_MENU, 0, ANCHO_GRID, ALTO_VENTANA)
    pygame.draw.rect(win, (30, 30, 40), rect)
    win.blit(fuentes['exito'].render("TIEMPOS Y NODOS", True, BLANCO), (ANCHO_MENU + 20, 50))

    encabezados = ["Jugador", "Nodos", "Tiempo", "ID"]
    x_pos = [ANCHO_MENU + 20, ANCHO_MENU + 200, ANCHO_MENU + 300, ANCHO_MENU + 450]
    y = 150
    for i, t in enumerate(encabezados):
        win.blit(fuentes['boton'].render(t, True, TURQUESA), (x_pos[i], y))

    pygame.draw.line(win, BLANCO, (ANCHO_MENU + 20, y + 30), (ANCHO_TOTAL - 20, y + 30), 2)
    y += 50

    for i, fila in enumerate(page_data):
        jugador_corto = fila[0].replace("Algoritmo ", "")
        nodos = fila[3]
        tiempo = f"{fila[2]}s"
        maze_id = fila[4]

        col = VERDE if "Humano" in fila[0] else NARANJA
        datos = [jugador_corto, nodos, tiempo, maze_id]
        colores = [col, BLANCO, BLANCO, GRIS_CLARO]

        for j, val in enumerate(datos):
            win.blit(fuentes['texto'].render(str(val), True, colores[j]), (x_pos[j], y))
        y += 35

    txt_pag = f"Página {pag_actual + 1} de {total_pags}"
    win.blit(fuentes['texto'].render(txt_pag, True, BLANCO), (ANCHO_MENU + ANCHO_GRID // 2 - 50, 560))

    if pag_actual > 0:
        botones_nav[0].dibujar(win, fuentes['boton'])

    if pag_actual < total_pags - 1:
        botones_nav[1].dibujar(win, fuentes['boton'])

    botones_nav[2].dibujar(win, fuentes['boton'])

    if confirmando:
        # Fondo semitransparente para bloquear el resto
        s = pygame.Surface((ANCHO_TOTAL, ALTO_VENTANA))
        s.set_alpha(200);
        s.fill(NEGRO)
        win.blit(s, (0, 0))

        # Cuadro de diálogo
        cx, cy = ANCHO_TOTAL // 2, ALTO_VENTANA // 2
        rect_pop = pygame.Rect(cx - 150, cy - 80, 300, 160)
        pygame.draw.rect(win, GRIS_OSCURO, rect_pop, border_radius=10)
        pygame.draw.rect(win, BLANCO, rect_pop, 2, border_radius=10)

        win.blit(fuentes['titulo'].render("¿Borrar todo?", True, BLANCO), (rect_pop.x + 60, rect_pop.y + 30))

        # Botones Sí/No
        for b in botones_conf: b.dibujar(win, fuentes['boton'])
    pygame.display.update()

