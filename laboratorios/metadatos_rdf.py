"""Crea metadatos ficticios DCMI y exporta RDF en Turtle, N-Triples y JSON-LD."""
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, XSD

EX = Namespace("https://example.org/biblioteca/")
BIBO = Namespace("http://purl.org/ontology/bibo/")

def crear_grafo() -> Graph:
    g = Graph()
    g.bind("ex", EX)
    g.bind("dcterms", DCTERMS)
    g.bind("bibo", BIBO)
    libro = EX["libro001"]
    autor = EX["autor001"]
    g.add((libro, RDF.type, BIBO.Book))
    g.add((libro, DCTERMS.title, Literal("El mapa de los grafos", lang="es")))
    g.add((libro, DCTERMS.identifier, Literal("ISBN-001")))
    g.add((libro, DCTERMS.creator, autor))
    g.add((libro, DCTERMS.issued, Literal("2025", datatype=XSD.gYear)))
    return g

def exportar(directorio: Path) -> dict[str, Path]:
    directorio.mkdir(parents=True, exist_ok=True)
    g = crear_grafo()
    rutas = {"turtle": directorio / "biblioteca.ttl",
             "nt": directorio / "biblioteca.nt",
             "json-ld": directorio / "biblioteca.jsonld"}
    for formato, ruta in rutas.items():
        g.serialize(destination=str(ruta), format=formato)
    return rutas

if __name__ == "__main__":
    destino = Path(__file__).resolve().parent / "exportaciones"
    for formato, ruta in exportar(destino).items():
        print(f"{formato}: {ruta.name}")
