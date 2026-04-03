import pyodbc

# 1. CONFIGURACIÓN DE LA CONEXIÓN
def conectar():
    try:
        # Usamos localhost porque tu instancia es la principal (MSSQLSERVER)
        # Añadimos TrustServerCertificate y Encrypt para evitar bloqueos de SSL
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=TransporteDB;"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )
        return conn
    except Exception as e:
        print(f"Error crítico de conexión: {e}")
        return None

# 2. GUARDAR UN NUEVO ÍTEM
def guardar_item(posicion, nombre, valor):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        # Usamos 'posicion' según tu diagrama de BD
        cursor.execute(
            "INSERT INTO Transporte (posicion, nombre, valor) VALUES (?, ?, ?)",
            (posicion, nombre, valor)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

# 3. OBTENER TODOS LOS ÍTEMS (PARA LA TABLA)
def traer_items():
    try:
        conn = conectar()
        if conn is None: return []
        
        cursor = conn.cursor()
        # Seleccionamos las columnas reales de tu tabla
        cursor.execute("SELECT posicion, nombre, valor FROM Transporte ORDER BY posicion ASC")
        datos = cursor.fetchall()
        conn.close()
        
        # Convertimos los datos a una lista simple para la interfaz
        resultado = []
        for fila in datos:
            resultado.append([fila[0], fila[1], fila[2]])
        return resultado
    except Exception as e:
        print(f"Error al traer datos: {e}")
        return []

# 4. ELIMINAR UN ÍTEM
def borrar_item(posicion):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Transporte WHERE posicion = ?", (posicion,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al borrar: {e}")
        return False

# 5. VERIFICAR SI YA EXISTE (PARA EVITAR DUPLICADOS)
def existe_item(nombre, posicion):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Transporte WHERE nombre = ? OR posicion = ?",
            (nombre, posicion)
        )
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None
    except:
        return False