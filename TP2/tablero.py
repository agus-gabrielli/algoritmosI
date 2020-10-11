from random import randint
def crear_tablero(posicion_serpiente, obstaculos, filas, columnas):
	"""Crea el tablero del juego, que contiene a los espacios vacíos, frutas y serpiente. Se llama únicamente al 
	principio de cada partida. También coloca a la serpiente por primera vez en el mismo."""
	color_amarillo = '\033[33m'
	color_normal = '\033[0m'
	tablero_juego = []
	estructura_tablero = [] #no se va a modificar durante el juego
	for i in range(filas):
		estructura_tablero.append([])
		tablero_juego.append([])
		
		for j in range(columnas):
			if j == columnas-1: tablero_juego[i].append(" "); continue
			if i == filas-1: estructura_tablero[i].append(" "); tablero_juego[i].append(" "); continue
			estructura_tablero[i].append(".")
			tablero_juego[i].append(" ")
	tablero_juego[posicion_serpiente[0][0]][posicion_serpiente[0][1]] = "o"
	for i in range(len(obstaculos)):
		tablero_juego[obstaculos[i][0]][obstaculos[i][1]] = color_amarillo + "O" + color_normal #agrego los obstáculos
	return tablero_juego, estructura_tablero
		
def imprimir_tablero(estructura_tablero, tablero_juego, filas, columnas):
	"""Imprime el tablero del juego."""
	for i in range(filas):	
		for j in range(columnas):	
			print(tablero_juego[i][j], end="")
			if j == columnas-1: continue
			print(estructura_tablero[i][j], end="")
		print()

def esta_contenido_o_igual(lista1, lista2):
	"""Devuelve True si lista1 está contenidaen la lista2 que contiene 1 o más listas, o si lista1 es igual la lista
	que contiene lista2."""
	if len(lista2) == 1: return [lista1] == lista2
	return any(lista1 == sublista2 for sublista2 in lista2)

def colocar_fruta(tablero_juego, posicion_serpiente, obstaculos, filas, columnas, posicion_especial):
	"""Coloca una nueva fruta en el mapa y devuelve su posición en el tablero. Si la posicion nueva de la fruta cae sobre 
	la serpiente, se anula y calcula nuevamente una posicion hasta que no caiga sobre la serpiente.""" 
	color_rojo = '\033[91m'
	color_normal = '\033[0m'
	while True:	
		posicion_fruta = [randint(0, filas-1), randint(0, columnas-1)]
		if not any((esta_contenido_o_igual(posicion_fruta,posicion_serpiente), 
		esta_contenido_o_igual(posicion_fruta,obstaculos),
		esta_contenido_o_igual(posicion_fruta,posicion_especial))): break
	tablero_juego[posicion_fruta[0]][posicion_fruta[1]] = color_rojo + "ర"  + color_normal
	return posicion_fruta