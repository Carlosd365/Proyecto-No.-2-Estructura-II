import os
from datos.articulo import Articulo
from datos.tabla_memoria import TablaArticulos

RUTA_DB = "articulos_db.txt"
CARPETA_ARTICULOS = "articulos"

def asegurar_estructura() -> None:
    os.makedirs(CARPETA_ARTICULOS, exist_ok=True)
    if not os.path.exists(RUTA_DB):
        with open(RUTA_DB, "w", encoding="utf-8"):
            pass

def cargar_desde_archivo() -> TablaArticulos:
    
    asegurar_estructura()
    tabla = TablaArticulos()
    with open(RUTA_DB, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split("|")
            if len(partes) != 5:
                continue
            ident, titulo, autor, anio, nombre_archivo = partes
            try:
                art = Articulo(
                    identificador=ident,
                    titulo=titulo,
                    autor=autor,
                    anio=int(anio),
                    nombre_archivo=nombre_archivo,
                )
                tabla.agregar(art)
            except Exception:
                continue
    return tabla

def reescribir_archivo(tabla: TablaArticulos) -> None:
    with open(RUTA_DB, "w", encoding="utf-8") as f:
        for art in tabla.obtener_todos():
            f.write(f"{art.identificador}|{art.titulo}|{art.autor}|{art.anio}|{art.nombre_archivo}\n")

def anexar_registro(art: Articulo) -> None:
    with open(RUTA_DB, "a", encoding="utf-8") as f:
        f.write(f"{art.identificador}|{art.titulo}|{art.autor}|{art.anio}|{art.nombre_archivo}\n")
