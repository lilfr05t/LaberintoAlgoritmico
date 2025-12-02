import os
import csv
import time

ARCHIVO = 'leaderboard.csv'

def guardar_datos(jugador, filas, tiempo):
    existe = os.path.isfile(ARCHIVO)
    with open(ARCHIVO, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not existe: writer.writerow(["Jugador", "Grid_Size", "Tiempo (s)", "Fecha"])
        writer.writerow([jugador, f"{filas}x{filas}", f"{tiempo:.3f}", time.strftime("%Y-%m-%d %H:%M:%S")])
    print(f"Datos guardados: {jugador}")

def obtener_ranking():
    datos = []
    if not os.path.isfile(ARCHIVO): return []
    try:
        with open(ARCHIVO, mode='r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader: datos.append(row)
        datos.sort(key=lambda x: float(x[2]))
        return datos[:10]
    except: return []