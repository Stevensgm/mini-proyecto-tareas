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
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, tarea FROM tareas ORDER BY id")
    tareas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tareas=tareas)


@app.route("/crear", methods=["POST"])
def crear():
    tarea = request.form["tarea"].strip()

    if tarea:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tareas (tarea) VALUES (%s)", (tarea,))
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
        if tarea:
            cur.execute("UPDATE tareas SET tarea = %s WHERE id = %s", (tarea, id))
            conn.commit()
        cur.close()
        conn.close()
        return redirect("/")

    cur.execute("SELECT id, tarea FROM tareas WHERE id = %s", (id,))
    fila = cur.fetchone()
    cur.close()
    conn.close()

    if fila is None:
        return redirect("/")

    return render_template("editar.html", id=fila["id"], tarea=fila["tarea"])


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