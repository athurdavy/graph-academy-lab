"""Valida RDF/SHACL usando los archivos ficticios de la academia."""
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, RDF
from rdflib.namespace import XSD


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "ejemplos" / "ontologias" / "biblioteca.ttl"
SHAPES = ROOT / "ejemplos" / "ontologias" / "shapes.ttl"
EX = Namespace("https://example.org/biblioteca/")


def carga():
    return Graph().parse(DATA, format="turtle")


def formas():
    return Graph().parse(SHAPES, format="turtle")


def test_datos_ficticios_validos():
    conforms, _, report = validate(
        data_graph=carga(), shacl_graph=formas(), inference="none"
    )
    assert conforms, str(report)


def test_quitar_titulo_produce_error_shacl():
    datos = carga()
    for objeto in list(datos.objects(EX.libro001, EX.titulo)):
        datos.remove((EX.libro001, EX.titulo, objeto))
    conforms, _, report = validate(
        data_graph=datos, shacl_graph=formas(), inference="none"
    )
    assert not conforms
    assert "minCount" in str(report) or "MinCount" in str(report)


def test_tipos_explicitos():
    datos = carga()
    assert (EX.libro001, RDF.type, EX.Libro) in datos
