import importlib.util
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

source = Path(__file__).resolve().parents[1] / "arcadedb_http.py"
spec = importlib.util.spec_from_file_location("arcadedb_http_lab", source)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)


def test_respuesta_normal_se_convierte_en_lista():
    assert lab.extraer_libros_json({"result": [{"isbn": "ISBN-001"}]}) == [
        {"isbn": "ISBN-001"}
    ]


def test_respuesta_inesperada_no_se_confunde_con_lista_vacia():
    with pytest.raises(ValueError):
        lab.extraer_libros_json({"error": "autorizacion denegada"})


def test_solicitud_usa_json_correcto_y_timeout():
    session = Mock()
    session.post.return_value.json.return_value = {"result": []}
    assert lab.consultar_libros(
        session, "http://localhost:2480/", "biblioteca", "usuario", "clave"
    ) == []
    args, kwargs = session.post.call_args
    assert args[0] == "http://localhost:2480/api/v1/query/biblioteca"
    assert kwargs["json"] == {"language": "sql", "command": "SELECT FROM Libro"}
    assert kwargs["timeout"] == 10
    session.post.return_value.raise_for_status.assert_called_once_with()


def test_error_http_no_se_oculta():
    session = Mock()
    session.post.return_value.raise_for_status.side_effect = requests.HTTPError("401")
    with pytest.raises(requests.HTTPError):
        lab.consultar_libros(session, "http://localhost:2480", "biblioteca",
                             "usuario", "incorrecta")


def test_configuracion_vacia_falla_antes_de_enviar():
    session = Mock()
    with pytest.raises(ValueError):
        lab.consultar_libros(session, "", "biblioteca", "usuario", "clave")
    session.post.assert_not_called()


def test_timeout_se_propaga():
    session = Mock()
    session.post.side_effect = requests.Timeout("tiempo agotado")
    with pytest.raises(requests.Timeout):
        lab.consultar_libros(session, "http://localhost:2480", "biblioteca",
                             "usuario", "clave")
