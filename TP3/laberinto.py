from mapa import Mapa
from mapa import Coord
from random import choice

def generar_laberinto(filas, columnas):
    """Genera un laberinto. Devuelve un mapa nuevo con celdas bloqueadas formando un laberinto aleatorio"""
    laberinto = Mapa(filas,columnas)
    bloquear_mapa(laberinto)
    origen = laberinto.origen()
    destino = laberinto.destino()
    if destino.fila % 2 != 1 and destino.columna % 2 != 1: raise Exception("Destino en celda par. Insertar número de filas y columnas impar!")

    camino = []
    celdas_prohibidas = []
    generar_camino_directo(origen, camino, celdas_prohibidas, laberinto)
    camino_completo = obtener_camino_completo(camino)
    desbloquear_celdas(camino_completo, laberinto)
    generar_ramas(camino, laberinto)

    return laberinto

def generar_camino_directo(celda, camino, celdas_prohibidas, laberinto):
    """Muta la lista camino, insertando en ella las celdas del camino aleatorio generado entre el origen y el destino.
    Es una función recursiva."""
    if len(camino) != 0: 
        celda_anterior = camino[-1]
    camino.append(celda)

    if laberinto.destino() in camino: #caso base
        return

    vecinas_donde_ir = obtener_vecinas_donde_ir(celda, camino, celdas_prohibidas, laberinto)
    if len(vecinas_donde_ir) == 0: #está encerrado! Volver atrás
        celdas_prohibidas.append(celda)
        camino.pop(-1)
        camino.pop(-1)
        vecinas_donde_ir.append(celda_anterior) 
    proxima_celda = choice(vecinas_donde_ir)
    generar_camino_directo(proxima_celda, camino, celdas_prohibidas, laberinto)

def generar_ramas(camino_principal, laberinto):
    """Función recursiva. A partir de un camino principal, crea ramas del mismo."""
    if len(camino_principal) == 1: #caso base
        return

    for celda in camino_principal:
        rama = []
        esta_encerrado = False
        while True:
            rama.append(celda)
            celda_nueva = celda
            #Ahora agarramos una celda vecina bloqueada. Si está encerrado, corta y pasa a otra celda del camino principal:
            while not laberinto.celda_bloqueada(celda_nueva): 
                celdas_vecinas = obtener_celdas_vecinas(celda, laberinto)
                if encerrado(celdas_vecinas, laberinto): 
                    esta_encerrado = True
                    break
                celda_nueva = choice(tuple(celdas_vecinas))
            if esta_encerrado: break
            laberinto.desbloquear(celda_nueva)
            desbloquear_celda_del_medio(celda, celda_nueva, laberinto)
            celda = celda_nueva
        generar_ramas(rama, laberinto) #genero ramitas dentro de las ramas grandes        
        
def encerrado(celdas_vecinas, laberinto):
    """Devuevle True si se encerró el creador del laberinto, es decir, si las celdas vecinas están todas desbloqueadas
    y no puede avanzar más prolongando esa rama."""
    return all([not laberinto.celda_bloqueada(c) for c in celdas_vecinas])        
      
def desbloquear_celda_del_medio(celda_actual, celda_siguiente, laberinto):
    """Dadas dos celdas a distancia 1, desbloquea la celda del medio."""
    promedio_fila = (celda_actual.fila + celda_siguiente.fila)//2
    promedio_columna = (celda_actual.columna + celda_siguiente.columna)//2
    celda_del_medio = Coord(promedio_fila, promedio_columna)
    laberinto.desbloquear(celda_del_medio)

def obtener_vecinas_donde_ir(celda, camino, celdas_prohibidas, laberinto):
    """Devuelve una lista con las celdas vecinas bloqueadas, es decir, las celdas a las cuales se podrá viajar para avanzar en la creación del laberinto."""
    vecinas_donde_ir = []
    vecinas = obtener_celdas_vecinas(celda, laberinto)
    for v in vecinas:
        if (v not in camino) and (v not in celdas_prohibidas): 
            vecinas_donde_ir.append(v)
    return vecinas_donde_ir

def obtener_celdas_vecinas(coord, laberinto):
    """Devuelve un set que contiene las celdas vecinas de la celda de coordenadas coord."""
    vecinas = set()
    posibles_vecinas = set()
    posibles_vecinas.add(laberinto.trasladar_coord(coord, 2, 0))  
    posibles_vecinas.add(laberinto.trasladar_coord(coord, -2, 0))  
    posibles_vecinas.add(laberinto.trasladar_coord(coord, 0, 2))  
    posibles_vecinas.add(laberinto.trasladar_coord(coord, 0, -2))  
    for v in posibles_vecinas: 
        if v != coord: vecinas.add(v) 
    return vecinas

def obtener_camino_completo(celdas_impares):
    """Devuevle un set con las celdas, tanto pares como impares, del camino aleatorio directo desde el origen al destino."""
    camino_total = set()
    camino_total.add(celdas_impares[0])
    for i,sig in enumerate(celdas_impares[1:]):
        act = celdas_impares[i] #el i empieza desde el 0
        promedio_fila = (act.fila + sig.fila)//2
        promedio_columna = (act.columna + sig.columna)//2
        celda_del_medio = Coord(promedio_fila, promedio_columna)
        camino_total.add(sig)
        camino_total.add(celda_del_medio)
    return camino_total

def desbloquear_celdas(camino, laberinto):
    """Muta el laberinto desbloqueando las celdas. Se le pasa un conjunto de celdas llamado camino."""
    for celda in camino:
        laberinto.desbloquear(celda)

def bloquear_mapa(mapa):
    """Bloquea todas las coordenadas de un mapa."""
    for coord in mapa:
        mapa.bloquear(coord)