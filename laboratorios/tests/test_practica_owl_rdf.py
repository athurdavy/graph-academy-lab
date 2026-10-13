"""Comprobaciones de estructura RDF, SPARQL y serialización sin servidor RDF."""
from pathlib import Path
import importlib.util
import sys

from rdflib import Graph, Namespace, RDF

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("practica_owl_rdf", ROOT / "practica_owl_rdf.py")
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)
EX = Namespace("https://example.org/biblioteca/")


def test_tipos_explicitos_y_no_materializados():
    estado = lab.explicitos()
    assert estado["libro_digital"]
    assert estado["subclase"]
    assert not estado["tipo_libro_materializado"]


def test_sparql_recupera_instancias_de_subclase_sin_materializar():
    result = lab.consultar_libros()
    assert len(result) == 2
    assert [title for _, title in result] == ["El mapa de los grafos", "Rutas de conocimiento"]


def test_exportacion_conserva_triples(tmp_path):
    out = tmp_path / "ontologia.ttl"
    lab.exportar_turtle(out)
    original = lab.cargar()
    recuperado = Graph().parse(out, format="turtle")
    assert set(original) == set(recuperado)
    assert (EX.libro001, RDF.type, EX.LibroDigital) in recuperado
