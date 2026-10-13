"""Ejecuta con: python -m pytest laboratorios/tests -q."""
from pathlib import Path
import importlib.util

import pytest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("biblioteca_lab", ROOT / "biblioteca.py")
biblioteca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(biblioteca)


def test_grafo_tiene_entidades_y_relaciones_esperadas():
    g = biblioteca.construir_biblioteca()
    assert g.number_of_nodes() == 5
    assert g.number_of_edges() == 4


def test_consulta_por_autor():
    g = biblioteca.construir_biblioteca()
    assert biblioteca.libros_de_autor(g, "A-001") == [
        "libro:ISBN-001",
        "libro:ISBN-002",
    ]


def test_consulta_por_tema():
    g = biblioteca.construir_biblioteca()
    assert biblioteca.libros_sobre_tema(g, "GRAFOS") == ["libro:ISBN-001"]


def test_identificador_inexistente_no_provoca_error():
    g = biblioteca.construir_biblioteca()
    assert biblioteca.libros_de_autor(g, "NO-EXISTE") == []
    assert biblioteca.libros_sobre_tema(g, "NO-EXISTE") == []


def test_no_confundir_direccion_de_la_relacion():
    g = biblioteca.construir_biblioteca()
    assert not g.has_edge("libro:ISBN-001", "autor:A-001")
    assert g.has_edge("autor:A-001", "libro:ISBN-001")


def test_no_confundir_tipos_de_relacion():
    g = biblioteca.construir_biblioteca()
    assert all(datos["tipo"] for _, _, datos in g.edges(data=True))
    assert biblioteca.libros_de_autor(g, "A-001") != biblioteca.libros_de_autor(g, "L-001")
