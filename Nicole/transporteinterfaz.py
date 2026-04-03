import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import math


CONFIG_BD = {
    "driver": "{SQL Server}", 
    "server": r"localhost\SQLEXPRESS",
    "database": "transporte_db"
}

# --- PALETA DE COLORES RETRO 90s ---
COLOR_FONDO_APP = "#B465D3"    
COLOR_BORDE = "#2B2D5C"       
COLOR_VENTANA = "#9CB9D7"     
COLOR_CABECERA_1 = "#96DDA6"   
COLOR_CABECERA_2 = "#1D2EAB"  

class InterfazRetro:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro OS - Transportes")
        self.root.geometry("750x600")
        self.root.configure(bg=COLOR_FONDO_APP)

        self.crear_interfaz()
        self.actualizar_tabla()

    def conectar_bd(self):
        return pyodbc.connect(
            f"DRIVER={CONFIG_BD['driver']};"
            f"SERVER={CONFIG_BD['server']};"
            f"DATABASE={CONFIG_BD['database']};"
            f"Trusted_Connection=yes;"
        )

    def crear_interfaz(self):
        
        marco_formulario = tk.Frame(self.root, bg=COLOR_VENTANA, highlightbackground=COLOR_BORDE, highlightthickness=3)
        marco_formulario.pack(padx=30, pady=20, fill="x")

     
        barra_titulo_1 = tk.Frame(marco_formulario, bg=COLOR_CABECERA_1, height=25, highlightbackground=COLOR_BORDE, highlightthickness=1)
        barra_titulo_1.pack(fill="x")
        tk.Label(barra_titulo_1, text=" Ingresar_Datos.exe", bg=COLOR_CABECERA_1, fg="white", font=("Courier", 10, "bold")).pack(side="left")
        tk.Label(barra_titulo_1, text="_ [] X ", bg=COLOR_CABECERA_1, fg="white", font=("Courier", 10, "bold")).pack(side="right")

        
        contenido_form = tk.Frame(marco_formulario, bg=COLOR_VENTANA)
        contenido_form.pack(pady=15, padx=10)

        tk.Label(contenido_form, text="Nombre:", bg=COLOR_VENTANA, font=("Arial", 10, "bold"), fg=COLOR_BORDE).grid(row=0, column=0, padx=10)
        self.entrada_nombre = tk.Entry(contenido_form, width=20, highlightbackground=COLOR_BORDE, highlightthickness=2, relief="flat")
        self.entrada_nombre.grid(row=0, column=1, padx=5)

        tk.Label(contenido_form, text="Comodidad (1-10):", bg=COLOR_VENTANA, font=("Arial", 10, "bold"), fg=COLOR_BORDE).grid(row=0, column=2, padx=10)
        self.entrada_comodidad = tk.Entry(contenido_form, width=10, highlightbackground=COLOR_BORDE, highlightthickness=2, relief="flat")
        self.entrada_comodidad.grid(row=0, column=3, padx=5)

        
        boton_registrar = tk.Button(contenido_form, text=" OK ", font=("Arial", 10, "bold"), bg=COLOR_VENTANA, fg=COLOR_BORDE, 
                                    relief="flat", highlightbackground=COLOR_BORDE, highlightthickness=2, 
                                    activebackground="#9A86DB", command=self.validar_y_guardar)
        boton_registrar.grid(row=0, column=4, padx=20)


        
        marco_tabla = tk.Frame(self.root, bg=COLOR_VENTANA, highlightbackground=COLOR_BORDE, highlightthickness=3)
        marco_tabla.pack(padx=30, pady=10, fill="both", expand=True)

      
        barra_titulo_2 = tk.Frame(marco_tabla, bg=COLOR_CABECERA_2, height=25, highlightbackground=COLOR_BORDE, highlightthickness=1)
        barra_titulo_2.pack(fill="x")
        tk.Label(barra_titulo_2, text=" Base_De_Datos_Transporte.sys", bg=COLOR_CABECERA_2, fg="white", font=("Courier", 10, "bold")).pack(side="left")
        tk.Label(barra_titulo_2, text="_ [] X ", bg=COLOR_CABECERA_2, fg="white", font=("Courier", 10, "bold")).pack(side="right")

       
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview.Heading", background=COLOR_VENTANA, foreground=COLOR_BORDE, font=("Arial", 10, "bold"), bordercolor=COLOR_BORDE)
        estilo.configure("Treeview", rowheight=25, bordercolor=COLOR_BORDE)

       
        self.tabla = ttk.Treeview(marco_tabla, columns=("id", "nombre", "posicion", "valor"), show='headings')
        self.tabla.heading("id", text="id")
        self.tabla.heading("nombre", text="nombre")
        self.tabla.heading("posicion", text="posicion")
        self.tabla.heading("valor", text="valor")
        
        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("nombre", width=250)
        self.tabla.column("posicion", width=80, anchor="center")
        self.tabla.column("valor", width=150, anchor="center")
        
        self.tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        try:
            conexion = self.conectar_bd()
            cursor = conexion.cursor()
        
            cursor.execute("SELECT id, nombre, posicion, valor FROM transportes ORDER BY valor ASC")
            for fila in cursor.fetchall():
                self.tabla.insert("", tk.END, values=(fila[0], fila[1], fila[2], fila[3]))
            conexion.close()
        except Exception as e:
            print(f"Error: {e}")

    def validar_y_guardar(self):
        nombre = self.entrada_nombre.get()
        comodidad_str = self.entrada_comodidad.get()

        if nombre == "" or comodidad_str == "":
            messagebox.showwarning("Error", "Faltan datos.")
            return

        try:
            nivel = float(comodidad_str)
            if nivel < 1 or nivel > 10:
                messagebox.showwarning("Error", "Del 1 al 10 unicamente.")
                return

            # Calculo de caminatas (Equivalencia exponencial)
            valor_calculado = int(math.pow(nivel, 1.9))

            conexion = self.conectar_bd()
            cursor = conexion.cursor()
           
            cursor.execute("SELECT * FROM transportes WHERE nombre = ?", (nombre,))
            if cursor.fetchone():
                messagebox.showerror("FAIL", f"'{nombre}' ya existe.")
            else:
                
                cursor.execute("SELECT ISNULL(MAX(posicion), 0) + 1 FROM transportes")
                posicion_automatica = cursor.fetchone()[0]

                # Insertar
                cursor.execute("INSERT INTO transportes (nombre, posicion, valor) VALUES (?, ?, ?)", 
                               (nombre, posicion_automatica, valor_calculado))
                conexion.commit()
                
                messagebox.showinfo("OK", f"Registrado!\nPosicion asignada: {posicion_automatica}\nEquivale a: {valor_calculado} caminatas.")
                
                self.entrada_nombre.delete(0, tk.END)
                self.entrada_comodidad.delete(0, tk.END)
                self.actualizar_tabla()
            
            conexion.close()
        except ValueError:
            messagebox.showerror("Error", "Ingrese numeros validos en comodidad.")
        except Exception as e:
            messagebox.showerror("Error BD", f"Problema: {e}")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazRetro(ventana)
    ventana.mainloop()