
import os
import time
import psycopg2
import psycopg2.extras

from datetime import date
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "tareas_db")
DB_USER = os.environ.get("DB_USER", "tareas_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "tareas_pass")

# Estados permitidos para las tareas
ESTADOS_VALIDOS = {
    "pendiente",
    "en_progreso",
    "completada",
}

ESTADO_POR_DEFECTO = "pendiente"


def validar_fecha_limite(fecha):
    if not fecha:
        return False

    try:
        fecha_convertida = date.fromisoformat(fecha)
        return fecha_convertida >= date.today()
    except ValueError:
        return False


def filtrar_tareas_por_estado(tareas, estado):
    if estado not in ESTADOS_VALIDOS:
        return tareas

    return [
        tarea for tarea in tareas
        if tarea["estado"] == estado
    ]


def get_connection():
    intentos = 0

    while True:
        try:
            return psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                cursor_factory=psycopg2.extras.RealDictCursor,
            )
        except psycopg2.OperationalError:
            intentos += 1

            if intentos > 10:
                raise

            time.sleep(2)


@app.route("/")
def index():
    estado = request.args.get("estado")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, tarea, fecha_limite, estado FROM tareas ORDER BY id"
    )

    tareas = cur.fetchall()

    cur.close()
    conn.close()

    tareas_filtradas = filtrar_tareas_por_estado(tareas, estado)

    return render_template(
        "index.html",
        tareas=tareas_filtradas,
        estado_actual=estado if estado in ESTADOS_VALIDOS else None,
        estados_validos=sorted(ESTADOS_VALIDOS),
    )


@app.route("/api/tareas")
def api_tareas():
    estado = request.args.get("estado")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, tarea, fecha_limite, estado FROM tareas ORDER BY id"
    )

    tareas = cur.fetchall()

    cur.close()
    conn.close()

    tareas_filtradas = filtrar_tareas_por_estado(tareas, estado)

    return {
        "estado_filtro": estado if estado in ESTADOS_VALIDOS else None,
        "total": len(tareas_filtradas),
        "tareas": [dict(t) for t in tareas_filtradas],
    }


@app.route("/crear", methods=["POST"])
def crear():
    tarea = request.form.get("tarea", "").strip()
    fecha_limite = request.form.get("fecha_limite", "")
    estado = request.form.get("estado", ESTADO_POR_DEFECTO)

    if estado not in ESTADOS_VALIDOS:
        estado = ESTADO_POR_DEFECTO

    if not tarea:
        return redirect("/")

    if not validar_fecha_limite(fecha_limite):
        return "Fecha límite inválida. Debe ser hoy o una fecha futura.", 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tareas (tarea, fecha_limite, estado)
        VALUES (%s, %s, %s)
        """,
        (tarea, fecha_limite, estado),
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        tarea = request.form.get("tarea", "").strip()
        estado = request.form.get("estado", ESTADO_POR_DEFECTO)

        if estado not in ESTADOS_VALIDOS:
            estado = ESTADO_POR_DEFECTO

        if not tarea:
            cur.close()
            conn.close()
            return redirect("/")

        # Si el formulario incluye fecha, también se actualiza.
        if "fecha_limite" in request.form:
            fecha_limite = request.form.get("fecha_limite", "")

            if not validar_fecha_limite(fecha_limite):
                cur.close()
                conn.close()
                return "Fecha límite inválida. Debe ser hoy o una fecha futura.", 400

            cur.execute(
                """
                UPDATE tareas
                SET tarea = %s, fecha_limite = %s, estado = %s
                WHERE id = %s
                """,
                (tarea, fecha_limite, estado, id),
            )

        else:
            cur.execute(
                """
                UPDATE tareas
                SET tarea = %s, estado = %s
                WHERE id = %s
                """,
                (tarea, estado, id),
            )

        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")

    cur.execute(
        """
        SELECT id, tarea, fecha_limite, estado
        FROM tareas
        WHERE id = %s
        """,
        (id,),
    )

    fila = cur.fetchone()

    cur.close()
    conn.close()

    if fila is None:
        return redirect("/")

    return render_template(
        "editar.html",
        id=fila["id"],
        tarea=fila["tarea"],
        fecha_limite=fila["fecha_limite"],
        estado=fila["estado"],
        estados_validos=sorted(ESTADOS_VALIDOS),
    )


@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tareas WHERE id = %s",
        (id,),
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
