# Laboratorio 03 — Neo4j AuraDB y Cypher de principio a fin

![Biblioteca ficticia](../assets/biblioteca-grafo.svg)

**Duración:** 2–3 horas. **Requisito:** instancia de Neo4j AuraDB de prueba y acceso al editor de Cypher. El curso no publica secretos ni necesita datos reales.

## 1. Preparar una instancia y los datos

Accede a [Neo4j Aura](https://console.neo4j.io/) y crea o utiliza una instancia adecuada a tus permisos. Guarda las credenciales **localmente**. En la consola de consultas, comprueba:

\`\`\`cypher
RETURN 'conectado' AS estado;
\`\`\`

**Resultado esperado:** una fila con \`estado = conectado\`.

Abre [\`ejemplos/neo4j/01_biblioteca.cypher\`](../ejemplos/neo4j/01_biblioteca.cypher) y ejecuta las sentencias en el editor. Se crean tres libros, dos autores, tres temas y un lector, además de las relaciones.

## 2. Comprueba el dataset

\`\`\`cypher
MATCH (l:Libro) RETURN count(l) AS libros;
\`\`\`

**Resultado esperado en base vacía antes de cargar:** 3.

\`\`\`cypher
MATCH (a:Autor) RETURN count(a) AS autores;
\`\`\`

**Resultado esperado:** 2.

\`\`\`cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
RETURN a.nombre AS autor, collect(l.titulo) AS libros
ORDER BY autor;
\`\`\`

**Resultado esperado:** Diego Ríos tiene «Historias del océano» y Marina Soler tiene «El mapa de los grafos» y «Rutas de conocimiento».

## 3. Repetir la carga

Ejecuta de nuevo el script; los recuentos deberían permanecer iguales porque se utilizan \`MERGE\` con claves estables y restricciones. Si no son iguales, investiga antes de seguir.

**Matiz:** \`MERGE\` no resuelve automáticamente duplicados con claves diferentes ni garantiza que las entradas sean semánticamente correctas.

## 4. Consultas para resolver

**Reto A.** ¿Qué libros tratan sobre «Grafos»?

\`\`\`cypher
MATCH (l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo:$codigo})
RETURN l.isbn AS isbn, l.titulo AS titulo
ORDER BY titulo;
\`\`\`

Ejecuta con el parámetro \`codigo = "GRAFOS"\`. Según el dataset, deben aparecer \`ISBN-001\` y \`ISBN-002\`.

**Reto B.** ¿Qué temas tiene cada autor?

\`\`\`cypher
MATCH (a:Autor)-[:ESCRIBIO]->(:Libro)-[:TRATA_SOBRE]->(t:Tema)
RETURN DISTINCT a.nombre AS autor, t.nombre AS tema
ORDER BY autor, tema;
\`\`\`

**Reto C.** ¿Qué libros no tienen autor?

\`\`\`cypher
MATCH (l:Libro)
WHERE NOT EXISTS { MATCH (:Autor)-[:ESCRIBIO]->(l) }
RETURN l.isbn AS isbn, l.titulo AS titulo;
\`\`\`

Con los datos iniciales, el resultado esperado es **cero filas**.

## 5. Driver oficial de Python

Usa el ejemplo [\`ejemplos/neo4j/app.py\`](../ejemplos/neo4j/app.py).

\`\`\`bash
python -m pip install -r ejemplos/neo4j/requirements.txt
# Copia .env.example a .env y rellena SOLO tus valores locales
python ejemplos/neo4j/app.py
\`\`\`

El código ejecuta una consulta **parametrizada** por tema. No concatenes entrada de usuarios al texto Cypher. Consulta el manual oficial para sesiones y transacciones.

## 6. Preguntas de diseño

1. ¿Por qué ISBN es mejor clave que título?
2. ¿Qué sucede si un autor cambia de nombre?
3. ¿Se deben permitir múltiples relaciones \`LEYO\` entre las mismas entidades?
4. ¿Cuándo necesitarías registrar una entidad intermedia \`Lectura\` con fecha?
5. ¿Qué podrías hacer con un CSV que llega parcialmente corrupto?

## 7. Evidencia de aprendizaje

Guarda un archivo con las consultas, los recuentos, las decisiones y los errores encontrados. No incluyas credenciales ni URI de acceso privado.

## Documentación oficial

- [Neo4j GraphAcademy: Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
