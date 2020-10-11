from terminal import timed_input, clear_terminal
def partida_perdida(posicion_serpiente, movimiento_actual, nueva_posicion_cabeza, obstaculos, filas, columnas):
	"""Devuelve True si la serpiente choca con los bordes del mapa, si se come a si misma o si chocó con 
	un obstáculo, es decir, devuelve True si perdio el jugador."""
	en_primera_fila = posicion_serpiente[0] in [[0,i] for i in range(columnas)]
	en_ultima_fila = posicion_serpiente[0] in [[filas-1,i] for i in range(filas)]
	en_primera_columna = posicion_serpiente[0] in [[i,0] for i in range(filas)]
	en_ultima_columna = posicion_serpiente[0] in [[i,columnas-1] for i in range(filas)]
	choco_obstaculo = nueva_posicion_cabeza in obstaculos	

	return any((en_primera_fila and movimiento_actual == "w", en_ultima_fila and movimiento_actual == "s", 
	en_primera_columna and movimiento_actual == "a", en_ultima_columna and movimiento_actual == "d",
	nueva_posicion_cabeza in posicion_serpiente[:-1] and len(posicion_serpiente) > 2,
	nueva_posicion_cabeza in posicion_serpiente and len(posicion_serpiente) == 2, choco_obstaculo))
	
def nivel_ganado(posicion_serpiente, largo_max_serpiente):
	"""Devuelve True si el jugador alcanzó el largo objetivo de la serpiente en dicho nivel."""
	return largo_max_serpiente == len(posicion_serpiente)

def presentar_nivel():
	"""Informa al usuario (imprime) de que está por comenzar un nuevo nivel."""
	clear_terminal()
	print("¡Está por comenzar el próximo nivel!")
	timed_input(2)
	for i in "321":
		clear_terminal()
		print(f"---{i}---")
		timed_input(1)