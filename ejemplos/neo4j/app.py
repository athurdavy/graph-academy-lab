"""Cliente educativo de Neo4j AuraDB. Datos de biblioteca ficticios."""
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

def buscar_libros_por_tema(driver, codigo: str, database: str = "neo4j") -> list[dict]:
    records, _, _ = driver.execute_query(
        """
        MATCH (l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo: $codigo})
        RETURN l.isbn AS isbn, l.titulo AS titulo
        ORDER BY titulo
        """,
        codigo=codigo,
        database_=database,
    )
    return [record.data() for record in records]

def main() -> None:
    load_dotenv()
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
