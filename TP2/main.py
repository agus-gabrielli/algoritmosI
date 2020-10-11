from terminal import timed_input, clear_terminal
import tablero
import movimiento
import estado
import niveles
import especiales

NIVEL_INICIAL = 1
NIVEL_FINAL = 5

def main():
	"""Es la función principal, desde la cual se llaman a todas las funciones que permiten 
	el funcionamiento del juego."""
	niveles_juego = niveles.obtener_niveles_juego(NIVEL_INICIAL, NIVEL_FINAL)
	seguir_jugando = True
	print("¡Usá w a s d para moverte!"); timed_input(1.5)
	while(seguir_jugando):	
		for nivel_actual, ruta_nivel_actual in niveles_juego.items():
			datos_nivel = niveles.levantar_datos_nivel(ruta_nivel_actual)
			largo_max_serpiente = datos_nivel["largo_serpiente"]
			segundos_por_movimiento = datos_nivel["tiempo_reaccion"]
			filas = datos_nivel["filas"]
			columnas = datos_nivel["columnas"]
			obstaculos = datos_nivel["obstaculos"]
			especiales_nivel = datos_nivel["especiales"]
			posicion_serpiente = [[filas//2, columnas//2]]
			tablero_juego, estructura_tablero = tablero.crear_tablero(posicion_serpiente, obstaculos, filas, columnas)
			posicion_fruta = tablero.colocar_fruta(tablero_juego, posicion_serpiente, obstaculos, filas, columnas, [])
			datos_de_especiales = especiales.obtener_datos_de_especiales()
			posicion_especial, especial_colocado = especiales.colocar_especial(tablero_juego, filas, columnas, especiales_nivel, datos_de_especiales, obstaculos, posicion_fruta, posicion_serpiente)
			especiales_en_mochila = especiales.mochila(datos_de_especiales)
			inputs_validos = movimiento.obtener_inputs_validos(datos_de_especiales, especiales_nivel)
			letra_del_especial_usado = ""
			movimiento_actual = ""
			movimiento_anterior = "w" #primer movimiento por default 
			perdio, gano = False, False
			estado.presentar_nivel()

			while True:
				clear_terminal()
				print(f"Nivel {nivel_actual} | Faltan {largo_max_serpiente-len(posicion_serpiente)} pedacitos para completar el nivel")
				tablero.imprimir_tablero(estructura_tablero, tablero_juego, filas, columnas)
				especiales.imprimir_mochila(especiales_nivel, especiales_en_mochila, datos_de_especiales)
				input_usuario = timed_input(segundos_por_movimiento)
				if not movimiento.es_movimiento_valido(input_usuario, inputs_validos): movimiento_actual = movimiento_anterior
				else: movimiento_actual, letra_del_especial_usado = movimiento.desempaquetar_input(input_usuario, movimiento_anterior)
				cambio_de_largo = 0
				if letra_del_especial_usado: #si no es cadena vacía | si se usó un especial
					especial_usado = especiales.especial_correspondiente(letra_del_especial_usado, datos_de_especiales)
					if especiales.puede_usarse(especial_usado, segundos_por_movimiento, posicion_serpiente, especiales_en_mochila, datos_de_especiales):
						segundos_por_movimiento,cambio_de_largo = especiales.usar_especiales(especial_usado, segundos_por_movimiento, datos_de_especiales)
						especiales_en_mochila[especial_usado] -= 1
						letra_del_especial_usado = ""
				nueva_posicion_cabeza = movimiento.obtener_posicion_cabeza(movimiento_actual, posicion_serpiente)
				if estado.partida_perdida(posicion_serpiente, movimiento_actual, nueva_posicion_cabeza, obstaculos, filas, columnas): 
					print("¡Perdiste!")
					perdio = True
					break 
				movimiento.realizar_movimiento(nueva_posicion_cabeza, tablero_juego, posicion_serpiente, posicion_fruta, cambio_de_largo)
				if posicion_especial == posicion_serpiente[0]:#si comio especial
					especiales_en_mochila[especial_colocado] += 1
					posicion_especial, especial_colocado = especiales.colocar_especial(tablero_juego, filas, columnas, especiales_nivel, datos_de_especiales, obstaculos, posicion_fruta, posicion_serpiente)
				if estado.nivel_ganado(posicion_serpiente, largo_max_serpiente): #si gano
					clear_terminal()
					tablero.imprimir_tablero(estructura_tablero, tablero_juego, filas, columnas)
					if nivel_actual == NIVEL_FINAL:
						print("¡Has ganado el juego! Felicitaciones!")
						gano = True
					else: print("¡Has ganado el nivel! Felicitaciones!"); timed_input(2); break
				if posicion_fruta == posicion_serpiente[0]: #si comió la fruta
					posicion_fruta = tablero.colocar_fruta(tablero_juego, posicion_serpiente, obstaculos, filas, columnas, posicion_especial)
				movimiento_anterior = movimiento_actual
			if perdio or gano: break		
		seguir_jugando = "s" == input('Ingresá "s" para seguir jugando, o cualquier cosa para salir: ')

try:
	main()
except KeyboardInterrupt:
	print("...Has salido del juego...")
	exit()
except IOError or FileNotFoundError:
	print("""Ha ocurrido un error al abrir algún archivo correspondiente a los niveles o al del especial. 
Compruebe 1) que todos los .txt de los niveles estén dentro del directorio Niveles, y que este esté 
junto al main 2) Que el archivo especiales.csv esté en el mismo directorio que main.py 3) Que estés 
localizado dentro de la carpeta que contiene al juego, pues el programa utiliza paths relativos.""")
	exit()
except ModuleNotFoundError:
	print("Ha ocurrido un error. Compruebe que los módulos estén en el mismo directorio que contiene a main.py")
	exit()
except Exception as e:
	print(f"Ha ocurrido el siguiente error: {e}. El programa finalizará.")