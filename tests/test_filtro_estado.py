"""Pruebas unitarias de la funcionalidad 'Filtro por estado' (Steven).

Prueban filtrar_tareas_por_estado() de forma aislada: no requieren
PostgreSQL ni el cliente de Flask, porque la función no toca la base
de datos ni la app. Se ejecutan junto al resto de la suite con:

    python -m pytest -q
"""

from app import filtrar_tareas_por_estado


TAREAS_EJEMPLO = [
    {"id": 1, "tarea": "Diseñar wireframes", "estado": "pendiente"},
    {"id": 2, "tarea": "Configurar base de datos", "estado": "completada"},
    {"id": 3, "tarea": "Escribir pruebas", "estado": "en_progreso"},
    {"id": 4, "tarea": "Revisar PR de Steven", "estado": "pendiente"},
]


def test_filtrar_por_estado_pendiente():
    resultado = filtrar_tareas_por_estado(TAREAS_EJEMPLO, "pendiente")
    assert [t["id"] for t in resultado] == [1, 4]


def test_filtrar_por_estado_en_progreso():
    resultado = filtrar_tareas_por_estado(TAREAS_EJEMPLO, "en_progreso")
    assert [t["id"] for t in resultado] == [3]


def test_filtrar_por_estado_completada():
    resultado = filtrar_tareas_por_estado(TAREAS_EJEMPLO, "completada")
    assert [t["id"] for t in resultado] == [2]


def test_filtrar_sin_estado_devuelve_todas():
    # estado=None equivale a no mandar el parámetro ?estado=
    resultado = filtrar_tareas_por_estado(TAREAS_EJEMPLO, None)
    assert resultado == TAREAS_EJEMPLO


def test_filtrar_estado_vacio_devuelve_todas():
    resultado = filtrar_tareas_por_estado(TAREAS_EJEMPLO, "")
    assert resultado == TAREAS_EJEMPLO


def test_filtrar_estado_invalido_devuelve_todas():
    # Un valor que no es ninguno de los tres estados reales del sistema
    resultado = filtrar_tareas_por_estado(TAREAS_EJEMPLO, "archivada")
    assert resultado == TAREAS_EJEMPLO


def test_filtrar_estado_sin_coincidencias():
    tareas_solo_pendientes = [
        {"id": 1, "tarea": "Tarea 1", "estado": "pendiente"},
    ]
    resultado = filtrar_tareas_por_estado(tareas_solo_pendientes, "completada")
    assert resultado == []


def test_filtrar_lista_vacia():
    resultado = filtrar_tareas_por_estado([], "pendiente")
    assert resultado == []
