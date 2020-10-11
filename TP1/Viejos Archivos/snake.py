from terminal import timed_input, clear_terminal
from random import randint

FILAS_TABLERO = 35
COLUMNAS_TABLERO = 70
LARGO_MAX_SERPIENTE = 500 #largo para ganar. Minimo 2
SEGUNDOS_POR_MOVIMIENTO = 0.04

def main():
	"""Es la función principal, desde la cual se llaman a todas las funciones que permiten 
	el funcionamiento del juego."""
	seguir_jugando = True
	while(seguir_jugando):	
		posicion_serpiente = [[FILAS_TABLERO//2, COLUMNAS_TABLERO//2]]
		estructura_tablero = [] #no se va a modificar durante el juego
		tablero = [] #contiene a los espacios vacíos, frutas y serpiente
		crear_tablero(estructura_tablero, tablero, posicion_serpiente)
		posicion_fruta = colocar_fruta(tablero, posicion_serpiente)
		movimiento_anterior = "w" #primer movimiento de la serpiente por default 	
		
		while True:
			clear_terminal()
			imprimir_tablero(estructura_tablero, tablero)
			movimiento = timed_input(SEGUNDOS_POR_MOVIMIENTO)
			if not movimiento in ["w","a","s","d"]: movimiento = movimiento_anterior
			nueva_posicion_cabeza = obtener_posicion_cabeza(movimiento, posicion_serpiente)
			if partida_perdida(posicion_serpiente, movimiento, nueva_posicion_cabeza): 
				print("¡Perdiste!")
				break 
			realizar_movimiento(nueva_posicion_cabeza, tablero, posicion_serpiente, posicion_fruta)	
			if posicion_fruta == posicion_serpiente[0]: #si comió la fruta
				if partida_ganada(posicion_serpiente): 
					clear_terminal()
					imprimir_tablero(estructura_tablero, tablero)
					print("¡Has ganado el juego! Felicitaciones")
					break
				posicion_fruta = colocar_fruta(tablero, posicion_serpiente)
			movimiento_anterior = movimiento			
		seguir_jugando = "s" == input('Ingresá "s" para seguir jugando, o cualquier cosa para salir: ')
		
def crear_tablero(estructura_tablero, tablero, posicion_serpiente):
	"""Crea el tablero del juego. Se llama únicamente al principio de cada partida. 
	También coloca a la serpiente por primera vez en el mismo."""	
	for i in range(FILAS_TABLERO):
		estructura_tablero.append([])		
		tablero.append([])

		for j in range(COLUMNAS_TABLERO):
			if j == COLUMNAS_TABLERO-1: tablero[i].append(" "); continue
			if i == FILAS_TABLERO-1: estructura_tablero[i].append(" "); tablero[i].append(" "); continue
			estructura_tablero[i].append(".")
			tablero[i].append(" ")
	tablero[posicion_serpiente[0][0]][posicion_serpiente[0][1]] = "#" 
		
def imprimir_tablero(estructura_tablero, tablero):
	"""Imprime el tablero del juego."""
	for i in range(FILAS_TABLERO):	
		for j in range(COLUMNAS_TABLERO):	
			print(tablero[i][j], end="")
			if j == COLUMNAS_TABLERO-1: continue
			print(estructura_tablero[i][j], end="")
		print()

def colocar_fruta(tablero, posicion_serpiente):
	"""Coloca una nueva fruta en el mapa y devuelve su posición en el tablero. Si la posicion nueva de la fruta cae sobre 
	la serpiente, se anula y calcula nuevamente una posicion hasta que no caiga sobre la serpiente.""" 
	color_rojo = '\033[91m'
	color_normal = '\033[0m'
	while True:	
		posicion_fruta = [randint(0, FILAS_TABLERO-1), randint(0, COLUMNAS_TABLERO-1)]
		if not posicion_fruta in posicion_serpiente: break
	tablero[posicion_fruta[0]][posicion_fruta[1]] = color_rojo + "*" + color_normal
	return posicion_fruta

def obtener_posicion_cabeza(movimiento, posicion_serpiente):
	"""Devuelve la nueva (futura) posicion de la cabeza de la serpiente, pero no realiza ningún movimiento."""
	if movimiento == "w":
		cambiar_fila = -1
		cambiar_columna = 0
	elif movimiento == "s":
		cambiar_fila = 1
		cambiar_columna = 0
	elif movimiento == "a":
		cambiar_fila = 0
		cambiar_columna = -1
	elif movimiento == "d":
		cambiar_fila = 0
		cambiar_columna = 1
	return [posicion_serpiente[0][0] + cambiar_fila, posicion_serpiente[0][1] + cambiar_columna]

def realizar_movimiento(nueva_posicion_cabeza, tablero, posicion_serpiente, posicion_fruta):
	"""Funcion engargada del algoritmo de movimiento de la serpiente."""
	color_verde = '\033[92m'
	color_normal = '\033[0m'
	posicion_serpiente.insert(0, nueva_posicion_cabeza)
	remover_cola_vieja(tablero, posicion_serpiente, posicion_fruta)	
	#colocamos la serpiente en el tablero. Cada "parte" refiere a una partecita de la serpiente
	for parte in posicion_serpiente: 
		tablero[parte[0]][parte[1]] = color_verde + "#" + color_normal	

def remover_cola_vieja(tablero, posicion_serpiente, posicion_fruta):
	"""Remueve la última partecita de la serpiente, si es que NO comió fruta. 
	Si comió, no lo hace, haciendo que la serpiente crezca."""
	if not posicion_fruta == posicion_serpiente[0]:
		parte_a_remover = posicion_serpiente.pop(-1) 
		tablero[parte_a_remover[0]][parte_a_remover[1]] = " "

def partida_perdida(posicion_serpiente, movimiento, nueva_posicion_cabeza):
	"""Devuelve True si la serpiente choca con los bordes del mapa o si se come a si misma, es decir, 
	devuelve True si perdio el jugador."""
	en_primera_fila = posicion_serpiente[0] in [[0,i] for i in range(COLUMNAS_TABLERO)]
	en_ultima_fila = posicion_serpiente[0] in [[FILAS_TABLERO-1,i] for i in range(FILAS_TABLERO)]
	en_primera_columna = posicion_serpiente[0] in [[i,0] for i in range(FILAS_TABLERO)]
	en_ultima_columna = posicion_serpiente[0] in [[i,COLUMNAS_TABLERO-1] for i in range(FILAS_TABLERO)]
	
	return any((en_primera_fila and movimiento == "w", en_ultima_fila and movimiento == "s", 
	en_primera_columna and movimiento == "a", en_ultima_columna and movimiento == "d",
	nueva_posicion_cabeza in posicion_serpiente[:-1] and len(posicion_serpiente) > 2,
	nueva_posicion_cabeza in posicion_serpiente and len(posicion_serpiente) == 2))

def partida_ganada(posicion_serpiente):
	"""Devuelve True si el jugador ganó, es decir, si el largo de la serpiente alcanzó el largo preestablecido."""
	return LARGO_MAX_SERPIENTE == len(posicion_serpiente)

main()
