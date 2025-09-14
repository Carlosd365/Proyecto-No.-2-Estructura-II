
from dataclasses import dataclass

@dataclass
class Articulo:
    identificador: str   
    titulo: str
    autor: str
    anio: int
    nombre_archivo: str 
