"""Práctica reproducible de RDF y OWL (sin razonar automáticamente).

Solo usa identidades ficticias. Ejecutar:
python laboratorios/practica_owl_rdf.py
"""
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS

BASE = Path(__file__).resolve().parents[1]
ONTOLOGIA = BASE / "ejemplos" / "ontologias" / "ontologia-biblioteca.ttl"
EX = Namespace("https://example.org/biblioteca/")


def cargar() -> Graph:
    return Graph().parse(ONTOLOGIA, format="turtle")


def explicitos() -> dict[str, bool]:
    g = cargar()
    return {
        "libro_digital": (EX.libro001, RDF.type, EX.LibroDigital) in g,
        "subclase": (EX.LibroDigital, RDFS.subClassOf, EX.Libro) in g,
        "tipo_libro_materializado": (EX.libro001, RDF.type, EX.Libro) in g,
    }


def consultar_libros() -> list[tuple[str, str]]:
    g = cargar()
    # Sin inferencia: obtenemos libros explícitos o subclases explícitas.
    consulta = """
        PREFIX ex: <https://example.org/biblioteca/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?libro ?titulo WHERE {
          ?libro a/rdfs:subClassOf* ex:Libro ;
                 ex:titulo ?titulo .
        }
        ORDER BY ?titulo
    """
    return [(str(f.libro), str(f.titulo)) for f in g.query(consulta)]


def exportar_turtle(destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    cargar().serialize(destination=str(destino), format="turtle")


if __name__ == "__main__":
    print("Afirmaciones explícitas:", explicitos())
    print("Libros recuperados:", consultar_libros())
    exportar_turtle(BASE / "laboratorios" / "exportaciones" / "ontologia-biblioteca.ttl")
    print("Exportación Turtle generada en laboratorios/exportaciones/")
