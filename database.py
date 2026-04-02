import pyodbc

# REALIZAMOS LA CONEXION CON SQL SERVER
def conectar():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=transporte_db;"
        "Trusted_Connection=yes;"
    )
    return conn

# GUARDAMOS EL VALOR DEL ITEM REGISTRADO
def guardar_item(comodidad, nombre, valor):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transporte (comodidad, nombre, valor) VALUES (?, ?, ?)",
            (comodidad, nombre, valor)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False

# TRAE TODOS LOS ITEMS
def traer_items():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT comodidad, nombre, valor FROM transporte ORDER BY comodidad ASC")
    datos = cursor.fetchall()
    conn.close()
    resultado = []
    for fila in datos:
        resultado.append([fila[0], fila[1], fila[2]])
    return resultado

# ELIMINAR ITEMS
def borrar_item(comodidad):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transporte WHERE comodidad = ?", (comodidad,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# VERIFICACION SI YA EXISTE EN LA LISTA EL ITEM REGISTRADO
def existe_item(nombre, comodidad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM transporte WHERE nombre = ? OR comodidad = ?",
        (nombre, comodidad)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
