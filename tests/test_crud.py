def test_inicio_muestra_estado_vacio(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Lista de tareas" in response.get_data(as_text=True)
    assert "Todavía no hay tareas" in response.get_data(as_text=True)


def test_crear_tarea_y_mostrarla(client):
    response = client.post("/crear", data={"tarea": "  Estudiar  "})
    pagina = client.get("/")

    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    assert "Estudiar" in pagina.get_data(as_text=True)


def test_no_crear_tarea_vacia(client):
    response = client.post("/crear", data={"tarea": "   "})

    assert response.status_code == 302
    assert "Todavía no hay tareas" in client.get("/").get_data(as_text=True)


def test_editar_muestra_formulario_de_tarea_existente(client):
    client.post("/crear", data={"tarea": "Pendiente"})

    response = client.get("/editar/1")

    assert response.status_code == 200
    assert "value=\"Pendiente\"" in response.get_data(as_text=True)


def test_editar_tarea(client):
    client.post("/crear", data={"tarea": "Texto anterior"})

    response = client.post("/editar/1", data={"tarea": "Texto actualizado"})
    contenido = client.get("/").get_data(as_text=True)

    assert response.status_code == 302
    assert "Texto actualizado" in contenido
    assert "Texto anterior" not in contenido


def test_no_reemplazar_tarea_con_texto_vacio(client):
    client.post("/crear", data={"tarea": "Conservar"})

    response = client.post("/editar/1", data={"tarea": "   "})
    contenido = client.get("/").get_data(as_text=True)

    assert response.status_code == 302
    assert "Conservar" in contenido


def test_eliminar_tarea(client):
    client.post("/crear", data={"tarea": "Eliminar"})

    response = client.get("/eliminar/1")
    contenido = client.get("/").get_data(as_text=True)

    assert response.status_code == 302
    assert "Eliminar" not in contenido


def test_editar_tarea_inexistente_redirige_al_inicio(client):
    response = client.get("/editar/42")

    assert response.status_code == 302
    assert response.headers["Location"] == "/"
