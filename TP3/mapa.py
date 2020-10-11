class Coord:
    """Representa las coordenadas de una celda en una grilla 2D, representada
    como filas y columnas. Las coordendas fila = 0, columna = 0 corresponden
    a la celda de arriba a la izquierda. Las instancias de Coord son inmutables."""

    def __init__(self, fila=0, columna=0):
        self.fila = fila
        self.columna = columna

    def trasladar(self, df, dc):
        """Devuelve una nueva coordanada a df filas y dc columnas de la que se pase como argumento."""
        return Coord(self.fila + df, self.columna + dc)

    def distancia(self, otra):
        """Devuelve la distancia entre dos celdas."""
        return ((self.fila - otra.fila)**2 + (self.columna - otra.columna)**2)**0.5

    def __eq__(self, otra):
        """Determina si dos coordenadas son iguales"""
        return self.fila == otra.fila and self.columna == otra.columna

    def __iter__(self):
        """Permite iterar las componentes de la coordenada.
        Devuelve un iterador que luego es usado con __next__() para poder iterar por una coordenada."""
        self.contador = 0
        return self

    def __next__(self):
        #self.contador --> 0 corresponde a fila, 1 a columna, 2 a nada
        if self.contador == 0: self.contador += 1; return self.fila
        elif self.contador == 1: self.contador += 1; return self.columna
        else: raise StopIteration

    def __hash__(self):
        """Código "hash" de la instancia inmutable."""
        # Este método es llamado por la función de Python hash(objeto), y debe devolver
        # un número entero.
        # Más información (y un ejemplo de cómo implementar la funcion) en:
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        return hash((self.fila, self.columna))

    def __repr__(self):
        """Representación de la coordenada como cadena de texto"""
        return f"({self.fila},{self.columna})"

class Mapa:
    """Representa el mapa de un laberinto en una grilla 2D con:
    * un tamaño determinado (filas y columnas)
    * una celda origen
    * una celda destino
    * 0 o más celdas "bloqueadas", que representan las paredes del laberinto
    Las instancias de Mapa son mutables."""

    def __init__(self, filas, columnas):
        """El mapa creado tiene todas las celdas desbloqueadas, el origen en la celda
        de arriba a la izquierda y el destino en el extremo opuesto. Argumentos:
        filas, columnas (int)."""
        self.filas = filas
        self.columnas = columnas
        self.celda_origen = Coord(1,1)
        self.celda_destino = Coord(self.filas-2, self.columnas-2)
        #creamos diccionario cuyas claves son las celdas, los valores son True or false si estan bloqueadas
        bloqueadas = {}
        for i in range(filas):
            for j in range(columnas):
                bloqueadas[Coord(i,j)] = False 
        self.bloqueadas = bloqueadas

    def dimension(self):
        """Dimensiones del mapa (filas y columnas). Devuelve: (int, int): Cantidad de filas y columnas"""
        return (self.filas, self.columnas)

    def origen(self):
        """Devuelve las coordenadas de la celda origen"""
        return self.celda_origen

    def destino(self):
        """Devuelve las coordenadas de la celda destino"""
        return self.celda_destino

    def asignar_origen(self, coord):
        """Asignar la celda origen. Argumentos: coord (Coord): Coordenadas de la celda origen"""
        self.celda_origen = coord

    def asignar_destino(self, coord):
        """Asignar la celda destino. Argumentos: coord (Coord): Coordenadas de la celda destino"""
        self.celda_destino = coord

    def celda_bloqueada(self, coord):
        """Devuelve True si la celda está bloqueada"""
        return self.bloqueadas[coord]

    def bloquear(self, coord):
        """Bloquea una celda"""
        self.bloqueadas[coord] = True

    def desbloquear(self, coord):
        """Desbloquea una celda."""
        self.bloqueadas[coord] = False

    def alternar_bloque(self, coord):
        """Alternar entre celda bloqueada y desbloqueada. Si la celda estaba previamente desbloqueada, la bloquea, y viceversa."""
        self.bloqueadas[coord] = not self.bloqueadas[coord]

    def es_coord_valida(self, coord):
        """Devuelve True si las coordenadas corresponden a una celda dentro del mapa"""
        return coord in self.bloqueadas #bloqueadas tiene todas las celdas validas como valores

    def trasladar_coord(self, coord, df, dc):
        """Trasladar una coordenada, si es posible.
        Argumentos: 
            coord: la coordenada de una celda en el mapa
            df, dc: a traslación a realizar
        Devuelve una nueva Coord: la coordenada trasladada si queda dentro del mapa. En caso
        contrario, devuelve la coordenada recibida."""
        nueva_coord = coord.trasladar(df, dc)
        if self.es_coord_valida(nueva_coord): return nueva_coord
        return coord

    def __iter__(self):
        """Devuelve un iterador que permite iterar por las coordenadas de todas las celdas del mapa."""
        self.en_fila_columna = [0,0]
        return self

    def __next__(self): 
        """Define cómo se itera y devuelve la coordenada siguiente en la iteración. La forma de iterar es:
        iteramos primero de izquierda a derecha por cada fila, y luego bajamos a la sig fila."""
        if self.en_fila_columna[0] <= self.filas -1:#esto siempre se cumple
            if self.en_fila_columna[1] < self.columnas -1:
                coord = Coord(self.en_fila_columna[0],self.en_fila_columna[1])
                self.en_fila_columna[1] += 1
                return coord
            if self.en_fila_columna[1] == self.columnas -1:
                coord = Coord(self.en_fila_columna[0],self.en_fila_columna[1])
                self.en_fila_columna[0] += 1
                self.en_fila_columna[1] = 0
                return coord
        else: raise StopIteration