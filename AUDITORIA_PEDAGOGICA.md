# Auditoría pedagógica y criterio de calidad — octubre 2026

## Veredicto desde la perspectiva de un programador que empieza desde cero

**No: el material actual no basta todavía para garantizar la preparación de un experto.** Hay 24 lecciones de profundidad desigual y una ruta extendida de 42 competencias. Las unidades avanzadas de GraphDB, Protégé, OWL, SPARQL, GDS, ORM/OGM y GraphRAG requieren laboratorios integrales y evaluación adicional.

## Problemas identificados

- Existían itinerarios distintos y recursos dispersos sin una entrada única para principiantes.
- Los primeros ejemplos cambiaban de dominio, dificultando seguir un solo caso.
- Las definiciones no siempre se explicaban antes de introducir operaciones sobre ellas.
- Algunos temas complejos tienen una descripción breve que no es una clase completa.
- Las pruebas y las preguntas de práctica no cubren todos los resultados de aprendizaje.
- No hay verificación completa, humana y reproducible de todas las herramientas y versiones.
- Un índice o una lista de estándares no equivale a saber diseñar una ontología.

## Cambios concretos implantados

- Página de orientación desde cero: empezar.html.
- Ruta secuencial y transparente: ruta.html.
- Lecciones iniciales 01, 02 y 03 reescritas con el mismo catálogo ficticio, ejemplos y resultados esperados.
- Semana 04 ampliada con transición de NetworkX a Neo4j.
- Lector con apartados internos, índice de cada unidad, botones de copia y navegación de módulos agrupada.
- Acceso al contenido desde el campus, manteniendo los laboratorios y la extensión de exámenes separados.

## Criterios para dar por terminada una clase

1. Objetivo observable y conocimientos previos explícitos.
2. Explicación desde cero con motivación del problema.
3. Dibujo técnico con significado de relaciones y leyenda.
4. Ejemplo pequeño ejecutable explicado línea por línea.
5. Instrucciones, versiones de dependencia y salida esperada.
6. Experimento donde se cambia un dato y se interpreta el resultado.
7. Tres ejercicios de complejidad progresiva.
8. Soluciones razonadas y explicación de errores comunes.
9. Pruebas unitarias o de integración y al menos un caso negativo.
10. Preguntas de autoevaluación antes de pasar a la siguiente unidad.
11. Referencias primarias y distinción entre norma, práctica e hipótesis.
12. Revisión técnica y editorial antes de marcarla como completa.

## Cobertura pendiente

| Bloque | Estado de calidad | Trabajo importante pendiente |
|---|---|---|
| Fundamentos 1–3 | Reestructurados | Revisión técnica e integración con ejercicios |
| Neo4j / Cypher | Parcial | Lenguaje completo, transacciones, índices, seguridad y GDS |
| ArcadeDB | Parcial | Despliegue y comparativa reproducible |
| RDF / SPARQL | Parcial | Named graphs, SPARQL avanzado y validación |
| SKOS / DCMI | Parcial | Alineación, metadatos y gobernanza |
| OWL / Protégé | Insuficiente para experto | Axiomas, razonadores, perfiles, inferencia y práctica extensa |
| GraphDB | Guía introductoria | Repositorios ejecutados, inferencia y SHACL real |
| ORM / OGM | Parcial | SQLAlchemy y neomodel con código integrador |
| GraphRAG | Introductorio | Pipeline completo y evaluación de respuestas |
| Certificaciones | Banco inicial | Simulacros amplios y práctica oficial equivalente |

**No declarar aprobado, experto ni titulado a alguien solo por recorrer los enlaces.** El programa es independiente y no concede acreditación oficial.
## Revisión centrada en las primeras cuatro unidades — octubre de 2026

**Perspectiva:** estudiante que sabe Python y SQL, no conoce bases de grafos ni ontologías. Esta matriz es una evaluación editorial **cualitativa**; no procede de un estudio empírico con alumnado ni de resultados reales de examen.

| Unidad | Orden y prerrequisitos | Comprensibilidad | Reproducibilidad | Acción editorial |
|---|---|---|---|---|
| 01. Pensar en grafos | Adecuados como comienzo | Faltaba enseñar cómo decidir entidades, identidad y cardinalidad | Ejemplo NetworkX y tests disponibles | Se ha añadido modelado desde frases, comparación SQL y primera construcción explicada |
| 02. Recorridos | Debe ir después del modelo | Siglas y diagramas ya explicados, pero faltaba contexto del caso | BFS, DFS y Dijkstra con Python y tests | Se añade un recorrido Autor→Libro→Tema con filtros semánticos |
| 03. Propiedades y RDF | Es un **puente introductorio**, no un curso de ontologías | El vocabulario de RDF puede abrumar si se adelantan SKOS, OWL y SHACL | Laboratorio de RDFLib publicado, sin integración universal verificada | Se distingue explícitamente materia obligatoria de conceptos que se estudiarán en la semana 11 |
| 04. Neo4j desde cero | A continuación del modelo y su comparación con RDF | Tiene un primer tutorial, necesita todavía comprobar conocimientos sin ayuda | Cypher y script en repositorio, ejecución remota no comprobada | Priorizar validación de los ejercicios y las respuestas esperadas |

### Orden recomendado a un alumno real

1. **Semana 01:** traducir preguntas de una biblioteca a nodos, relaciones y propiedades; explicar identidad.
2. **Semana 02:** comprender primero *qué es un camino* y después BFS, DFS y Dijkstra; consultar los temas por los libros de una autora.
3. **Semana 03:** comparar dos **representaciones** del mismo caso (propiedades y triples RDF). **No intentar aprender OWL ni SHACL en este punto**.
4. **Semana 04:** llevar la biblioteca a una base Neo4j real; crear, consultar y verificar.
5. **Semana 05:** profundizar en patrones Cypher, filtros y agregación.
6. **Semana 06:** aprender idempotencia, carga CSV, constraints y operaciones de escritura.
7. **Semana 07:** implementar un cliente Python, transacciones y un caso de uso reproducible.
8. **Evaluación del bloque:** resolver una prueba técnica independiente y corregir errores antes de estudiar motores alternativos.
9. **Ontologías, RDF avanzado y GraphDB:** partir de ese dominio conocido y ampliar su semántica.

### Qué falta antes de llamar al bloque «validado»

- Un entorno limpio que ejecute los scripts Python y las pruebas con versiones declaradas.
- Una instancia Neo4j de laboratorio para ejecutar todas las consultas de las semanas 04–07 y verificar resultados; no se presume acceso a credenciales del alumnado.
- Revisión de que **cada ejercicio** tiene datos de partida y una solución correcta bajo las condiciones indicadas.
- Tests de transferencia: cambiar una relación o identificador y razonar sobre la respuesta.
- Un pase de lectura por una persona sin conocimientos de grafos: registrar dudas reales en cada paso.
- Comprobar accesibilidad y navegación en móvil y escritorio.

**Criterio de cierre:** ninguna de las unidades se considera «100 % terminada» por tener varias páginas o referencias oficiales. Tiene que ser comprensible, ejecutable, transferible y verificable.

