# Semana 15 — Validación, gobierno del dato y calidad

## Objetivo

Pasar de un grafo que «funciona» a uno cuya calidad pueda medirse y discutirse.

## 1. Dimensiones de calidad

- **Completitud:** registros con datos necesarios.
- **Unicidad:** claves duplicadas.
- **Consistencia:** relaciones y tipos que cumplen reglas.
- **Procedencia:** fuente de cada afirmación.
- **Actualidad:** frecuencia y fecha de verificación.
- **Validez semántica:** definiciones y relaciones justificadas.

Una consulta correcta sobre datos falsos produce una respuesta técnicamente correcta y conceptualmente incorrecta.

## 2. Comprobaciones Cypher

Buscar libros sin ISBN:

\`\`\`cypher
MATCH (l:Libro)
WHERE l.isbn IS NULL
RETURN l.titulo AS libro;
\`\`\`

Contar etiquetas duplicadas de ejemplo:

\`\`\`cypher
MATCH (l:Libro)
WITH l.titulo AS titulo, count(*) AS cantidad
WHERE cantidad > 1
RETURN titulo, cantidad;
\`\`\`

**Cuidado:** dos libros pueden compartir título sin ser el mismo libro. Esta consulta propone **candidatos a revisión**, no una corrección automática.

## 3. Validación en RDF

En el laboratorio de ontologías, SHACL exige un título y un ISBN de cada \`ex:Libro\`. Cambia un dato y ejecuta \`validar.py\`: comprueba que la validación detecta la desviación. Distingue reglas de negocio en la aplicación, restricciones nativas Neo4j y formas SHACL.

## 4. Flujo de revisión

Propuesta → verificación de fuente → revisión editorial → aprobación → publicación → seguimiento. Define quién puede aprobar y revertir decisiones.

## 5. Ejercicios

1. Diseña cinco reglas de calidad para la biblioteca.
2. Clasifica cada una como restricción Neo4j, test Python o shape SHACL.
3. Define qué ocurre si la carga falla a mitad.
4. Documenta quién corrige cada error y cómo queda trazado.

## Fuentes

- [SHACL](https://www.w3.org/TR/shacl/)
- [Neo4j Constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/)
