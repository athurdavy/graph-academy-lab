# Semana 16 — Procedencia, identificadores y versionado

## 1. No basta con saber qué dice un grafo

También importa **quién** lo afirmó, **cuándo**, **a partir de qué fuente** y **en qué versión**. En un catálogo ficticio: «este libro trata sobre Grafos» puede provenir de una ficha editorial revisada o de una clasificación automática.

## 2. Identidad estable

Evita usar el título como clave: puede cambiar, traducirse o repetirse. Emplea un identificador controlado, como ISBN ficticio en el laboratorio. Distingue identificador de negocio, identificador técnico y URL del recurso.

## 3. Una forma de modelar procedencia

Cuando la relación necesita autor, fecha y revisión, una entidad intermedia puede resultar más explicativa:

\`\`\`cypher
MERGE (l:Libro {isbn:'ISBN-001'})
MERGE (t:Tema {codigo:'GRAFOS'})
MERGE (c:Clasificacion {id:'CL-001'})
SET c.origen='revision_editorial',
    c.estado='aprobada',
    c.fecha=date('2026-01-15')
MERGE (c)-[:SOBRE_LIBRO]->(l)
MERGE (c)-[:ASIGNA_TEMA]->(t);
\`\`\`

**No confundas:** registrar la procedencia de la afirmación con afirmar que la clasificación es objetivamente correcta.

## 4. PROV-O como referencia

La ontología PROV-O de W3C proporciona conceptos reutilizables de **entidades, actividades y agentes** para describir procedencia. No es obligatorio adoptarla al completo si el caso no necesita interoperabilidad.

## 5. Ejercicios

1. Añade revisión y estado editorial a una clasificación ficticia.
2. Modela cómo conservarías clasificaciones históricas.
3. Explica por qué cambiar un título no debe cambiar el identificador.
4. Distingue un evento de creación de un evento de aprobación.

## Fuentes

- [PROV-O — W3C](https://www.w3.org/TR/prov-o/)
- [DCAT 3 — W3C](https://www.w3.org/TR/vocab-dcat-3/)
