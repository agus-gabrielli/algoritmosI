from random import choice
class IA:
    """Inteligencia artificial para resolver un laberinto.
    Se simula un jugador que comienza en la celda de origen, y mediante
    el método avanzar() el jugador hace un movimiento."""
    
    def __init__(self, mapa):
        """Constructor. Tendrá como atributos el laberinto (objeto de tipo Mapa) a resolver, la posicion 
        actual en el mismo, que comienza siendo el origen, el destino, y luego dos listas: camino_directo tendrá
        las celdas que conectan el origen con el destino, mientras que visitadas tendrá las celdas en las que 
        alguna vez estuvo el "jugador" que busca la salida."""
        self.laberinto = mapa
        self.posicion = mapa.origen()
        self.destino = mapa.destino()
        self.camino_directo = [self.posicion]
        self.visitadas = [self.posicion]

    def coord_jugador(self):
        """Devuelve las coordenadas de la celda en la que se encuentra el jugador."""
        return self.posicion

    def visitados(self):
        """Devuelve la lista de celdas visitadas al menos una vez por el jugador desde que
            comenzó la simulación."""
        return self.visitadas

    def camino(self):
        """Devuelve la lista de celdas que componen el camino desde el origen hasta la posición
            del jugador. Es un subconjunto de visitados()."""
        return self.camino_directo

    def obtener_vecinas_donde_ir(self):
        """Devuelve una lista que contiene las celdas vecinas de la posicion actual que cumplen
        estar desbloqueadas y no estar en visitadas()."""
        coord = self.posicion
        laberinto = self.laberinto
        posibles_vecinas = set()
        vecinas_donde_ir = []
        posibles_vecinas.add(laberinto.trasladar_coord(coord, 1, 0))  
        posibles_vecinas.add(laberinto.trasladar_coord(coord, -1, 0))  
        posibles_vecinas.add(laberinto.trasladar_coord(coord, 0, 1))  
        posibles_vecinas.add(laberinto.trasladar_coord(coord, 0, -1))  
        for v in posibles_vecinas: 
            if (v != coord) and (v not in self.visitadas) and (not laberinto.celda_bloqueada(v)): 
                vecinas_donde_ir.append(v)
        return vecinas_donde_ir

    def avanzar(self):
        """Avanza un paso en la simulación. Si el jugador no está en la celda destino, y hay algún movimiento
        posible hacia una celda no visitada, se efectúa ese movimiento."""
        if len(self.camino_directo) != 0: 
            celda_anterior = self.camino_directo[-1]
        if self.destino in self.camino_directo:
            return

        vecinas_donde_ir = self.obtener_vecinas_donde_ir()
        if len(vecinas_donde_ir) == 0: #está encerrado! Volver atrás
            self.camino_directo.pop(-1)
            self.posicion = celda_anterior
        else: 
            self.posicion = choice(vecinas_donde_ir)
            self.camino_directo.append(self.posicion)
            self.visitadas.append(self.posicion)