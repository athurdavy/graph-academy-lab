# Soluciones razonadas · Evaluación práctica de Neo4j

**Lee primero la [prueba](08-evaluacion-neo4j.md)**. Estas respuestas son una referencia técnica para autocorregirte: una solución diferente también puede ser válida si ofrece la misma semántica, no altera datos ajenos y es reproducible.

## Parte A — Datos

### A1 · Restricciones

~~~cypher
CREATE CONSTRAINT libro_isbn IF NOT EXISTS FOR (l:Libro) REQUIRE l.isbn IS UNIQUE;
CREATE CONSTRAINT autor_id IF NOT EXISTS FOR (a:Autor) REQUIRE a.id IS UNIQUE;
~~~

La unicidad restringe valores **presentes** para una etiqueta. No impone por sí sola que la propiedad exista.

### A2 · Escritura idempotente

~~~cypher
MERGE (a:Autor {id:'A-003'})
SET a.nombre='Elena Vidal'
MERGE (l:Libro {isbn:'ISBN-004'})
SET l.titulo='Atlas de conexiones', l.anio=2025
MERGE (t:Tema {codigo:'HISTORIA'})
SET t.nombre='Historia'
MERGE (a)-[:ESCRIBIO]->(l)
MERGE (l)-[:TRATA_SOBRE]->(t);
~~~

El nodo se identifica mediante clave; los campos que pueden cambiar se actualizan con \`SET\`. El patrón de relación se fusiona **entre los nodos ya identificados**. Las constraints de unicidad ayudan bajo concurrencia, pero no sustituyen la gobernanza de identificadores.

**Comprobación:**

~~~cypher
MATCH (a:Autor {id:'A-003'})-[:ESCRIBIO]->(l:Libro {isbn:'ISBN-004'})-[:TRATA_SOBRE]->(t:Tema {codigo:'HISTORIA'})
RETURN count(*) AS recorridos;
~~~

Esperado: **1** si el entorno estaba limpio y no introdujiste relaciones paralelas adicionales.

### A3 · Referencias sin resolver

~~~cypher
UNWIND ['ISBN-001','ISBN-DESCONOCIDO'] AS isbn
OPTIONAL MATCH (l:Libro {isbn:isbn})
WITH isbn,l
WHERE l IS NULL
RETURN isbn AS referencia_inexistente;
~~~

Esperado: \`ISBN-DESCONOCIDO\`. Un \`MATCH\` obligatorio eliminaría directamente la fila ausente, ocultando el error de referencia.

## Parte B — Consultas

**B1 · Libros del autor:**

~~~cypher
MATCH (a:Autor {id:'A-001'})-[:ESCRIBIO]->(l:Libro)
RETURN l.isbn AS isbn, l.titulo AS titulo
ORDER BY isbn;
~~~

Esperado: \`ISBN-001\`, \`ISBN-002\`.

**B2 · Libros sobre grafos y sus autores:**

~~~cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo:'GRAFOS'})
RETURN a.nombre AS autor, l.isbn AS isbn, l.titulo AS titulo
ORDER BY isbn;
~~~

Esperado: Marina, ISBN-001; Marina, ISBN-002. La consulta exige dos relaciones dirigidas.

**B3 · Recuento de libros distintos por autor:**

~~~cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
RETURN a.nombre AS autor, count(DISTINCT l) AS total
ORDER BY total DESC, autor;
~~~

Esperado en el dataset principal: Marina 2, Diego 1. Si incluyes A-003, verás también Elena 1. \`DISTINCT\` elimina repeticiones en las filas de agregación, **no** repara entidades duplicadas.

**B4 · Todos los libros:**

~~~cypher
MATCH (l:Libro)
OPTIONAL MATCH (l)-[:TRATA_SOBRE]->(t:Tema)
RETURN l.isbn AS isbn, collect(t.nombre) AS temas
ORDER BY isbn;
~~~

\`OPTIONAL MATCH\` conserva la fila de Libro aun sin tema. \`collect\` reúne nombres disponibles; examina casos con \`null\` antes de aplicar la consulta a datos reales.

**B5 · Libros sin autoría:**

~~~cypher
MATCH (l:Libro)
WHERE NOT EXISTS { MATCH (:Autor)-[:ESCRIBIO]->(l) }
RETURN l.isbn AS isbn, l.titulo AS titulo;
~~~

Con el dataset de tres libros original, no deberían aparecer filas. Si añadiste libros sin autor, aparecerán. Falta de datos almacenados no equivale a falta de autor en el mundo real.

**B6 · Temas del autor A-001:**

~~~cypher
MATCH (a:Autor {id:'A-001'})-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema)
RETURN DISTINCT t.codigo AS tema
ORDER BY tema;
~~~

Esperado: \`CIENCIA\` y \`GRAFOS\`.

**B7 · Autores con dos libros o más:**

~~~cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
WITH a, count(DISTINCT l) AS total
WHERE total >= 2
RETURN a.nombre AS autor, total
ORDER BY total DESC;
~~~

Esperado: Marina, 2. \`WITH\` permite filtrar el valor agregado y reduce el ámbito de variables.

## Parte C — Python

**C1 · Búsqueda parametrizada:**

~~~python
def buscar_por_tema(driver, codigo: str, database: str) -> list[dict]:
    if not codigo or not codigo.strip():
        raise ValueError("Código de tema vacío")
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
~~~

No concatenamos \`codigo\` dentro de Cypher. La función distingue una consulta sin filas de un error de conectividad.

**C2 · Registrar lectura dentro de una transacción:**

~~~python
def guardar_lectura(tx, lector_id: str, isbn: str) -> bool:
    record = tx.run(
        """
        MATCH (p:Lector {id:$lector})
        MATCH (l:Libro {isbn:$isbn})
        MERGE (p)-[:LEYO]->(l)
        RETURN p.id AS id
        """,
        lector=lector_id, isbn=isbn,
    ).single()
    return record is not None
~~~

Invocación, con \`driver\` abierto:

~~~python
with driver.session(database="neo4j") as session:
    resultado = session.execute_write(guardar_lectura, "L-001", "ISBN-001")
~~~

\`execute_write\` puede reintentar la función ante errores transitorios: evita enviar efectos externos no idempotentes dentro de ella. Para registrar múltiples lecturas históricas necesitarías otro diseño, porque el \`MERGE\` simple anterior no guarda sesiones de lectura repetidas.

**C3 · Error oculto:**

~~~python
try:
    rows = driver.execute_query(query)
except Exception:
    return []
~~~

La captura general es incorrecta: un fallo de autenticación, red o sintaxis parecería una consulta sin libros. Debes manejar excepciones pertinentes, informar de errores y establecer políticas de reintentos según el tipo de fallo.

## Parte D — Diseño y operación

**D1.** Claves ficticias estables: \`Autor.id\`, \`Libro.isbn\`, \`Tema.codigo\`, \`Lector.id\`. Relaciones con dirección: Autor → Libro, Libro → Tema, Lector → Libro. Para múltiples lecturas conserva un evento o relaciones con IDs y fechas, según necesidades de auditoría.

**D2.** \`EXPLAIN\` muestra un plan estimado sin ejecutar; \`PROFILE\` ejecuta e informa métricas. Perfilar consultas destructivas modifica datos.

**D3.** PostgreSQL y Neo4j no comparten por defecto una transacción atómica entre motores. Una arquitectura híbrida debe definir fuente de verdad, outbox/eventos, reintentos idempotentes y reconciliación.

## Tabla de autocorrección

| Apartado | Puntos máximos | Condición |
|---|---:|---|
| A1 | 8 | Dos constraints correctas y semántica explicada |
| A2 | 10 | Claves estables, relaciones bien dirigidas, repetición sin duplicados |
| A3 | 7 | Devuelve únicamente la referencia inexistente |
| B1–B7 | 35 | Cinco puntos por consulta correcta y resultado explicado |
| C1 | 10 | Parámetros, lista/ausencia, validación |
| C2 | 10 | Transacción y referencia existente |
| C3 | 5 | Explica errores ocultos y la solución |
| D1–D3 | 15 | Cinco puntos por justificación técnicamente fundada |

**No te autoacredites por coincidir con los ejemplos.** Cambia un identificador, crea un registro sin tema y confirma que las consultas responden adecuadamente a un caso nuevo.

## Fuentes

- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [GraphAcademy](https://graphacademy.neo4j.com/)
