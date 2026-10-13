"""Cliente Neo4j oficial para el catálogo ficticio.

Ejecutar: python ejemplos/neo4j/app.py
Crear ejemplos/neo4j/.env a partir de .env.example (nunca subir secretos).
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


def buscar_libros_por_tema(driver, codigo: str, database: str = "neo4j") -> list[dict]:
    """Devuelve libros de un tema con Cypher parametrizado.

    Si el tema no existe, devuelve []. Los fallos de red/consulta NO se ocultan.
    """
    if not codigo or not codigo.strip():
        raise ValueError("El código del tema no puede estar vacío")
    records, _, _ = driver.execute_query(
        """
        MATCH (l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo:$codigo})
        RETURN l.isbn AS isbn, l.titulo AS titulo
        ORDER BY titulo
        """,
        codigo=codigo.strip(),
        database_=database,
    )
    return [record.data() for record in records]


def buscar_libro_por_isbn(driver, isbn: str, database: str = "neo4j") -> dict | None:
    """Busca por clave de negocio sin interpolar valores en Cypher."""
    if not isbn or not isbn.strip():
        raise ValueError("El ISBN no puede estar vacío")
    records, _, _ = driver.execute_query(
        """
        MATCH (l:Libro {isbn:$isbn})
        RETURN l.isbn AS isbn, l.titulo AS titulo
        """,
        isbn=isbn.strip(),
        database_=database,
    )
    return records[0].data() if records else None


def registrar_lectura_tx(tx, lector_id: str, isbn: str) -> bool:
    """Callback de transacción gestionada, seguro de repetir con MERGE.

    False indica que no se pudieron resolver ambos extremos.
    """
    record = tx.run(
        """
        MATCH (p:Lector {id:$lector})
        MATCH (l:Libro {isbn:$isbn})
        MERGE (p)-[:LEYO]->(l)
        RETURN p.id AS lector
        """,
        lector=lector_id,
        isbn=isbn,
    ).single()
    return record is not None


def main() -> None:
    load_dotenv(Path(__file__).with_name(".env"))
    uri = os.environ["NEO4J_URI"]
    username = os.environ["NEO4J_USERNAME"]
    password = os.environ["NEO4J_PASSWORD"]
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        driver.verify_connectivity()
        for libro in buscar_libros_por_tema(driver, "GRAFOS", database):
            print(f'{libro["isbn"]}: {libro["titulo"]}')


if __name__ == "__main__":
    main()
