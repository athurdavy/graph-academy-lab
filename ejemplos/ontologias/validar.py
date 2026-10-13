"""Validación SHACL del catálogo ficticio. Ejecutar desde la raíz del repositorio."""
from pathlib import Path
from rdflib import Graph
from pyshacl import validate

ROOT = Path(__file__).resolve().parent
datos = Graph().parse(ROOT / "biblioteca.ttl", format="turtle")
formas = Graph().parse(ROOT / "shapes.ttl", format="turtle")
conforme, _informe, texto = validate(data_graph=datos, shacl_graph=formas, inference="none")
print(texto)
if not conforme:
    raise SystemExit("El catálogo no cumple las formas SHACL")
print("✅ Validación completada: datos conformes")
