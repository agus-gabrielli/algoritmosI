def obtener_inputs_validos(especiales_juego, especiales_nivel):
	"""Devuelve un conjunto con los posibles inputs validos que el usuario pueda ingresar para que realice alguna acción
	en el juego. Se debe tener en cuenta que sólo se puede usar un especial en cada período de movimiento.""" 
	teclas_de_especiales = ""
	for simbolo,info in especiales_juego.items():
		if simbolo not in especiales_nivel: continue
		teclas_de_especiales += info[2]
	posibles_valores = set() #conjunto
	for m in "wasd":
		posibles_valores.add(m)
		for t in teclas_de_especiales:
			posibles_valores.add(t)
			posibles_valores.add(m+t)
			posibles_valores.add((m+t)[::-1])
	return posibles_valores

def desempaquetar_input(input_usuario, movimiento_anterior):
	"""Devuelve la letra del movimiento (que pueden ser wasd o None, si es que no se ingresó ninguna) y 
	la letra del especial utilizado, o None si es que no ha usado ninguno."""
	if len(input_usuario) == 1 and input_usuario in "wasd": return input_usuario, None
	elif len(input_usuario) == 1: return movimiento_anterior, input_usuario
	elif len(input_usuario) == 2: 
		if input_usuario[0] in "wasd": return input_usuario[0], input_usuario[1]
		else: return input_usuario[1], input_usuario[0]
	else: raise Exception("Se ha ingresado algo mal!")

def es_movimiento_valido(input_usuario, posibles_valores):
	""" """
	return input_usuario in posibles_valores
	
def obtener_posicion_cabeza(movimiento, posicion_serpiente):
	"""Devuelve la nueva (futura) posicion de la cabeza de la serpiente, pero no realiza ningún movimiento.""" 
	if "w" in movimiento:
		cambiar_fila = -1
		cambiar_columna = 0
	elif "s" in movimiento:
		cambiar_fila = 1
		cambiar_columna = 0
	elif "a" in movimiento:
		cambiar_fila = 0
		cambiar_columna = -1
	elif "d" in movimiento:
		cambiar_fila = 0
		cambiar_columna = 1
	return [posicion_serpiente[0][0] + cambiar_fila, posicion_serpiente[0][1] + cambiar_columna]

def realizar_movimiento(nueva_posicion_cabeza, tablero, posicion_serpiente, posicion_fruta, especial_largo):
	"""Funcion engargada del algoritmo de movimiento de la serpiente."""
	color_verde = '\033[92m'
	color_normal = '\033[0m'
	posicion_serpiente.insert(0, nueva_posicion_cabeza)
	if posicion_fruta != posicion_serpiente[0] and especial_largo != 1: #no llamo al metodo remover cola si se uso el especial de crecer y no si comio fruta
		remover_cola_vieja(tablero, posicion_serpiente)	
	if especial_largo == -2: #removemos dos veces la cola si se uso el especial de decrecer 2
		for i in range(2): remover_cola_vieja(tablero, posicion_serpiente)	
	for parte in posicion_serpiente:
		if parte is posicion_serpiente[0]: tablero[parte[0]][parte[1]] = color_verde + "o" + color_normal; continue
		tablero[parte[0]][parte[1]] = color_verde + "#" + color_normal	

def remover_cola_vieja(tablero, posicion_serpiente):
	"""Remueve la última partecita de la serpiente."""
	parte_a_remover = posicion_serpiente.pop(-1) 
	tablero[parte_a_remover[0]][parte_a_remover[1]] = " "