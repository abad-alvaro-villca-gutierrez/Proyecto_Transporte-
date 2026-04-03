import tkinter as tk
from tkinter import ttk, messagebox
from database import guardar_item, traer_items, borrar_item, existe_item

# CONFIGURACION DE LA VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("Transporte")
ventana.geometry("500x480")

# TITULO
tk.Label(ventana, text="TRANSPORTE", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(ventana, text="comodidad", font=("Arial", 9, "italic"), fg="gray").pack()

# CAMPOS DE ENTRADA
tk.Label(ventana, text="N° Comodidad:").pack()
campo_comodidad = tk.Entry(ventana, width=30)
campo_comodidad.pack()

tk.Label(ventana, text="Nombre:").pack()
campo_nombre = tk.Entry(ventana, width=30)
campo_nombre.pack()

tk.Label(ventana, text="Valor:").pack()
campo_valor = tk.Entry(ventana, width=30)
campo_valor.pack()

# LABEL DE ESTADO DEL REGISTRO
mensaje = tk.Label(ventana, text="", fg="green")
mensaje.pack(pady=5)

# TABLA
columnas = ("comodidad", "nombre", "valor")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
tabla.heading("comodidad", text="Comodidad")
tabla.heading("nombre", text="Nombre")
tabla.heading("valor", text="Valor")
tabla.column("comodidad", width=100, anchor="center")
tabla.column("nombre", width=220, anchor="w")
tabla.column("valor", width=100, anchor="center")
tabla.pack(padx=20, pady=5)

# CARGAR DATOS EN LA TABLA
def mostrar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for item in traer_items():
        tabla.insert("", "end", values=item)

# ACCION REGISTRAR
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
        messagebox.showerror("Error", "La comodidad debe ser un numero entero.")
        return

    try:
        valor = float(valor_txt)
    except ValueError:
        messagebox.showerror("Error", "El valor debe ser un numero.")
        return

    if existe_item(nombre, comodidad):
        messagebox.showerror("Error", "Ya existe ese item.")
        return

    ok = guardar_item(comodidad, nombre, valor)
    if ok:
        mensaje.config(text="Item registrado correctamente.", fg="green")
        campo_comodidad.delete(0, tk.END)
        campo_nombre.delete(0, tk.END)
        campo_valor.delete(0, tk.END)
        mostrar_tabla()
    else:
        messagebox.showerror("Error", "No se pudo guardar.")

# ACCION ELIMINAR
def eliminar():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Aviso", "Selecciona un item para eliminar.")
        return

    fila = tabla.item(seleccion[0])["values"]
    comodidad = int(fila[0])
    nombre = str(fila[1])

    confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}'?")
    if confirmar:
        borrar_item(comodidad)
        mensaje.config(text=f"'{nombre}' eliminado.", fg="red")
        mostrar_tabla()

# BOTONES
tk.Button(ventana, text="Registrar", width=15, command=registrar).pack(pady=2)
tk.Button(ventana, text="Eliminar", width=15, command=eliminar).pack(pady=2)

# CARGAR DATOS AL INICIAR
mostrar_tabla()