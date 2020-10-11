import csv
from random import randint, choice
CANTIDAD_ESPECIALES = 4

def obtener_datos_de_especiales():
    """Devuelve un diccionario cuyas claves son los símbolos de los especiales, y cuyos valores son listas con el respectivo
    aspecto, alteración, tecla y descripción del especial."""
    especiales_juego = {}
    with open("especiales.csv") as archivo:
        archivo.readline()
        archivo_csv = csv.reader(archivo)
        for linea in archivo_csv:
            especiales_juego[linea[0]] = linea[1:]
    return especiales_juego

def esta_contenido_o_igual(lista1, lista2):
	"""Devuelve True si lista1 está contenidaen la lista2 que contiene 1 o más listas, o si lista1 es igual la lista
	que contiene lista2."""
	if len(lista2) == 1: return [lista1] == lista2
	return any(lista1 == sublista2 for sublista2 in lista2)

def colocar_especial(tablero_juego, filas, columnas, especiales_nivel, datos_de_especiales, obstaculos, posicion_fruta, posicion_serpiente):
    """Coloca un especial random (aunque permitido por el nivel) en el tablero y devuelve su posicion y simbolo."""
    color_normal = '\033[0m'
    color_azul = '\033[34m'
    especial_colocado = choice(especiales_nivel)
    especial = datos_de_especiales[especial_colocado]
    while True:
        posicion_especial = [randint(0, filas-1), randint(0, columnas-1)]
        if not any((esta_contenido_o_igual(posicion_especial, obstaculos), 
        esta_contenido_o_igual(posicion_especial, posicion_serpiente), 
        esta_contenido_o_igual(posicion_especial, posicion_fruta))): break
    tablero_juego[posicion_especial[0]][posicion_especial[1]] = color_azul + especial_colocado + color_normal
    return posicion_especial, especial_colocado

def mochila(datos_de_especiales):
    """Devuelve una mochila (diccionario) cuyas claves son los símbolos de los especiales, y cuyos valores son 0, pues
    se inicializa vacía."""
    mochila = {}
    for esp in datos_de_especiales.keys():
        mochila[esp] = 0
    return mochila

def imprimir_mochila(especiales_nivel, especiales_en_mochila, datos_de_especiales):
    """Imprime en consola los especiales almacenados en la mochila."""
    print("""                MOCHILA
| SIMBOLO | TECLA | CANTIDAD | DESCRIPCIÓN |""")
    for simbolo, info in datos_de_especiales.items():
        if simbolo not in especiales_nivel: continue
        print(f"""
     {simbolo}        {info[2]}        {especiales_en_mochila[simbolo]}      {info[3]}""")

def especial_correspondiente(letra_del_especial_usado, datos_de_especiales):
    """Devuelve el símbolo correspondiente al especial cuya letra que fue pulsada por el usuario."""
    resultado = {}
    for simbolo,info in datos_de_especiales.items():
        if info[2] == letra_del_especial_usado:
            return simbolo
    
def usar_especiales(especial_usado, segundos_por_movimiento, datos_de_especiales):
    """Devuelve dos valores modificados por los especiales usados: segundos_por_movimiento y cambio_de_largo."""
    lista_info = datos_de_especiales.get(especial_usado, None)
    if not lista_info:
        return segundos_por_movimiento, 0
    if lista_info[0] == "velocidad":
        return segundos_por_movimiento + float(lista_info[1]), 0
    elif lista_info[0] == "largo":
        return segundos_por_movimiento, int(lista_info[1])

def puede_usarse(especial_usado, segundos_por_movimiento, posicion_serpiente, especiales_en_mochila, datos_de_especiales):
    """Devuelve True si se puede usar el especial en el momento. Devuelve False si no se tiene el especial en la 
    mochila, si se usa el especial para disminuir el largo matando a la snake, o si la velocidad es muy alta."""
    lista_info = datos_de_especiales.get(especial_usado, None)
    if any((especiales_en_mochila[especial_usado] == 0, especial_usado == "!" and segundos_por_movimiento < 0.05, 
    especial_usado == "%" and len(posicion_serpiente) < 3)): 
        return False
    return True