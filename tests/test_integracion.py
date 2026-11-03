from datetime import date


def test_flujo_completo_de_tareas(client):
    fecha = date.today().isoformat()

    client.post("/crear", data={
        "tarea": "Primera",
        "fecha_limite": fecha
    })

    client.post("/crear", data={
        "tarea": "Segunda",
        "fecha_limite": fecha
    })

    client.post("/editar/1", data={
        "tarea": "Primera actualizada"
    })

    client.get("/eliminar/2")

    response = client.get("/")
    contenido = response.get_data(as_text=True)

    assert response.status_code == 201
    assert "Primera actualizada" in contenido
    assert "Segunda" not in contenido