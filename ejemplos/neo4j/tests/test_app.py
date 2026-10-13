"""Pruebas sin red del cliente Python de Neo4j.

Ejecutar desde raíz:
python -m pip install -r ejemplos/neo4j/requirements.txt
python -m pytest ejemplos/neo4j/tests -q
"""
import importlib.util
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest


APP = Path(__file__).resolve().parents[1] / "app.py"
spec = importlib.util.spec_from_file_location("neo4j_training_app", APP)
app = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = app
spec.loader.exec_module(app)


def record(**data):
    result = Mock()
    result.data.return_value = data
    return result


def test_libros_por_tema_usa_parametro_y_devuelve_datos():
    driver = Mock()
    driver.execute_query.return_value = (
        [record(isbn="ISBN-001", titulo="El mapa de los grafos")],
        Mock(), ["isbn", "titulo"],
    )
    result = app.buscar_libros_por_tema(driver, " GRAFOS ", "neo4j")
    assert result == [{"isbn": "ISBN-001", "titulo": "El mapa de los grafos"}]
    args, kwargs = driver.execute_query.call_args
    assert "$codigo" in args[0]
    assert kwargs["codigo"] == "GRAFOS"
    assert kwargs["database_"] == "neo4j"


def test_busqueda_ausente_devuelve_lista_vacia():
    driver = Mock()
    driver.execute_query.return_value = ([], Mock(), ["isbn", "titulo"])
    assert app.buscar_libros_por_tema(driver, "INEXISTENTE") == []


def test_parametro_vacio_se_rechaza_antes_de_consultar():
    driver = Mock()
    with pytest.raises(ValueError):
        app.buscar_libros_por_tema(driver, "  ")
    driver.execute_query.assert_not_called()


def test_buscar_por_isbn_inexistente_devuelve_none():
    driver = Mock()
    driver.execute_query.return_value = ([], Mock(), [])
    assert app.buscar_libro_por_isbn(driver, "ISBN-999") is None
    assert driver.execute_query.call_args.kwargs["isbn"] == "ISBN-999"


def test_transaccion_devuelve_true_si_existen_ambos_extremos():
    tx = Mock()
    tx.run.return_value.single.return_value = record(lector="L-001")
    assert app.registrar_lectura_tx(tx, "L-001", "ISBN-001") is True
    assert tx.run.call_args.kwargs == {"lector": "L-001", "isbn": "ISBN-001"}


def test_transaccion_devuelve_false_si_falta_referencia():
    tx = Mock()
    tx.run.return_value.single.return_value = None
    assert app.registrar_lectura_tx(tx, "L-001", "NO-EXISTE") is False


def test_no_se_oculta_error_del_driver():
    driver = Mock()
    driver.execute_query.side_effect = RuntimeError("conexión fallida")
    with pytest.raises(RuntimeError, match="conexión fallida"):
        app.buscar_libros_por_tema(driver, "GRAFOS")
