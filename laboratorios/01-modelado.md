# Laboratorio 01 — Grafo en Python, con resultados y tests

![Biblioteca ficticia](../assets/biblioteca-grafo.svg)

**Duración:** 60–90 minutos. **Dificultad:** inicial. **No requiere base de datos ni credenciales.**

## Qué vas a aprender

El propósito no es dibujar círculos: es entender cómo la **dirección** y el **tipo** de una relación cambian el resultado de una consulta.

En el catálogo ficticio:

- Marina **ESCRIBIO** El mapa de los grafos.
- El mapa de los grafos **TRATA_SOBRE** Grafos.
- Un lector **LEYO** El mapa de los grafos.

No son tres relaciones intercambiables.

## Preparación y ejecución

Desde la raíz del repositorio:

\`\`\`bash
python -m pip install -r laboratorios/requirements.txt
python laboratorios/biblioteca.py
\`\`\`

**Salida esperada:**

\`\`\`text
Nodos: 5, relaciones: 4
Libros de Marina: ['libro:ISBN-001', 'libro:ISBN-002']
Libros sobre grafos: ['libro:ISBN-001']
\`\`\`

Ejecuta los tests:

\`\`\`bash
python -m pytest laboratorios/tests/test_biblioteca.py -q
\`\`\`

## Leer el código

En [\`biblioteca.py\`](../laboratorios/biblioteca.py), \`nx.MultiDiGraph\` representa un multigrafo dirigido: puede guardar distintas aristas entre el mismo par de nodos. \`out_edges\` recupera relaciones **salientes**; \`in_edges\` recupera las **entrantes**.

El filtro \`datos["tipo"] == "ESCRIBIO"\` evita confundir las relaciones de autoría con cualquier otra conexión.

## Ejercicios

1. Añade «Diego Ríos» como autor de un libro nuevo. Ajusta los recuentos de tests.
2. Añade una relación \`RECOMENDO\` entre un lector y un libro; ¿debe aparecer en \`libros_de_autor\`? ¿Por qué?
3. Cambia la dirección de \`TRATA_SOBRE\` y observa qué consulta falla.
4. Implementa \`autores_de_tema(g, codigo)\`: recorre Tema ← Libro ← Autor.

## Pista de solución del ejercicio 4

Primero obtén libros con \`libros_sobre_tema\`. Para cada libro, examina \`in_edges\` y filtra por \`ESCRIBIO\`. Usa un conjunto para evitar duplicados.

**Resultado esperado con el dataset inicial:** \`['autor:A-001']\`.

## Preguntas de reflexión

¿Sería más sencillo consultar los datos con SQL? Para pocas relaciones fijas, posiblemente sí. El modelo de grafo puede ser más expresivo para recorridos complejos. No presupongas rendimiento superior sin medir.

## Documentación

- [NetworkX MultiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html)
- [Neo4j GraphAcademy: modelado](https://graphacademy.neo4j.com/courses/modeling-fundamentals/)
