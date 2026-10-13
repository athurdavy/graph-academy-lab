from pathlib import Path
import importlib.util
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("servicios_lab", ROOT / "servicios.py")
servicios = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = servicios
spec.loader.exec_module(servicios)


def test_caso_de_uso_consulta_repositorio_sin_bbdd():
    repo = servicios.RepositorioMemoria([
        servicios.Libro("ISBN-001", "El mapa de los grafos")
    ])
    caso = servicios.ConsultarLibro(repo)
    assert caso.ejecutar("ISBN-001").titulo == "El mapa de los grafos"
    assert caso.ejecutar("ISBN-999") is None


def test_no_acepta_identificador_vacio():
    caso = servicios.ConsultarLibro(servicios.RepositorioMemoria([]))
    with pytest.raises(ValueError):
        caso.ejecutar("   ")


def test_limpieza_de_espacios_en_identificador():
    caso = servicios.ConsultarLibro(
        servicios.RepositorioMemoria([servicios.Libro("ISBN-001", "Libro")])
    )
    assert caso.ejecutar(" ISBN-001 ").isbn == "ISBN-001"
