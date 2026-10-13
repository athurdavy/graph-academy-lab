# Examen práctico del bloque Neo4j · Del modelo a una aplicación Python

**Evaluación del campus, no examen oficial de Neo4j.** Duración sugerida: **3–5 horas**, con una pausa. Requisitos: semanas [04](semana-04.md), [05](semana-05.md), [06](semana-06.md), [07](semana-07.md). **Objetivo:** demostrar conocimientos con una base de biblioteca ficticia y no solo recordar definiciones.

![Modelo visual de la biblioteca de prácticas](../assets/biblioteca-grafo.svg)

## 1. Qué debes entregar y cómo se corrige

Esta prueba vale **100 puntos**, repartidos en:

| Parte | Competencia | Puntos |
|---|---|---:|
| A | Crear esquema y cargar datos idempotentes | 25 |
| B | Resolver consultas Cypher y explicar resultados | 35 |
| C | Driver Python, transacciones y errores | 25 |
| D | Interpretar modelo, índices y decisiones técnicas | 15 |

**Criterio interno orientativo:** 80/100 puntos o más, con un mínimo de **la mitad de los puntos de cada apartado** y sin exponer secretos. No corresponde a ninguna calificación oficial.

### Reglas

1. Utiliza únicamente el conjunto de datos público inventado.
2. Trabaja en una instancia de **pruebas**, idealmente limpia, para evitar interferencias con experimentos anteriores.
3. Guarda las respuestas como \`evaluacion.cypher\`, \`solucion.py\` y \`decisiones.md\`.
4. Antes de mirar las soluciones, intenta todas las preguntas y anota qué resultados esperas obtener.
5. No publiques contraseñas, tokens, URI privados ni capturas con credenciales.

## 2. Preparación del entorno

Desde una instancia Neo4j AuraDB de laboratorio, ejecuta el archivo [\`ejemplos/neo4j/01_biblioteca.cypher\`](../ejemplos/neo4j/01_biblioteca.cypher), que crea el dataset ficticio:

- Autores: **A-001, A-002**
- Libros: **ISBN-001, ISBN-002, ISBN-003**
- Temas: **GRAFOS, CIENCIA, NATURALEZA**
- Lector: **L-001**
- Autorías: Marina Soler escribió los dos primeros libros; Diego Ríos escribió el tercero.
- Clasificaciones: ISBN-001 → GRAFOS; ISBN-002 → GRAFOS y CIENCIA; ISBN-003 → NATURALEZA.
- Lecturas: L-001 leyó ISBN-001.

> **Importante:** si ya has practicado antes en la misma base pueden existir nodos adicionales. Para comparar cantidades, usa una base aislada o consultas con los identificadores concretos del examen. No borres un entorno compartido con \`DETACH DELETE\`.

Comprueba las entidades del laboratorio con una consulta explícita:

~~~cypher
MATCH (l:Libro)
WHERE l.isbn IN ['ISBN-001','ISBN-002','ISBN-003']
RETURN l.isbn AS isbn, l.titulo AS titulo ORDER BY isbn;
~~~

**Resultado esperado:** tres filas. Si no coinciden, revisa la carga antes de empezar.

## 3. Parte A · Esquema y carga (25 puntos)

### A1 — Diseña restricciones (8 puntos)

Define una restricción de unicidad para \`Libro.isbn\` y otra para \`Autor.id\`. Explica por qué *única* no significa *obligatoria*.

### A2 — Crea datos idempotentes (10 puntos)

Escribe Cypher para registrar:

- Autora ficticia: \`A-003\`, **Elena Vidal**
- Libro: \`ISBN-004\`, **Atlas de conexiones**, año 2025
- Tema: \`HISTORIA\`, **Historia**
- Relaciones \`ESCRIBIO\` y \`TRATA_SOBRE\` desde los nodos correctos.

Ejecuta el mismo script dos veces. Debe haber exactamente **un nodo para cada nueva clave** y una relación de cada tipo entre esos extremos.

### A3 — Detecta errores de referencia (7 puntos)

Tienes los ISBN \`ISBN-001\` e \`ISBN-DESCONOCIDO\`. Redacta una consulta que devuelva solo los ISBN que **no existen**. No crees nodos para ocultar el problema.

## 4. Parte B · Consultas Cypher (35 puntos)

Cada reto vale cinco puntos. Incluye la consulta, resultado esperado y una explicación del patrón.

**B1.** Lista título e ISBN de los libros de \`A-001\`, por ISBN.

**B2.** Encuentra libros sobre \`GRAFOS\` y devuelve su autora o autor, título e ISBN.

**B3.** Cuenta cuántos **libros distintos** escribió cada autor, ordenando por cantidad descendente.

**B4.** Lista **todos** los libros, aunque alguno no tenga tema. Debe aparecer un libro no clasificado si lo añades como experimento.

**B5.** Encuentra libros **sin relación de autoría registrada**. Explica por qué eso no demuestra que no tengan autor en la realidad.

**B6.** Muestra temas de \`A-001\` sin repetirlos. Deben aparecer \`GRAFOS\` y \`CIENCIA\`.

**B7.** Escribe una consulta con \`WITH\` que devuelva únicamente autores con **dos libros o más**.

### No te adelantes a las soluciones

Puedes comprobar que la consulta tiene sentido cambiando una única arista en una copia de la base de laboratorio y prediciendo si cambiará el resultado. No se evalúa solo que Cypher ejecute, sino que responda **la pregunta correcta**.

## 5. Parte C · Driver Python y transacciones (25 puntos)

**C1 (10 puntos).** Implementa la función:

~~~python
def buscar_por_tema(driver, codigo: str, database: str) -> list[dict]:
    ...
~~~

Debe usar \`$codigo\` como parámetro Cypher; devolver una lista de diccionarios con \`isbn\` y \`titulo\`; devolver \`[]\` para un tema no encontrado y rechazar un código vacío mediante un error explícito.

**C2 (10 puntos).** Escribe una función de transacción gestionada para crear la relación de lectura de un lector a un libro, **solo si existen ambos**; usa \`MERGE\` y explica qué efecto tiene un reintento.

**C3 (5 puntos).** Identifica qué está mal aquí:

~~~python
try:
    rows = driver.execute_query(query)
except Exception:
    return []
~~~

No resuelvas el problema repitiendo todas las excepciones de forma ilimitada.

## 6. Parte D · Razona como ingeniero (15 puntos)

**D1 (5 puntos).** Describe el modelo del caso, las claves estables y la dirección de sus relaciones. ¿Cómo representarías que un lector vuelve a leer un libro en otra fecha?

**D2 (5 puntos).** ¿Cuándo utilizarías \`EXPLAIN\` y cuándo \`PROFILE\`? ¿Por qué resulta peligroso perfilar una operación destructiva en una base con datos?

**D3 (5 puntos).** Si PostgreSQL lleva los préstamos y Neo4j proporciona una proyección de relaciones, ¿se actualizan ambos con una única transacción ACID? Define cómo detectarías y recuperarías una inconsistencia.

## 7. Plantilla de autocorrección

Primero completa tu entrega. Después consulta las [soluciones razonadas en la web](../laboratorios/08-evaluacion-neo4j-soluciones.md), donde se explica **por qué** es correcta cada consulta y qué errores habituales podrían aprobar una comprobación superficial.

### Revisión rápida del evaluador

- ¿Se ejecutan consultas con datos de entrada bien identificados?
- ¿La importación es repetible?
- ¿Se respetan dirección y tipos de las relaciones?
- ¿Se utiliza \`DISTINCT\` cuando corresponde, sin esconder duplicados reales?
- ¿Las consultas parametrizan correctamente los valores?
- ¿Se explica qué ocurre con referencias ausentes?
- ¿La aplicación diferencia una lista vacía de un error de infraestructura?
- ¿La entrega permite reproducir resultados sin datos confidenciales?

## 8. Siguiente etapa: el mismo catálogo en RDF

Cuando termines, ya sabes almacenar y consultar conexiones mediante un grafo de propiedades. La pregunta nueva es: **¿cómo publicamos esas afirmaciones de forma interoperable y con significado formal?**

En la [introducción a RDF y ontologías](semana-03.md) verás cómo escribir afirmaciones en triples y qué añade cada estándar. Más adelante entraremos en **SKOS, Dublin Core Terms, SPARQL, Protégé, OWL 2 y GraphDB** sin confundirlos con Cypher.

## Referencias oficiales

- [Neo4j Cypher — MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/)
- [Neo4j Cypher — MERGE](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
- [Neo4j Cypher — OPTIONAL MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/)
- [Neo4j Cypher — Query Tuning](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/query-tuning/)
- [Neo4j Python Driver — Transactions](https://neo4j.com/docs/python-manual/current/transactions/)

**Estado:** prueba redactada para el dataset público. La puntuación no está certificada ni supervisada; su ejecución de extremo a extremo en AuraDB deberá verificarse antes de considerarla una evaluación de integración validada.
