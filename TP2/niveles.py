#encargado de leer archivos txt y mandarle informacion de los niveles al main
def obtener_niveles_juego(NIVEL_INICIAL, NIVEL_FINAL):
	"""Devuelve un diccionario cuyas claves son los numeros de los niveles que se juegan, y cuyos 
	valores son el path relativo a dicho nivel. Importante: los archivos de texto de los niveles deben
	estar dentro de la carpeta Niveles, y deben nombrarse nivel_k.txt si k es el nivel."""
	niveles_juego = {}
	for i in range(NIVEL_INICIAL, NIVEL_FINAL+1):
		niveles_juego[i] = f"Niveles/nivel_{i}.txt"
	return niveles_juego

def levantar_datos_nivel(nivel_actual):
	"""Devuelve un diccionario cuyas claves son el nombre del dato del nivel, y sus valores son los datos
	correspondientes a dicho tipo de dato."""
	datos_nivel = {}
	with open (nivel_actual, 'r') as archivo:
		datos_nivel["largo_serpiente"] = int(archivo.readline().rstrip("\n"))
		datos_nivel["tiempo_reaccion"] = float(archivo.readline().rstrip("\n"))
		dimension = archivo.readline().rstrip("\n").split("x")
		datos_nivel["filas"] = int(dimension[0])
		datos_nivel["columnas"] = int(dimension[1])
		obstaculos = []
		for obs in archivo.readline().rstrip("\n").split(";"):
			obstaculos.append([int(obs.split(",")[0]), int(obs.split(",")[1])])
		datos_nivel["obstaculos"] = obstaculos
		datos_nivel["especiales"] = archivo.readline().rstrip("\n").split(",")
	return datos_nivel