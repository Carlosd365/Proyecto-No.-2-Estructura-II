import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datos.base_datos import cargar_desde_archivo
from datos.operaciones import agregar_articulo, eliminar_articulo, modificar_articulo

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Artículos — Tablas Hash")
        self.geometry("900x520")

        # Carga de datos
        self.tabla = cargar_desde_archivo()

        # --- Formulario de alta ---
        marco = ttk.LabelFrame(self, text="Nuevo artículo")
        marco.pack(fill="x", padx=10, pady=10)

        self.var_titulo = tk.StringVar()
        self.var_autor = tk.StringVar()
        self.var_anio = tk.StringVar()
        self.var_ruta = tk.StringVar()

        fila = 0
        ttk.Label(marco, text="Título:").grid(row=fila, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(marco, textvariable=self.var_titulo, width=50).grid(row=fila, column=1, sticky="w", padx=5, pady=5)
        fila += 1

        ttk.Label(marco, text="Autor(es):").grid(row=fila, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(marco, textvariable=self.var_autor, width=50).grid(row=fila, column=1, sticky="w", padx=5, pady=5)
        fila += 1

        ttk.Label(marco, text="Año:").grid(row=fila, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(marco, textvariable=self.var_anio, width=20).grid(row=fila, column=1, sticky="w", padx=5, pady=5)
        fila += 1

        ttk.Label(marco, text="Archivo .txt:").grid(row=fila, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(marco, textvariable=self.var_ruta, width=50).grid(row=fila, column=1, sticky="w", padx=5, pady=5)
        ttk.Button(marco, text="Examinar...", command=self._elegir_archivo).grid(row=fila, column=2, padx=5)
        fila += 1

        ttk.Button(marco, text="Agregar", command=self._agregar).grid(row=fila, column=1, sticky="w", padx=5, pady=5)

        # --- Búsqueda/Listado ---
        bloque = ttk.LabelFrame(self, text="Buscar / Listar")
        bloque.pack(fill="both", expand=True, padx=10, pady=10)

        self.var_filtro_autor = tk.StringVar()
        self.var_filtro_anio = tk.StringVar()
        self.var_filtro_titulo = tk.StringVar()

        barra = ttk.Frame(bloque)
        barra.pack(fill="x", pady=5)

        ttk.Label(barra, text="Autor:").pack(side="left", padx=5)
        ttk.Entry(barra, textvariable=self.var_filtro_autor, width=25).pack(side="left")
        ttk.Button(barra, text="Filtrar por autor", command=self._filtrar_autor).pack(side="left", padx=5)

        ttk.Label(barra, text="Año:").pack(side="left", padx=10)
        ttk.Entry(barra, textvariable=self.var_filtro_anio, width=8).pack(side="left")
        ttk.Button(barra, text="Filtrar por año", command=self._filtrar_anio).pack(side="left", padx=5)

        ttk.Label(barra, text="Título contiene:").pack(side="left", padx=10)
        ttk.Entry(barra, textvariable=self.var_filtro_titulo, width=25).pack(side="left")
        ttk.Button(barra, text="Filtrar por título", command=self._filtrar_titulo).pack(side="left", padx=5)

        ttk.Button(barra, text="Listar todos (por título)", command=self._listar_todos).pack(side="right", padx=5)

        # Tabla de resultados
        self.tree = ttk.Treeview(bloque, columns=("id","titulo","autor","anio","archivo"), show="headings")
        for c, w in [("id",180), ("titulo",260), ("autor",180), ("anio",60), ("archivo",180)]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=5)

        # Acciones sobre selección
        acciones = ttk.Frame(bloque)
        acciones.pack(fill="x")
        ttk.Button(acciones, text="Modificar autor/año", command=self._modificar).pack(side="left", padx=5, pady=5)
        ttk.Button(acciones, text="Eliminar", command=self._eliminar).pack(side="left", padx=5, pady=5)

        self._listar_todos()

    # Helpers GUI
    def _elegir_archivo(self):
        ruta = filedialog.askopenfilename(title="Selecciona un .txt", filetypes=[("Text files","*.txt")])
        if ruta:
            self.var_ruta.set(ruta)

    def _refrescar(self, filas):
        self.tree.delete(*self.tree.get_children())
        for a in filas:
            self.tree.insert("", "end", values=(a.identificador, a.titulo, a.autor, a.anio, a.nombre_archivo))

    def _seleccion(self):
        sel = self.tree.selection()
        if not sel:
            return None
        vals = self.tree.item(sel[0], "values")
        return vals[0]  # identificador

    # Eventos
    def _agregar(self):
        t = self.var_titulo.get().strip()
        a = self.var_autor.get().strip()
        y = self.var_anio.get().strip()
        r = self.var_ruta.get().strip()
        if not (t and a and y and r):
            messagebox.showwarning("Campos", "Completa todos los campos.")
            return
        try:
            yint = int(y)
        except ValueError:
            messagebox.showwarning("Año", "El año debe ser numérico.")
            return
        try:
            ident = agregar_articulo(self.tabla, t, a, yint, r)
            messagebox.showinfo("OK", f"Artículo agregado con ID {ident}.")
            self._listar_todos()
        except ValueError as e:
            messagebox.showerror("Duplicado", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def _modificar(self):
        ident = self._seleccion()
        if not ident:
            messagebox.showwarning("Selección", "Selecciona un registro.")
            return
        win = tk.Toplevel(self)
        win.title(f"Modificar {ident}")
        ttk.Label(win, text="Nuevo autor (opcional):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        var_aut = tk.StringVar()
        ttk.Entry(win, textvariable=var_aut, width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(win, text="Nuevo año (opcional):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        var_yr = tk.StringVar()
        ttk.Entry(win, textvariable=var_yr, width=10).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        def guardar():
            new_aut = var_aut.get().strip() or None
            new_yr = var_yr.get().strip()
            if new_yr == "":
                new_yr_i = None
            else:
                try:
                    new_yr_i = int(new_yr)
                except ValueError:
                    messagebox.showwarning("Año", "Año inválido.")
                    return
            try:
                modificar_articulo(self.tabla, ident, new_aut, new_yr_i)
                messagebox.showinfo("OK", "Registro modificado.")
                self._listar_todos()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Guardar", command=guardar).grid(row=2, column=1, padx=5, pady=10, sticky="e")

    def _eliminar(self):
        ident = self._seleccion()
        if not ident:
            messagebox.showwarning("Selección", "Selecciona un registro.")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar artículo {ident}? También se borrará su archivo .txt."):
            try:
                eliminar_articulo(self.tabla, ident)
                messagebox.showinfo("OK", "Eliminado.")
                self._listar_todos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _filtrar_autor(self):
        a = self.var_filtro_autor.get().strip()
        if not a:
            messagebox.showwarning("Filtro", "Ingresa autor.")
            return
        filas = self.tabla.por_autor_listado(a)
        filas.sort(key=lambda r: (r.titulo.lower(), r.autor.lower()))
        self._refrescar(filas)

    def _filtrar_anio(self):
        an = self.var_filtro_anio.get().strip()
        try:
            an = int(an)
        except Exception:
            messagebox.showwarning("Filtro", "Año inválido.")
            return
        filas = self.tabla.por_anio_listado(an)
        filas.sort(key=lambda r: (r.titulo.lower(), r.autor.lower()))
        self._refrescar(filas)

    def _filtrar_titulo(self):
        sub = self.var_filtro_titulo.get().strip().lower()
        if not sub:
            messagebox.showwarning("Filtro", "Ingresa parte del título.")
            return
        filas = [r for r in self.tabla.obtener_todos() if sub in r.titulo.lower()]
        filas.sort(key=lambda r: (r.titulo.lower(), r.autor.lower()))
        self._refrescar(filas)

    def _listar_todos(self):
        filas = self.tabla.obtener_todos()
        filas.sort(key=lambda r: (r.titulo.lower(), r.autor.lower()))
        self._refrescar(filas)
