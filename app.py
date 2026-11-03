import os
import time
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "tareas_db")
DB_USER = os.environ.get("DB_USER", "tareas_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "tareas_pass")

# Estados válidos que puede tener una tarea.
ESTADOS_VALIDOS = {"pendiente", "en_progreso", "completada"}
ESTADO_POR_DEFECTO = "pendiente"


def filtrar_tareas_por_estado(tareas, estado):
    """Filtra una lista de tareas por su estado.

    Es una función pura (no toca la base de datos ni Flask), para poder
    probarla de forma aislada con una prueba unitaria.

    - Si 'estado' es None, cadena vacía o no es uno de los
      ESTADOS_VALIDOS, se devuelve la lista completa sin filtrar
      (equivale a "mostrar todas").
    - Si 'estado' es válido, se devuelven solo las tareas cuyo campo
      'estado' coincide exactamente.
    """
    if not estado or estado not in ESTADOS_VALIDOS:
        return list(tareas)
    return [tarea for tarea in tareas if tarea["estado"] == estado]


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
    cur.execute("SELECT id, tarea, estado FROM tareas ORDER BY id")
    tareas = cur.fetchall()
    cur.close()
    conn.close()

    tareas_filtradas = filtrar_tareas_por_estado(tareas, estado)
    return render_template(
        "index.html",
        tareas=tareas_filtradas,
        estado_actual=estado,
        estados_validos=sorted(ESTADOS_VALIDOS),
    )


@app.route("/api/tareas")
def api_tareas():
    """Endpoint de la funcionalidad 'Filtro por estado'.

    GET /api/tareas            -> todas las tareas, en JSON.
    GET /api/tareas?estado=X   -> solo las tareas con estado == X.
    """
    estado = request.args.get("estado")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, tarea, estado FROM tareas ORDER BY id")
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
    tarea = request.form["tarea"].strip()
    estado = request.form.get("estado", ESTADO_POR_DEFECTO)
    if estado not in ESTADOS_VALIDOS:
        estado = ESTADO_POR_DEFECTO

    if tarea:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tareas (tarea, estado) VALUES (%s, %s)", (tarea, estado)
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
        tarea = request.form["tarea"].strip()
        estado = request.form.get("estado", ESTADO_POR_DEFECTO)
        if estado not in ESTADOS_VALIDOS:
            estado = ESTADO_POR_DEFECTO
        if tarea:
            cur.execute(
                "UPDATE tareas SET tarea = %s, estado = %s WHERE id = %s",
                (tarea, estado, id),
            )
            conn.commit()
        cur.close()
        conn.close()
        return redirect("/")

    cur.execute("SELECT id, tarea, estado FROM tareas WHERE id = %s", (id,))
    fila = cur.fetchone()
    cur.close()
    conn.close()

    if fila is None:
        return redirect("/")

    return render_template(
        "editar.html",
        id=fila["id"],
        tarea=fila["tarea"],
        estado=fila["estado"],
        estados_validos=sorted(ESTADOS_VALIDOS),
    )


@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tareas WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)