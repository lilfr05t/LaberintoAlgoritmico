import pygame

# Geometría
ANCHO_MENU = 250
ANCHO_GRID = 600
ALTO_VENTANA = ANCHO_GRID
ANCHO_TOTAL = ANCHO_MENU + ANCHO_GRID

# Variables iniciales
FILAS_INICIALES = 40
ANCHO_NODO_INICIAL = ANCHO_GRID // FILAS_INICIALES

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (50, 50, 50)
GRIS_BOTON = (100, 100, 100)
VERDE_BOTON = (0, 200, 0)
NARANJA = (255, 165, 0)
TURQUESA = (64, 224, 208)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
MORADO = (128, 0, 128)
AMARILLO = (255, 255, 0)

# Fuentes (Se inicializan después de pygame.init en main, pero definimos nombres)
def init_fuentes():
    return {
        'titulo': pygame.font.SysFont('arial', 30, bold=True),
        'texto': pygame.font.SysFont('arial', 18),
        'boton': pygame.font.SysFont('arial', 20, bold=True),
        'modo': pygame.font.SysFont('arial', 30, bold=True),
        'exito': pygame.font.SysFont('arial', 40, bold=True)
    }