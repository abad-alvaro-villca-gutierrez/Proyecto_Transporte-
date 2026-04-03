import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import guardar_item, traer_items, borrar_item, existe_item

ventana = tk.Tk()
ventana.title("Sistema de Transporte")
ventana.geometry("500x580")

# TITULO
tk.Label(ventana, text="GESTIÓN TRANSPORTE", font=("Arial", 16, "bold")).pack(pady=10)

# CAMPOS DE ENTRADA
tk.Label(ventana, text="Número de Comodidad:").pack()
campo_comodidad = tk.Entry(ventana, width=35)
campo_comodidad.pack(pady=5)

tk.Label(ventana, text="Nombre del Transporte:").pack()
campo_nombre = tk.Entry(ventana, width=35)
campo_nombre.pack(pady=5)

# Label para mensajes de éxito o error
mensaje = tk.Label(ventana, text="", fg="green")
mensaje.pack(pady=5)

# TABLA
columnas = ("comodidad", "nombre", "valor")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
tabla.heading("comodidad", text="Comodidad")
tabla.heading("nombre", text="Nombre")
tabla.heading("valor", text="Valor / Tarifa")

tabla.column("comodidad", width=100, anchor="center")
tabla.column("nombre", width=200, anchor="w")
tabla.column("valor", width=100, anchor="center")
tabla.pack(padx=20, pady=10)

# FUNCIÓN PARA MOSTRAR LA TABLA
def mostrar_tabla():
    # Limpiar tabla
    for fila in tabla.get_children():
        tabla.delete(fila)
    # Cargar datos desde database.py
    datos = traer_items()
    for item in datos:
        tabla.insert("", "end", values=item)

# FUNCIÓN REGISTRAR (Adaptada a tu existe_item y guardar_item)
def registrar():
    com_txt = campo_comodidad.get().strip()
    nom = campo_nombre.get().strip().capitalize()

    if not com_txt or not nom:
        messagebox.showwarning("Aviso", "Completa Comodidad y Nombre.")
        return

    try:
        comodidad = int(com_txt)
    except ValueError:
        messagebox.showerror("Error", "La comodidad debe ser un número entero.")
        return

    # 1. Usamos tu existe_item(nombre, comodidad) - requiere 2 datos
    if existe_item(nom, comodidad):
        messagebox.showinfo("Coincidencia", f"Ya existe un registro con el nombre '{nom}' o comodidad {comodidad}.")
    else:
        # 2. Si no existe, preguntamos si desea registrar y pedimos el valor
        confirmar = messagebox.askyesno("Confirmar", f"No hay coincidencias.\n¿Desea registrar '{nom}'?")
        
        if confirmar:
            # Pedimos el valor que mencionaste
            valor = simpledialog.askfloat("Nuevo Valor", f"Ingrese la tarifa para {nom}:")
            
            if valor is not None:
                # 3. Llamamos a tu guardar_item(comodidad, nombre, valor)
                exito = guardar_item(comodidad, nom, valor)
                if exito:
                    mensaje.config(text=f"'{nom}' registrado con éxito", fg="green")
                    campo_comodidad.delete(0, tk.END)
                    campo_nombre.delete(0, tk.END)
                    mostrar_tabla()
                else:
                    messagebox.showerror("Error", "No se pudo guardar en la base de datos.")

# FUNCIÓN ELIMINAR
def eliminar():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Aviso", "Selecciona una fila para eliminar.")
        return
    
    # Obtenemos la comodidad de la fila seleccionada
    item_tabla = tabla.item(seleccion[0])["values"]
    comodidad_id = item_tabla[0]
    nombre_item = item_tabla[1]

    if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre_item}' (Comodidad {comodidad_id})?"):
        if borrar_item(comodidad_id):
            mensaje.config(text="Registro eliminado.", fg="red")
            mostrar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo eliminar.")

# BOTONES
tk.Button(ventana, text="Registrar / Verificar", width=25, bg="#4CAF50", fg="white", command=registrar).pack(pady=5)
tk.Button(ventana, text="Eliminar Seleccionado", width=25, bg="#F44336", fg="white", command=eliminar).pack(pady=5)

# Cargar tabla al iniciar
mostrar_tabla()