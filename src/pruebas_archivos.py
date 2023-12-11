import json

# Obtén el nombre y el puntaje del jugador (puedes modificar esto según tu implementación)
nombre_jugador = input("Ingresa tu nombre: ")
puntaje_jugador = int(input("Ingresa tu puntaje: "))

# Crea un diccionario con la información del jugador
info_jugador = {"nombre": nombre_jugador, "puntaje": puntaje_jugador}

# Intenta cargar el archivo JSON existente
try:
    with open("puntajes.json", "r") as file:
        puntajes = json.load(file)
except FileNotFoundError:
    # Si el archivo no existe, crea una lista vacía
    puntajes = []

# Agrega la información del jugador a la lista de puntajes
puntajes.append(info_jugador)

# Guarda la lista actualizada en el archivo JSON
with open("puntajes.json", "w") as file:
    json.dump(puntajes, file)

print("Puntaje guardado correctamente.")