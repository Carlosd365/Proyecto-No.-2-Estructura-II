from typing import List, Optional
from datos.articulo import Articulo
from datos.tabla_hash import TablaHash

class TablaArticulos:
    def __init__(self) -> None:
        # capacidades "cómodas" para dispersión
        self.principal: TablaHash[str, Articulo] = TablaHash(capacidad=257)
        self.por_autor: TablaHash[str, List[str]] = TablaHash(capacidad=257)
        self.por_anio: TablaHash[int, List[str]] = TablaHash(capacidad=257)

    # Utilidades internas para listas de ids (evitar duplicado, quitar si existe)
    def _append_unique(self, lst: List[str], ident: str) -> None:
        if ident not in lst:
            lst.append(ident)

    def _remove_if_present(self, lst: List[str], ident: str) -> None:
        try:
            lst.remove(ident)
        except ValueError:
            pass

    # --------------- CRUD en memoria ---------------
    def agregar(self, art: Articulo) -> None:
        ident = art.identificador
        # principal
        self.principal.insertar(ident, art)
        # índice autor
        a = art.autor.strip()
        lst_aut = self.por_autor.obtener(a) or []
        self._append_unique(lst_aut, ident)
        self.por_autor.insertar(a, lst_aut)
        # índice año
        y = int(art.anio)
        lst_y = self.por_anio.obtener(y) or []
        self._append_unique(lst_y, ident)
        self.por_anio.insertar(y, lst_y)

    def eliminar(self, ident: str) -> None:
        art = self.principal.obtener(ident)
        if not art:
            return
        # quitar de principal
        self.principal.eliminar(ident)
        # quitar de autor
        a = art.autor.strip()
        lst_aut = self.por_autor.obtener(a) or []
        self._remove_if_present(lst_aut, ident)
        if lst_aut:
            self.por_autor.insertar(a, lst_aut)
        else:
            self.por_autor.eliminar(a)
        # quitar de año
        y = int(art.anio)
        lst_y = self.por_anio.obtener(y) or []
        self._remove_if_present(lst_y, ident)
        if lst_y:
            self.por_anio.insertar(y, lst_y)
        else:
            self.por_anio.eliminar(y)

    def actualizar_metadatos(self, ident: str, nuevo_autor: Optional[str] = None, nuevo_anio: Optional[int] = None) -> bool:
        art = self.principal.obtener(ident)
        if not art:
            return False

        # autor
        if nuevo_autor is not None and nuevo_autor.strip() != art.autor.strip():
            old = art.autor.strip()
            lst_old = self.por_autor.obtener(old) or []
            self._remove_if_present(lst_old, ident)
            if lst_old:
                self.por_autor.insertar(old, lst_old)
            else:
                self.por_autor.eliminar(old)

            art.autor = nuevo_autor.strip()
            lst_new = self.por_autor.obtener(art.autor) or []
            self._append_unique(lst_new, ident)
            self.por_autor.insertar(art.autor, lst_new)

        # año
        if nuevo_anio is not None and int(nuevo_anio) != int(art.anio):
            oldy = int(art.anio)
            lst_oldy = self.por_anio.obtener(oldy) or []
            self._remove_if_present(lst_oldy, ident)
            if lst_oldy:
                self.por_anio.insertar(oldy, lst_oldy)
            else:
                self.por_anio.eliminar(oldy)

            art.anio = int(nuevo_anio)
            lst_newy = self.por_anio.obtener(art.anio) or []
            self._append_unique(lst_newy, ident)
            self.por_anio.insertar(art.anio, lst_newy)

        # actualizar registro en principal por si cambiaron campos
        self.principal.insertar(ident, art)
        return True

    # --------------- Consultas ---------------
    def obtener_todos(self) -> List[Articulo]:
        out: List[Articulo] = []
        for k in self.principal.claves():
            art = self.principal.obtener(k)
            if art is not None:
                out.append(art)
        return out

    def por_autor_listado(self, autor: str) -> List[Articulo]:
        ids = self.por_autor.obtener(autor.strip()) or []
        out: List[Articulo] = []
        for ident in ids:
            art = self.principal.obtener(ident)
            if art is not None:
                out.append(art)
        return out

    def por_anio_listado(self, anio: int) -> List[Articulo]:
        ids = self.por_anio.obtener(int(anio)) or []
        out: List[Articulo] = []
        for ident in ids:
            art = self.principal.obtener(ident)
            if art is not None:
                out.append(art)
        return out
