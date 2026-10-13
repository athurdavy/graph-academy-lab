# Semana 16 — Procedencia, identificadores y versionado

## Antes de utilizar PROV-O: ¿qué es la procedencia?

En el catálogo alguien ha afirmado «ISBN-001 trata sobre Grafos». **¿Quién lo decidió?** ¿Fue un bibliotecario, una importación CSV o una clasificación sugerida por un algoritmo?

La **procedencia** (en inglés, *provenance*) es el conjunto de datos que nos permite rastrear **de dónde salió una afirmación, cómo se produjo y quién intervino**.

No confundas procedencia con veracidad: «fue revisado por alguien» es información útil, pero por sí sola no demuestra que el dato sea correcto.

### Un ejemplo que un alumno puede seguir

```text
Libro ISBN-001 ── tiene clasificación ── Grafos
                           |
                           v
                     Revisión CL-001
                     realizada por Editor 07
                     en 2026-01-15
                     estado: aprobada
```

Una relación directa Libro→Tema permite consultar rápidamente una clasificación, pero si queremos registrar múltiples revisiones, autores, versiones y decisiones contradictorias, podemos representar una **entidad Clasificacion**.

### Comprender MERGE y el identificador de una revisión

```cypher
MERGE (c:Clasificacion {id:'CL-001'})
SET c.estado = 'aprobada',
    c.origen = 'revision_editorial';
```

- `Clasificacion` es una etiqueta de nodo, no un texto mágico.
- `id` es una clave ficticia de la revisión.
- `MERGE` busca o crea el patrón de esa revisión.
- `SET` actualiza sus propiedades.

**Advertencia de diseño:** una entidad de clasificación no debe reescribirse indiscriminadamente si necesitas conservar todo el historial. Una modificación de estado puede requerir un **evento adicional** o un registro de versiones.

### PROV-O sin confundir las palabras

**PROV-O** es una ontología W3C para representar procedencia. Sus conceptos esenciales incluyen:

| Término | Significado | Biblioteca ficticia |
|---|---|---|
| Entity | Cosa o información cuya procedencia describimos | Clasificación propuesta |
| Activity | Proceso o acción que generó o modificó información | Revisión editorial |
| Agent | Persona, sistema u organización responsable | Editor 07 |

No necesitas memorizar toda PROV-O todavía. Primero diseña qué quieres rastrear y por qué, luego decide si debes expresarlo con vocabulario RDF interoperable.


## 1. No basta con saber qué dice un grafo

También importa **quién** lo afirmó, **cuándo**, **a partir de qué fuente** y **en qué versión**. En un catálogo ficticio: «este libro trata sobre Grafos» puede provenir de una ficha editorial revisada o de una clasificación automática.

## 2. Identidad estable

Evita usar el título como clave: puede cambiar, traducirse o repetirse. Emplea un identificador controlado, como ISBN ficticio en el laboratorio. Distingue identificador de negocio, identificador técnico y URL del recurso.

## 3. Una forma de modelar procedencia

Cuando la relación necesita autor, fecha y revisión, una entidad intermedia puede resultar más explicativa:

```cypher
MERGE (l:Libro {isbn:'ISBN-001'})
MERGE (t:Tema {codigo:'GRAFOS'})
MERGE (c:Clasificacion {id:'CL-001'})
SET c.origen='revision_editorial',
    c.estado='aprobada',
    c.fecha=date('2026-01-15')
MERGE (c)-[:SOBRE_LIBRO]->(l)
MERGE (c)-[:ASIGNA_TEMA]->(t);
```

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

## Soluciones y verificación de la práctica

**Comprensión:** explica con una situación de la biblioteca la diferencia entre una afirmación guardada y un dato confiable. **Aplicación:** cambia un registro ficticio o un adaptador en memoria, predice el resultado y verifica lo observado. **Límite:** un test local correcto no verifica datos del mundo real ni las transacciones de otros motores.

**Criterio para avanzar:** debes poder justificar la decisión técnica y reproducir el ejemplo, no solo repetir los términos. Registra preguntas que no sepas contestar para reforzarlas antes del siguiente bloque.
