# Plan de estudios — 24 semanas

**La formación se consulta en la web:** [Entrar al lector de lecciones](https://athurdavy.github.io/graph-academy-lab/lecciones.html). Cada semana tiene su propia página con teoría y ejercicios; no es necesario navegar archivos Markdown en GitHub.

**Ruta adicional:** [Arquitectura con Neo4j, PostgreSQL, ORM/OGM y RDF](https://athurdavy.github.io/graph-academy-lab/lecciones.html?tema=arquitectura).

**Caso práctico:** biblioteca digital **completamente ficticia**, con libros, autores y temas inventados. No se utiliza información confidencial de ningún proyecto externo.

**Perfil de entrada:** Python y fundamentos de SQL. **Dedicación orientativa:** 8–10 h/semana.

| Semana | Objetivo | Entregable |
|---|---|---|
| 01 | Nodos, aristas, tipos y dirección | Modelo y tests NetworkX |
| 02 | Recorridos, caminos, centralidad y complejidad | Notebook de algoritmos |
| 03 | Grafos de propiedades frente a RDF | Dos representaciones del mismo dominio |
| 04 | Neo4j: entorno, Aura y seguridad básica | Base de prueba |
| 05 | Cypher: MATCH, WHERE, RETURN | 15 consultas |
| 06 | Escritura Cypher, MERGE, constraints e índices | Importación idempotente |
| 07 | Driver Python, transacciones y pruebas | CLI de consultas |
| 08 | ArcadeDB: arquitectura y modelos | Documento comparativo |
| 09 | ArcadeDB: consultas y APIs | Prototipo equivalente |
| 10 | Comparativa práctica y criterios de selección | Informe de decisión |
| 11 | Glosario, catálogo, taxonomía y ontología | Requisitos del catálogo |
| 12 | SKOS: conceptos, etiquetas y jerarquías | Vocabulario Turtle |
| 13 | RDF, URIs y SPARQL | Dataset y consultas |
| 14 | OWL: clases, propiedades e inferencia | Ontología mínima |
| 15 | SHACL: validación de vocabularios | Shapes y casos de prueba |
| 16 | Gobernanza, procedencia y versionado | Flujo editorial |
| 17 | Arquitectura: APIs, modelo y almacenamiento | ADR y diagrama |
| 18 | Knowledge graphs: integración y calidad | Grafo de conceptos y activos |
| 19 | NLP: extracción y evaluación | Conjunto anotado |
| 20 | Embeddings y recuperación | Comparativa de búsqueda |
| 21 | GraphRAG: patrones, límites y evaluación | Prototipo con fuentes |
| 22 | Integración del catálogo de biblioteca digital | MVP |
| 23 | Pruebas, seguridad y rendimiento | Informe de validación |
| 24 | Documentación y demostración | Proyecto final |

## Metodología semanal

1. Leer las referencias oficiales.
2. Replicar un ejemplo pequeño.
3. Resolver ejercicios sin copiar la solución.
4. Aplicar el concepto al catálogo de biblioteca digital.
5. Escribir una nota de decisiones y dudas.

## Rúbrica

- 30 % precisión conceptual.
- 30 % ejecución y pruebas reproducibles.
- 25 % aplicación razonada al proyecto.
- 15 % documentación y referencias.

## Material desarrollado

- [Semana 01: fundamentos de grafos](semana-01.md)
- [Semana 02: recorridos y algoritmos](semana-02.md)
- [Semana 03: grafos de propiedades y RDF](semana-03.md)
- [Caso práctico ficticio: biblioteca digital](proyecto-catálogo.md)

Las 24 semanas cuentan con páginas de formación, pero **su profundidad es desigual**: algunas ofrecen laboratorios extensos y soluciones; otras son primeras unidades prácticas que necesitan ampliar pruebas, ejemplos y teoría para alcanzar el mismo nivel.

## Lectura dentro de la web

Para acceder a cualquier semana usa `https://athurdavy.github.io/graph-academy-lab/lecciones.html?semana=NN`, donde `NN` es el número de dos dígitos de la semana. El código y los datos ficticios están en `ejemplos/neo4j/` y `ejemplos/ontologias/`.
