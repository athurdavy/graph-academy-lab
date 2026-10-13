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



## Auditoría transversal de las 24 semanas — octubre de 2026

**Pregunta de evaluación:** ¿puede una persona que sabe programar, pero no conoce grafos, estudiar esta unidad en orden, explicar cada símbolo y resolver un problema nuevo sin consultar la solución?

**Estado actual por tramo:**

| Semanas | Evaluación de contenido | Intervención realizada | Siguiente requisito |
|---|---|---|---|
| 01–03 | Base desarrollada, requiere observación con principiantes y verificación de ejemplos | Explicaciones paso a paso de nodos, identificadores, BFS/DFS, RDF y diferencias entre símbolos | Comprobar aprendizaje en casos nuevos |
| 04–07 | Tutoriales amplios de Neo4j, Cypher, CSV y Python; integración Aura pendiente | Explicaciones sintácticas, laboratorio, pruebas simuladas y evaluación práctica | Ejecutar cada sentencia en AuraDB y validar resultados |
| 08 | Era un esquema, ahora incluye instrucción por instrucción | Rediseñada como primera clase ArcadeDB con vocabulario, SQL y soluciones | Verificar sintaxis en versión instalada |
| 09–10 | Eran clases breves y con formato Markdown erróneo | Introducción a API/HTTP/JSON, reglas de error, benchmark y soluciones | Pruebas de integración ArcadeDB y benchmarks reproducibles |
| 11–14 | Clases extensas de semántica; necesitan pruebas educativas e integración de razonadores | RDF, SKOS, SPARQL, OWL, SHACL explicados con bibliografía y código | Probar razonadores, validación y casos negativos |
| 15–17 | Esquemas insuficientes | Añadidos ejemplos básicos de calidad, procedencia y arquitectura | Desarrollar tests de gobierno, historial y consistencia híbrida |
| 18–21 | **Borradores introductorios**, no enseñan desde cero GraphRAG ni NLP profesional | Estado pedagógico advertido de forma explícita | Construir curso completo con datos, métricas y soluciones |
| 22–24 | **Borradores introductorios**, no constituyen una evaluación experta | Estado pedagógico advertido | Implementar proyecto final ejecutable y rúbrica verificable |

### Defectos transversales detectados

1. **Terminología que presupone experiencia:** etiquetas Cypher, prefijos Turtle, patrones, drivers y APIs se introducían sin explicar qué símbolos significan. Acción: introducir primero frase, diagrama, lectura símbolo a símbolo y código.
2. **Cambio de modelo antes de dominar el anterior:** RDF aparecía antes de que el alumno manejara Neo4j. Acción: la semana 03 es únicamente una **comparación introductoria**; las ontologías formales comienzan después.
3. **Repetición de texto superficial en semanas avanzadas:** se presentaban objetivos genéricos sin soluciones. Acción: declarar estado de borrador y no confundir extensión con aprendizaje.
4. **Diferencias entre datasets no comunicadas:** el grafo NetworkX de la primera semana es deliberadamente pequeño; el dataset Neo4j posterior contiene más libros, autores, temas y relaciones. Las salidas esperadas deben asociarse siempre a uno de esos conjuntos.
5. **Ejecución no demostrada:** código en GitHub y explicación conceptual no son lo mismo que un test de integración. Nunca dar un resultado por comprobado contra un motor remoto si no se ha ejecutado.
6. **Presentación del código:** se detectaron fences escapados en algunas semanas. Acción: corrección en las unidades intervenidas, pendiente revisión automática de todos los documentos.

### Rúbrica de calidad previa a publicar una unidad como terminada

Puntúa cada ítem con **0 = ausente**, **1 = parcial**, **2 = comprobado**, por un máximo de **20 puntos**:

1. Prerrequisitos coherentes con el curso anterior.
2. Objetivos observables y motivación del caso de biblioteca.
3. Términos y siglas definidos antes de utilizarse.
4. Símbolos y sintaxis leídos paso a paso.
5. Modelo visual y explicación textual accesible.
6. Ejemplo completo reproducible desde entorno limpio.
7. Resultado esperado verificado, con versión/dataset y caso negativo.
8. Ejercicios de reproducción, adaptación y diseño.
9. Soluciones razonadas y errores habituales.
10. Evaluación de transferencia sin copiar, fuentes oficiales y limitaciones.

**Criterio interno:** no declarar una unidad completa con menos de **18/20**, ni siquiera si obtiene esa puntuación sin haber ejecutado el código cuando se exige integración.

### Orden editorial de continuación

**Prioridad A:** comprobar las semanas 01–07 con pruebas reales de salida, solucionar discrepancias, y mejorar las clases que un principiante no pueda explicar con palabras propias.

**Prioridad B:** integrar ArcadeDB 08–10, revisar fielmente sintaxis por versión y comprobar ejemplos.

**Prioridad C:** mejorar 15–17 como aplicaciones de calidad y arquitectura sobre el mismo catálogo.

**Prioridad D:** desarrollar 18–24 desde sus primeras definiciones y con ejercicios evaluables; sustituir expresamente los borradores actuales, **no** añadir párrafos genéricos.

**Conclusión:** la academia todavía **no** permite afirmar de forma sustentada que una persona pasará de cero a experta tras recorrer el contenido actual. La ruta señala el objetivo, pero el estándar de salida exige prácticas, comprobaciones y revisión pedagógica adicional.
