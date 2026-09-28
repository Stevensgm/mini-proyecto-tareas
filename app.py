from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tareas = []

@app.route("/")
def index():
    return render_template("index.html", tareas=tareas)

@app.route("/crear", methods=["POST"])
def crear():
    tarea = request.form["tarea"]

    if tarea.strip():
        tareas.append(tarea)

    return redirect("/")

@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    tarea = request.form["tarea"].strip()

    if 0 <= id < len(tareas) and tarea:
        tareas[id] = tarea

    return redirect("/")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    if 0 <= id < len(tareas):
        tareas.pop(id)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)