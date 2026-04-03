import tkinter as tk
from tkinter import messagebox, END, LEFT, RIGHT, BOTH, X
import ttkbootstrap as tb
from database import guardar_item, traer_items, borrar_item, existe_item

# --- CONFIGURACIÓN DE LA VENTANA ---
ventana = tb.Window(themename="journal") 
ventana.title("Sistema de Gestión de Transporte")
ventana.geometry("1100x600")

font_banner = ("Segoe UI", 20, "bold")
font_titulo = ("Segoe UI", 13, "bold")

# --- BANNER SUPERIOR ---
banner = tb.Frame(ventana, bootstyle="primary", padding=20)
banner.pack(fill=X)
tb.Label(banner, text="Panel de Control de Transporte", font=font_banner, bootstyle="inverse-primary").pack(side=LEFT)

# --- CONTENEDOR PRINCIPAL (Paneles lado a lado) ---
contenedor = tb.Frame(ventana, padding=25)
contenedor.pack(fill=BOTH, expand=True)

panel_izq = tb.Frame(contenedor, padding=(0, 0, 20, 0))
panel_izq.pack(side=LEFT, fill=BOTH, expand=False)

panel_der = tb.Frame(contenedor, padding=(20, 0, 0, 0))
panel_der.pack(side=RIGHT, fill=BOTH, expand=True)

# --- PANEL IZQUIERDO: TABLA ---
tb.Label(panel_izq, text="Inventario de Medios", font=font_titulo, bootstyle="primary").pack(anchor="w", pady=(0, 10))

tabla = tb.Treeview(panel_izq, columns=("comodidad", "nombre", "valor"), show="headings", height=20, bootstyle="primary")
tabla.heading("comodidad", text="N° Comodidad")
tabla.heading("nombre", text="Nombre del Transporte")
tabla.heading("valor", text="Valor")
tabla.column("comodidad", width=120, anchor="center")
tabla.column("nombre", width=250, anchor="w")
tabla.column("valor", width=100, anchor="center")
tabla.pack(fill=BOTH, expand=True)

# --- PANEL DERECHO: FORMULARIO DE REGISTRO ---
tb.Label(panel_der, text="Registrar Nuevo Transporte", font=font_titulo, bootstyle="success").pack(anchor="w")
f_registro = tb.Frame(panel_der, padding=15)
f_registro.pack(fill=X, pady=(5, 20))

tb.Label(f_registro, text="N° Comodidad:").grid(row=0, column=0, padx=5, pady=10, sticky="w")
campo_comodidad = tb.Entry(f_registro, width=30)
campo_comodidad.grid(row=0, column=1, padx=5, pady=10)

tb.Label(f_registro, text="Nombre:").grid(row=1, column=0, padx=5, pady=10, sticky="w")
campo_nombre = tb.Entry(f_registro, width=30)
campo_nombre.grid(row=1, column=1, padx=5, pady=10)

tb.Label(f_registro, text="Valor:").grid(row=2, column=0, padx=5, pady=10, sticky="w")
campo_valor = tb.Entry(f_registro, width=30)
campo_valor.grid(row=2, column=1, padx=5, pady=10)

# --- FUNCIONES LÓGICAS ---
def mostrar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for item in traer_items():
        tabla.insert("", "end", values=item)

def registrar():
    comodidad_txt = campo_comodidad.get().strip()
    nombre = campo_nombre.get().strip().capitalize()
    valor_txt = campo_valor.get().strip()

    if not comodidad_txt or not nombre or not valor_txt:
        messagebox.showwarning("Aviso", "Debes llenar todos los campos.")
        return

    try:
        comodidad = int(comodidad_txt)
    except ValueError:
        messagebox.showerror("Error", "La comodidad debe ser un número entero.")
        return

    try:
        valor = float(valor_txt)
    except ValueError:
        messagebox.showerror("Error", "El valor debe ser un número.")
        return

    if existe_item(nombre, comodidad):
        messagebox.showerror("Error", "Ya existe ese ítem en la base de datos.")
        return

    ok = guardar_item(comodidad, nombre, valor)
    if ok:
        messagebox.showinfo("Éxito", "Ítem registrado correctamente.")
        campo_comodidad.delete(0, tk.END)
        campo_nombre.delete(0, tk.END)
        campo_valor.delete(0, tk.END)
        mostrar_tabla()
    else:
        messagebox.showerror("Error", "No se pudo guardar en la base de datos.")

def eliminar():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Aviso", "Selecciona un ítem de la tabla para eliminar.")
        return

    fila = tabla.item(seleccion[0])["values"]
    comodidad = int(fila[0])
    nombre = str(fila[1])

    confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}' permanentemente?")
    if confirmar:
        borrar_item(comodidad)
        messagebox.showinfo("Eliminado", f"'{nombre}' ha sido eliminado.")
        mostrar_tabla()

# --- BOTONES DE ACCIÓN ---
f_botones = tb.Frame(panel_der)
f_botones.pack(fill=X, pady=10)

tb.Button(f_botones, text="Registrar Ítem", bootstyle="success", width=20, command=registrar).pack(side=LEFT, padx=10)
tb.Button(f_botones, text="Eliminar Seleccionado", bootstyle="danger", width=20, command=eliminar).pack(side=LEFT, padx=10)

# Cargar los datos al iniciar la aplicación
mostrar_tabla()