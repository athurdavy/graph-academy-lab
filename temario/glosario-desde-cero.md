# Glosario de iniciación — siglas, palabras y ejemplos

Este glosario acompaña las lecciones de Graph Academy Lab. Se lee de forma progresiva: **no memorices una lista sin ejemplos**. Abre la lección que acompaña cada término, ejecuta su código y explica el concepto con tus palabras.

## Grafos, recorridos y matemáticas

| Término | Significado sencillo | Ejemplo |
|---|---|---|
| Grafo | Conjunto de entidades y conexiones | Autor conectado con Libro |
| Nodo o vértice | Una entidad en el grafo | ISBN-001 |
| Arista | Una conexión entre dos nodos | A escribió B |
| Grafo dirigido | La conexión tiene dirección | Autor → Libro |
| Grafo ponderado | Las conexiones tienen un coste o peso numérico | Trayecto que cuesta 10 minutos |
| Camino | Sucesión de aristas que permite llegar de A a B | A → Libro → Tema |
| Salto | Una arista recorrida | A→B es un salto |
| Camino mínimo | Camino que optimiza un criterio, definido previamente | Menos saltos o menor coste |
| BFS | *Breadth-First Search*, búsqueda en anchura | Recorrer primero vecinos próximos |
| DFS | *Depth-First Search*, búsqueda en profundidad | Seguir una rama hasta el final |
| FIFO | *First In, First Out*, primero en entrar y salir | Cola de personas |
| LIFO | *Last In, First Out*, último en entrar, primero en salir | Pila de platos |
| Dijkstra | Apellido del creador de un algoritmo de caminos de coste mínimo con pesos no negativos | Elegir ruta con coste total 3 frente a 20 |
| Big O | Forma de describir cómo crece el esfuerzo computacional | O(V+E) para BFS con listas de adyacencia |
| V y E | *Vertices* y *Edges*: número de nodos y aristas | V=5, E=5 |

**Estúdialos con dibujos:** [Semana 02: BFS, DFS y Dijkstra](semana-02.md).

## Bases de datos y Neo4j

| Término | Qué significa |
|---|---|
| Neo4j | Motor de base de datos basado en grafos de propiedades |
| AuraDB | Servicio gestionado para utilizar Neo4j |
| Cypher | Lenguaje declarativo para consultar y modificar grafos de propiedades |
| MATCH | Buscar patrones existentes |
| CREATE | Crear nodos y relaciones |
| MERGE | Buscar un patrón o crearlo si no existe |
| SET | Asignar propiedades o etiquetas según la sintaxis |
| WHERE | Filtrar condiciones |
| RETURN | Seleccionar los datos que devuelve la consulta |
| WITH | Pasar y transformar variables entre fases de una consulta |
| OPTIONAL MATCH | Mantener filas anteriores aunque falte un patrón |
| DISTINCT | Evitar repeticiones en resultados, sin eliminar datos |
| Constraint | Restricción de integridad, como unicidad por identificador |
| Índice | Estructura que facilita ciertas búsquedas |
| Transacción | Grupo de operaciones que se confirma o revierte de forma conjunta en su ámbito |
| ACID | Atomicidad, consistencia, aislamiento y durabilidad: propiedades transaccionales |
| Driver | Cliente de conexión a una base desde un lenguaje como Python |
| ORM | *Object-Relational Mapper*: mapeo de objetos a un modelo relacional |
| OGM | *Object-Graph Mapper*: mapeo de objetos a un grafo |

**Practica:** [Semana 04](semana-04.md), [Semana 05](semana-05.md), [Semana 06](semana-06.md), [Semana 07](semana-07.md).

## RDF, ontologías y web semántica

| Término | Significado | Ejemplo |
|---|---|---|
| RDF | *Resource Description Framework*: modelo de afirmaciones en triples | Libro → tiene título → «El mapa» |
| Triple | Sujeto + predicado + objeto | libro001, título, «El mapa» |
| IRI | *Internationalized Resource Identifier*: identificador global | https://example.org/biblioteca/libro001 |
| Turtle | Formato textual para serializar datos RDF | Archivos `.ttl` |
| RDFS | *RDF Schema*: clases, subclases y propiedades básicas | LibroDigital subclase de Libro |
| SKOS | *Simple Knowledge Organization System*: conceptos de clasificación | Teoría de grafos tiene etiqueta Grafos |
| OWL | *Web Ontology Language*: axiomas para ontologías formales | Propiedades inversas |
| OWA | *Open World Assumption*: ausencia de información no implica falsedad | Libro sin autor declarado |
| SHACL | *Shapes Constraint Language*: validación de grafos RDF | Exigir al menos un título |
| SPARQL | Lenguaje estandarizado para consultar RDF | SELECT con patrones de triples |
| DCMI | *Dublin Core Metadata Initiative*: vocabulario de metadatos | `dcterms:title` |
| Dublin Core Terms | Propiedades RDF estándar para recursos | Título, creador, identificador |
| Protégé | Editor de ontologías OWL | Crear una clase Libro |
| GraphDB | Motor de repositorios RDF/SPARQL | Importar Turtle y consultar triples |
| RDFLib | Biblioteca Python para leer y escribir RDF | `Graph().parse(...)` |
| Inferencia | Consecuencia derivada de hechos y axiomas | LibroDigital implica Libro |
| Razonador | Programa que calcula o comprueba inferencias con una semántica | Clasificar individuos según axiomas |

**Ruta recomendada:** [Semana 11: ontologías desde cero](semana-11.md), [Semana 12: SKOS y SPARQL](semana-12.md), [Semana 13: OWL](semana-13.md), [Semana 14: SHACL](semana-14.md).

## Cómo utilizar el glosario

1. Cuando aparezca una palabra nueva, busca su definición aquí.
2. Abre la lección, revisa el dibujo y encuentra el ejemplo concreto.
3. Explica el término en una frase con tus propias palabras.
4. Cambia una parte del ejemplo y predice qué ocurrirá.
5. Ejecuta el código y compara resultado esperado y resultado obtenido.

**Recordatorio:** saber expandir una sigla no es saber utilizar esa tecnología. El objetivo final es resolver problemas y justificar decisiones técnicas.

## Referencias primarias

- [NetworkX](https://networkx.org/documentation/stable/)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [RDF 1.1 Primer — W3C](https://www.w3.org/TR/rdf11-primer/)
- [OWL 2 Primer — W3C](https://www.w3.org/TR/owl2-primer/)
- [SKOS — W3C](https://www.w3.org/TR/skos-reference/)
- [SHACL — W3C](https://www.w3.org/TR/shacl/)
