# Extensión de preparación para certificaciones Neo4j

**Material independiente en español.** Preparación basada en los temarios **públicos y oficiales** de GraphAcademy. No es un examen oficial ni garantiza aprobar. Esta extensión complementa las lecciones y laboratorios de la academia sin sustituir el programa de ontologías RDF/OWL/GraphDB.

## 1. Neo4j Certified Professional

**Formato oficial consultado (octubre 2026):** 80 preguntas, 60 minutos, aprobación a partir de 80 %. Preguntas de opción múltiple, selección múltiple y retos prácticos Cypher.

| Dominio oficial | Preguntas | Preparación interna |
|---|---:|---|
| Cypher | 32 | Semanas 5 y 6; 30 consultas, OPTIONAL MATCH, WITH, listas, agregación, patrones |
| Neo4j Fundamentals | 11 | Semanas 1, 3 y 4 |
| Schema & Indexes | 9 | Semanas 4, 6 y 23 |
| Drivers | 8 | Semana 7, laboratorio 03 y manejo de transacciones |
| Data Modeling | 8 | Semanas 3 y 4; diseño y cardinalidades |
| Importing Data | 6 | Semana 6; CSV, UNWIND y Data Importer |
| Hands-on challenges | 6 | Laboratorio 03 y ejercicios de Cypher |

*Las áreas suman 80 según la página oficial. Los retos prácticos constituyen una categoría propia en este desglose.*

**Preparación oficial recomendada:** Neo4j Fundamentals; Cypher Fundamentals; Graph Data Modeling Fundamentals; Importing Data Fundamentals; Using Neo4j with Python; Neo4j & Generative AI Fundamentals.

**Pruebas mínimas internas:**
1. Crear una base de biblioteca ficticia idempotente y probar restricciones.
2. Escribir 30 consultas Cypher, incluyendo agregaciones, patrones de 2 saltos y subconsultas de existencia.
3. Corregir una consulta que devuelve filas duplicadas y justificar cuándo usar DISTINCT.
4. Elegir un índice razonando con EXPLAIN/PROFILE.
5. Conectarse con el driver oficial y usar parámetros y transacciones gestionadas.

## 2. Graph Data Science Certification

**Formato oficial:** 50 preguntas, 60 minutos, 80 % mínimo.

| Dominio oficial | Preguntas | Preparación interna |
|---|---:|---|
| Algoritmos | 25 | Caminos mínimos, centralidad, comunidades, PageRank, ponderaciones |
| Workflows | 17 | Proyección en memoria, modo stats/stream/mutate/write, evaluación |
| GDS Library | 8 | Catálogo, configuración, tipos de proyecciones y procedimientos |

**Condición necesaria:** los laboratorios anteriores de NetworkX no sustituyen a GDS. Debes ejecutar prácticas específicas de la librería en un entorno Neo4j/GDS compatible antes del examen.

**Pruebas mínimas:** proyectar un grafo, ejecutar dos algoritmos apropiados para diferentes preguntas, interpretar resultados y destruir una proyección temporal sin confundirla con borrar datos persistidos.

## 3. Neo4j & Generative AI Certification

**Formato oficial:** 50 preguntas, 60 minutos, 80 % mínimo.

| Dominio oficial | Preguntas |
|---|---:|
| GraphRAG & Vectors | 15 |
| Data Modeling | 10 |
| Vectors | 6 |
| MCP | 6 |
| Neo4j Fundamentals | 5 |
| Cypher | 5 |
| Schema & Indexes | 2 |
| Drivers | 1 |

**Pruebas mínimas:** diseñar una recuperación que cite nodos y fuentes; distinguir similitud vectorial de afirmaciones comprobadas; justificar búsqueda híbrida, construcción del grafo y evaluación de respuestas. MCP debe estudiarse sobre documentación vigente por su evolución.

## 4. Método para estudiar

1. Lee el tema en español y la norma/documentación primaria asociada.
2. Ejecuta los laboratorios con datos ficticios y guarda evidencias.
3. Responde preguntas **sin mirar documentación** para detectar lagunas.
4. Revisa una explicación por cada error y repite la práctica correspondiente.
5. Haz un simulacro original completo de duración y distribución equivalentes al examen **cuando esté implementado**.
6. Como criterio de prudencia, busca >=90 % repetido en simulacros nuevos, ninguna área debajo del 80 % y retos prácticos completados sin ayuda. Esto es **criterio de estudio propio, no exigencia oficial**.

## 5. Estado y honestidad de cobertura

- **Ya disponible:** lector interactivo de práctica con preguntas originales, explicación y corrección por dominio.
- **Pendiente:** simulacros completos de 80/50/50 preguntas originales, validados conceptualmente, y laboratorios específicos completos de GDS y GraphRAG.
- **No equivale:** una buena nota en nuestro cuestionario breve no predice necesariamente una nota suficiente en el examen oficial.

## Referencias oficiales

- [Neo4j Certified Professional](https://graphacademy.neo4j.com/certifications/neo4j-certification)
- [Graph Data Science Certification](https://graphacademy.neo4j.com/certifications/gds-certification)
- [Neo4j & Generative AI Certification](https://graphacademy.neo4j.com/certifications/genai-certification)
- [Neo4j GraphAcademy: cursos](https://graphacademy.neo4j.com/courses)
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Graph Data Science Manual](https://neo4j.com/docs/graph-data-science/current/)
- [Neo4j GraphRAG Python](https://neo4j.com/docs/neo4j-graphrag-python/current/)
