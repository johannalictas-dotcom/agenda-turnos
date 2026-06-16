import sqlite3

conexion = sqlite3.connect("database.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS turnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL
)
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")