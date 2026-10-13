# Semana 07 — Neo4j AuraDB desde Python

## Objetivos

Conectar mediante el driver oficial, ejecutar consultas parametrizadas, organizar código y manejar transacciones sin exponer credenciales.

## 1. Preparación

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\Activate.ps1
python -m pip install neo4j python-dotenv pytest
```

Crea un archivo local `.env` (no lo subas a GitHub):

```dotenv
NEO4J_URI=neo4j+s://TU_INSTANCIA.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=TU_PASSWORD
NEO4J_DATABASE=neo4j
```

Añade `.env` a `.gitignore`. El nombre de la base puede variar según la instancia.

## 2. Script de conexión

El fichero completo está en [`ejemplos/neo4j/app.py`](../ejemplos/neo4j/app.py).

```python
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

with GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
) as driver:
    driver.verify_connectivity()
    records, summary, keys = driver.execute_query(
        """
        MATCH (l:Libro)
        WHERE l.anio >= $desde
        RETURN l.isbn AS isbn, l.titulo AS titulo
        ORDER BY titulo
        """,
        desde=2020,
        database_=os.getenv("NEO4J_DATABASE", "neo4j"),
    )
    for record in records:
        print(record["isbn"], record["titulo"])
```

**Por qué parametrizar:** evita concatenar valores del usuario en el texto de la consulta, mejora seguridad y permite reutilizar planes. Las etiquetas y tipos de relación requieren consideraciones distintas según la versión de Cypher; no concatenes nombres arbitrarios provenientes de usuarios.

## 3. Transacciones

`driver.execute_query()` simplifica consultas habituales. Para agrupar varias operaciones atómicas usa sesiones y transacciones gestionadas:

```python
def guardar_lectura(tx, lector_id, isbn):
    tx.run("""
        MATCH (p:Lector {id:$lector_id})
        MATCH (l:Libro {isbn:$isbn})
        MERGE (p)-[:LEYO]->(l)
    """, lector_id=lector_id, isbn=isbn).consume()

with driver.session(database="neo4j") as session:
    session.execute_write(guardar_lectura, "L-001", "ISBN-001")
```

El ejemplo anterior es **un fragmento**, destinado a ejecutarse con un `driver` abierto. Para una implementación real, comprueba que ambos nodos existen y decide si múltiples lecturas requieren historial. Las funciones de transacción gestionada pueden reintentarse: evita efectos externos no idempotentes dentro de ellas.

## 4. Ejercicios

1. Implementa `buscar_libros_por_tema(codigo)` con parámetros.
2. Añade `listar_autores()` y ordenación alfabética.
3. Prueba qué ocurre con una contraseña incorrecta; no registres secretos en logs.
4. Separa configuración, consultas y presentación.
5. Escribe una prueba de integración que solo se ejecute si las variables de entorno están presentes.

### Solución de referencia: búsqueda por tema

```python
def buscar_libros_por_tema(driver, codigo, database="neo4j"):
    records, _, _ = driver.execute_query("""
        MATCH (l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo:$codigo})
        RETURN l.isbn AS isbn, l.titulo AS titulo
        ORDER BY titulo
    """, codigo=codigo, database_=database)
    return [record.data() for record in records]
```

## 5. Entregable final del bloque

Una aplicación CLI que cargue el dataset ficticio, liste libros por tema y registre lecturas; README de instalación, tests y explicación de decisiones.

## Referencias oficiales

- [Neo4j Python Driver Manual](https://neo4j.com/docs/python-manual/current/)
- [Conexión](https://neo4j.com/docs/python-manual/current/connect/)
- [Consultas](https://neo4j.com/docs/python-manual/current/query-simple/)
- [Transacciones](https://neo4j.com/docs/python-manual/current/transactions/)
