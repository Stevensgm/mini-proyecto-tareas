def test_flujo_completo_de_tareas(client):
    client.post("/crear", data={"tarea": "Primera"})
    client.post("/crear", data={"tarea": "Segunda"})

    client.post("/editar/1", data={"tarea": "Primera actualizada"})
    client.get("/eliminar/2")

    response = client.get("/")
    contenido = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Primera actualizada" in contenido
    assert "Segunda" not in contenido
