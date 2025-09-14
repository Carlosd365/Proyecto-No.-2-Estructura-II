import os
import shutil
from datos.articulo import Articulo
from datos.calculo_hash import calcular_hash_archivo
from datos.tabla_memoria import TablaArticulos
from datos.base_datos import asegurar_estructura, anexar_registro, reescribir_archivo, CARPETA_ARTICULOS

def agregar_articulo(tabla: TablaArticulos, titulo: str, autor: str, anio: int, ruta_txt: str) -> str:
    
    ident = calcular_hash_archivo(ruta_txt)  
    if tabla.principal.obtener(ident) is not None:
        raise ValueError("Artículo duplicado (mismo contenido)")

    asegurar_estructura()
    destino = os.path.join(CARPETA_ARTICULOS, f"{ident}.txt")
    shutil.copyfile(ruta_txt, destino)

    art = Articulo(
        identificador=ident,
        titulo=titulo.strip(),
        autor=autor.strip(),
        anio=int(anio),
        nombre_archivo=f"{ident}.txt",
    )
    tabla.agregar(art)
    anexar_registro(art)
    return ident

def eliminar_articulo(tabla: TablaArticulos, ident: str) -> None:
    art = tabla.principal.obtener(ident)
    if not art:
        raise ValueError("No existe ese identificador")

    tabla.eliminar(ident)
    try:
        os.remove(os.path.join(CARPETA_ARTICULOS, art.nombre_archivo))
    except FileNotFoundError:
        pass
    reescribir_archivo(tabla)

def modificar_articulo(tabla: TablaArticulos, ident: str, nuevo_autor: str | None = None, nuevo_anio: int | None = None) -> None:
    ok = tabla.actualizar_metadatos(ident, nuevo_autor, nuevo_anio)
    if not ok:
        raise ValueError("No existe ese identificador")
    reescribir_archivo(tabla)
