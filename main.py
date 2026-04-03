import tkinter as tk
# Importamos los módulos completos
import codigoAndreina
import codigoMarina
import codigoAbad
import interfaz_alfredo

def menu_principal():
    ventana = tk.Tk()
    ventana.title("Sistema de Transporte - Equipo")
    ventana.geometry("300x400")

    tk.Label(ventana, text="PANEL DE CONTROL", font=("Arial", 12, "bold")).pack(pady=20)

    # Botones para cada interfaz
    # Suponiendo que cada uno guardó su código en una función abrir()
    tk.Button(ventana, text="Interfaz Andreina", command=codigoAndreina.abrir, width=20).pack(pady=5)
    tk.Button(ventana, text="Interfaz Marina", command=codigoMarina.abrir, width=20).pack(pady=5)
    tk.Button(ventana, text="Interfaz Abad", command=codigoAbad.abrir, width=20).pack(pady=5)
    tk.Button(ventana, text="Interfaz Alfredo", command=interfaz_alfredo.abrir, width=20).pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    menu_principal()