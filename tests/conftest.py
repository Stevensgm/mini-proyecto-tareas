import pytest

import app as tareas_app


class FakeCursor:
    def __init__(self, tareas):
        self.tareas = tareas
        self.resultados = []
        self.resultado = None

    def execute(self, query, params=None):
        consulta = " ".join(query.lower().split())

        if consulta == "select id, tarea, estado from tareas order by id":
            self.resultados = [dict(tarea) for tarea in self.tareas]
        elif consulta == "insert into tareas (tarea, estado) values (%s, %s)":
            siguiente_id = max((tarea["id"] for tarea in self.tareas), default=0) + 1
            self.tareas.append(
                {"id": siguiente_id, "tarea": params[0], "estado": params[1]}
            )
        elif consulta == "update tareas set tarea = %s, estado = %s where id = %s":
            for tarea in self.tareas:
                if tarea["id"] == params[2]:
                    tarea["tarea"] = params[0]
                    tarea["estado"] = params[1]
                    break
        elif consulta == "select id, tarea, estado from tareas where id = %s":
            self.resultado = next(
                (dict(tarea) for tarea in self.tareas if tarea["id"] == params[0]),
                None,
            )
        elif consulta == "delete from tareas where id = %s":
            self.tareas[:] = [
                tarea for tarea in self.tareas if tarea["id"] != params[0]
            ]
        else:
            raise AssertionError(f"Consulta SQL inesperada: {query}")

    def fetchall(self):
        return self.resultados

    def fetchone(self):
        return self.resultado

    def close(self):
        pass


class FakeConnection:
    def __init__(self, tareas):
        self.tareas = tareas

    def cursor(self):
        return FakeCursor(self.tareas)

    def commit(self):
        pass

    def close(self):
        pass


@pytest.fixture
def client(monkeypatch):
    tareas_app.app.config.update(TESTING=True)
    tareas = []
    monkeypatch.setattr(
        tareas_app,
        "get_connection",
        lambda: FakeConnection(tareas),
    )

    with tareas_app.app.test_client() as test_client:
        yield test_client
