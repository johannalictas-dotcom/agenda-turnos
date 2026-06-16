from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import date, timedelta
app = Flask(__name__)


# -----------------------------
# INICIO (LISTA + INSERTA TURNO)
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def inicio():

    # INSERTAR TURNO
    if request.method == "POST":

        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        conexion = sqlite3.connect("database.db")
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO turnos (nombre, telefono, fecha, hora)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, fecha, hora))

        conexion.commit()
        conexion.close()

        # redirige para evitar reenvío del formulario
        return redirect(url_for("inicio"))

    # -----------------------------
    # CONSULTAR TURNOS
    # -----------------------------
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, telefono, fecha, hora
        FROM turnos
        ORDER BY fecha, hora
    """)

    turnos = cursor.fetchall()
    conexion.close()

    # -----------------------------
    # FORMATEAR FECHAS
    # -----------------------------
    turnos_formateados = []

    for turno in turnos:
        fecha_bd = turno[3]
        año, mes, dia = fecha_bd.split("-")
        fecha_arg = f"{dia}/{mes}/{año}"

        turnos_formateados.append(
            (
                turno[0],
                turno[1],
                turno[2],
                fecha_arg,
                turno[4]
            )
        )

    # -----------------------------
    # TARJETAS (STATS BÁSICOS)
    # -----------------------------
    total_turnos = len(turnos_formateados)

    # turnos de hoy
    from datetime import date
    hoy = date.today().strftime("%d/%m/%Y")

    turnos_hoy = len([
        t for t in turnos_formateados if t[3] == hoy
    ])

    # -----------------------------
    # RENDER
    # -----------------------------
    return render_template(
        "index.html",
        turnos=turnos_formateados,
        total_turnos=total_turnos,
        turnos_hoy=turnos_hoy
    )
@app.route("/recordatorios")
def recordatorios():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, telefono, fecha, hora
        FROM turnos
    """)

    turnos = cursor.fetchall()
    conexion.close()

    return render_template("recordatorios.html", turnos=turnos)
# -----------------------------
# ELIMINAR TURNO
# -----------------------------
@app.route("/eliminar/<int:id_turno>")
def eliminar(id_turno):

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM turnos WHERE id = ?",
        (id_turno,)
    )

    conexion.commit()
    conexion.close()

    return redirect(url_for("inicio"))


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)