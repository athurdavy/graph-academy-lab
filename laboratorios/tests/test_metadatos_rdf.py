"""Comprobar exportación y reimportación semántica, no igualdad textual de archivos."""
import importlib.util
from pathlib import Path

from rdflib import Graph
from rdflib.namespace import DCTERMS

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("metadatos", ROOT / "metadatos_rdf.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_metadatos_dcmi():
    g = m.crear_grafo()
    assert len(g) == 5
    assert any(True for _, _, _ in g.triples((None, DCTERMS.title, None)))
    assert any(True for _, _, _ in g.triples((None, DCTERMS.creator, None)))

def test_roundtrip_formatos(tmp_path):
    g = m.crear_grafo()
    archivos = m.exportar(tmp_path)
    assert set(archivos) == {"turtle", "nt", "json-ld"}
    for formato, archivo in archivos.items():
        leido = Graph().parse(str(archivo), format=formato)
        assert len(leido) == len(g)
        assert set(leido) == set(g)
