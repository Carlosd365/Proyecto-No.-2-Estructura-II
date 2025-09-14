from typing import List, Tuple, Optional, Callable, Iterable, TypeVar, Generic

Clave = TypeVar("Clave")
Valor = TypeVar("Valor")

class TablaHash(Generic[Clave, Valor]):
    """
    Implementación sencilla de tabla hash con encadenamiento (listas en cada bucket).
    - capacidad: número de buckets en la tabla.
    - cubetas: lista de listas de pares (clave, valor).
    - funcion_hash: función usada para calcular el hash de las claves.
    """

    def __init__(self, capacidad: int = 257, funcion_hash: Optional[Callable[[Clave], int]] = None) -> None:
        self.cantidad_cubetas = max(3, int(capacidad))
        self.cubetas: List[List[Tuple[Clave, Valor]]] = [[] for _ in range(self.cantidad_cubetas)]
        self.funcion_hash = funcion_hash or (lambda clave: hash(clave))

    def _indice(self, clave: Clave) -> int:
        """Calcula el índice de la cubeta usando la función de hash y el tamaño de la tabla."""
        return self.funcion_hash(clave) % self.cantidad_cubetas

    def insertar(self, clave: Clave, valor: Valor) -> None:
        """
        Inserta un nuevo par (clave, valor) en la tabla.
        Si la clave ya existe, se actualiza el valor.
        """
        cubeta = self.cubetas[self._indice(clave)]
        for i, (clave_existente, _) in enumerate(cubeta):
            if clave_existente == clave:
                cubeta[i] = (clave, valor)  # actualizar
                return
        cubeta.append((clave, valor))       # insertar (encadenado si hay colisión)

    def obtener(self, clave: Clave) -> Optional[Valor]:
        """
        Devuelve el valor asociado a una clave.
        Si la clave no existe, retorna None.
        """
        cubeta = self.cubetas[self._indice(clave)]
        for clave_existente, valor in cubeta:
            if clave_existente == clave:
                return valor
        return None

    def eliminar(self, clave: Clave) -> None:
        """
        Elimina un par (clave, valor) de la tabla.
        Si la clave no existe, no hace nada.
        """
        cubeta = self.cubetas[self._indice(clave)]
        for i, (clave_existente, _) in enumerate(cubeta):
            if clave_existente == clave:
                cubeta.pop(i)
                return

    def claves(self) -> Iterable[Clave]:
        """Devuelve todas las claves almacenadas en la tabla."""
        for cubeta in self.cubetas:
            for (clave, _) in cubeta:
                yield clave

    def valores(self) -> Iterable[Valor]:
        """Devuelve todos los valores almacenados en la tabla."""
        for cubeta in self.cubetas:
            for (_, valor) in cubeta:
                yield valor

    def pares(self) -> Iterable[Tuple[Clave, Valor]]:
        """Devuelve todos los pares (clave, valor) de la tabla."""
        for cubeta in self.cubetas:
            for par in cubeta:
                yield par
