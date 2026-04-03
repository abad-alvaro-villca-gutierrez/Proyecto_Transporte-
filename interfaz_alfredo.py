import tkinter as tk
from tkinter import messagebox, ttk
# Importamos las funciones que ya creamos en tu otro archivo
import database 

def registrar_item():
    nombre = entry_nombre.get().strip()
    posicion = entry_posicion.get().strip()
    valor = entry_valor.get().strip()

    if not nombre or not posicion or not valor:
        messagebox.showwarning("Atención", "Todos los campos son obligatorios")
        return

    try:
        # Convertimos a entero para asegurar compatibilidad con la BD
        pos_int = int(posicion)
        val_int = int(valor)

        # 1. VALIDACIÓN: Usamos la función de database.py
        if database.existe_item(nombre, pos_int):
            messagebox.showerror("Error", f"El ítem o la posición ya existen.")
        else:
            # 2. REGISTRO: Llamamos a la función de database.py
            exito = database.guardar_item(pos_int, nombre, val_int)
            
            if exito:
                messagebox.showinfo("Éxito", "Registro completado correctamente.")
                # Limpiar campos
                entry_nombre.delete(0, tk.END)
                entry_posicion.delete(0, tk.END)
                entry_valor.delete(0, tk.END)
                actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo guardar en la base de datos.")

    except ValueError:
        messagebox.showerror("Error de datos", "Posición y Valor deben ser números enteros.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

def actualizar_tabla():
    # Limpiar tabla actual
    for i in tree.get_children():
        tree.delete(i)
    
    # Obtener datos usando database.py
    items = database.traer_items()
    
    for item in items:
        # item[0]=posicion, item[1]=nombre, item[2]=valor
        tree.insert("", tk.END, values=(item[1], item[0], item[2]))

# --- CONFIGURACIÓN DE LA VENTANA ---
root = tk.Tk()
root.title("Registro de Transporte - Comparativa")
root.geometry("450x550")

# Encabezado
tk.Label(root, text="REGISTRO DE ITEMS", font=("Arial", 14, "bold")).pack(pady=15)

# Contenedor del Formulario
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nombre Ítem:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nombre = tk.Entry(frame, width=25)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Orden (Posición):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_posicion = tk.Entry(frame, width=25)
entry_posicion.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Valor (Relativo):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_valor = tk.Entry(frame, width=25)
entry_valor.grid(row=2, column=1, padx=5, pady=5)

# Botón Registrar
btn_reg = tk.Button(root, text="REGISTRAR", command=registrar_item, 
                   bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=20)
btn_reg.pack(pady=20)

# Estilo de la Tabla
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

# Tabla de Resultados
tree = ttk.Treeview(root, columns=("Nombre", "Posición", "Valor"), show="headings", height=10)
tree.heading("Nombre", text="Ítem")
tree.heading("Posición", text="Orden")
tree.heading("Valor", text="Valor")

# Ajuste de columnas
tree.column("Nombre", width=150)
tree.column("Posición", width=80, anchor="center")
tree.column("Valor", width=80, anchor="center")

tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Cargar datos iniciales
actualizar_tabla()

root.mainloop()