# Semana 24 — Proyecto final: demostrar autonomía en grafos y ontologías

**Antes:** las [semanas 01–23](../ruta.html). **Meta:** entregar una solución para una biblioteca ficticia que puedas construir, explicar, modificar y defender sin copiar un tutorial. Este proyecto sirve como evaluación **interna** de la academia, no equivale a una certificación oficial ni a un título universitario.

## 1. Qué significa «saber hacerlo» de verdad

Has aprendido conceptos de grafos, Cypher, RDF, RDFS, SKOS, OWL, SHACL, APIs y evaluación. Pero **recordar sus definiciones no demuestra autonomía**.

El proyecto final debe partir de un problema **nuevo**:

> Una biblioteca ficticia recibe un catálogo de libros, autorías y temas. Quiere consultar relaciones, publicar metadatos interoperables, validar su calidad y explicar de dónde salió cada afirmación.

No tienes que usar todas las tecnologías simultáneamente por obligación. Tienes que justificar **por qué utilizas cada herramienta**.

## 2. El encargo: requisitos que no debes confundir

### Preguntas funcionales

1. ¿Qué libros escribió cada autor?
2. ¿Qué libros tratan sobre un tema dado?
3. ¿Qué autores escribieron sobre un tema?
4. ¿Qué registros no tienen un título válido?
5. ¿Qué fuente respalda cada autoría?
6. ¿Hay registros cuyo identificador parece duplicado?
7. ¿Qué ocurre cuando una consulta no encuentra libros?
8. ¿Qué sabe el sistema y qué afirmaciones no puede verificar?

### Requisitos no funcionales

**Reproducibilidad:** otra persona puede instalar y ejecutar lo que entregas.

**Seguridad:** no compartes secretos; el acceso está controlado.

**Calidad:** detectas algunos datos inválidos y los distingues de datos simplemente desconocidos.

**Rendimiento:** mides antes de afirmar que una consulta es rápida.

**Trazabilidad:** una respuesta se puede relacionar con sus fuentes.

## 3. Entregables obligatorios

| Archivo o carpeta | Qué demuestra |
|---|---|
| `README.md` | Alguien puede instalarlo y saber qué ejecuta |
| `data/` | Dataset ficticio con entradas válidas y errores deliberados |
| `modelo.md` | Diseño de entidades, identidad, relaciones y reglas |
| `cypher/` | Carga idempotente, restricciones y consultas |
| `rdf/` | Exportación Turtle y vocabularios reutilizados |
| `shacl/` | Formas de validación y casos no conformes |
| `src/` | Aplicación Python y contrato de repositorio |
| `tests/` | Tests positivos, negativos y de integración cuando el motor esté disponible |
| `evidencias/` | Resultados de comandos, versiones y limitaciones |
| `defensa.md` | Decisiones técnicas justificadas y cosas que NO se garantizan |

No publiques contraseñas ni información privada. Todos los datos de la academia deben ser **ficticios**.

## 4. Fase 1: pasar de frases a un modelo

Empieza con cuatro entidades: Autor, Libro, Tema y Ficha. Dibuja las relaciones con flechas y define identificadores estables.

**No conviertas automáticamente todo sustantivo en nodo.** Un título puede ser propiedad de Libro. Una Ficha puede necesitar nodo propio si queremos adjuntarle procedencia y consultar su historia.

### Preguntas que debes documentar

- ¿Un Libro representa una obra abstracta, una edición o un ejemplar físico?
- ¿Cómo representas coautoría?
- ¿Qué diferencia hay entre un nombre y un identificador?
- ¿En qué circunstancias fusionarías dos autores?
- ¿Qué haces si una ficha afirma una autoría y otra la contradice?

**Resultado esperado de la fase:** diagrama, identificadores y explicaciones, **antes de abrir la base**.

## 5. Fase 2: crear Neo4j con integridad

Usa el [laboratorio de Neo4j](../laboratorios/03-neo4j.md) como referencia, pero crea una variante nueva del catálogo.

```cypher
CREATE CONSTRAINT libro_isbn IF NOT EXISTS
FOR (l:Libro) REQUIRE l.isbn IS UNIQUE;

MERGE (l:Libro {isbn:'ISBN-101'})
SET l.titulo='Atlas de conexiones';
```

Explica cada parte:

- La **constraint** protege la unicidad del ISBN cuando esté presente.
- `MERGE` busca o crea por clave.
- `SET` actualiza el título sin utilizarlo como criterio de identidad.

Prueba a repetir la carga y comprobar que el mismo ISBN no genera una entidad duplicada. Registra qué hiciste si existían duplicados antes de crear la constraint.

## 6. Fase 3: cinco consultas Cypher

Desarrolla consultas diferentes para:

1. Buscar libro por ISBN.
2. Listar libros por autora o autor.
3. Recuperar temas de los libros de una autora.
4. Detectar libros sin tema declarado.
5. Recuperar autorías con su fuente, según tu diseño de procedencia.

Para cada una escribe: **pregunta, patrón, consulta, resultado esperado, resultado observado y un caso negativo**.

Ejemplo:

```cypher
MATCH (a:Autor {id:$id})-[:ESCRIBIO]->(l:Libro)
RETURN l.isbn AS isbn, l.titulo AS titulo
ORDER BY isbn;
```

Si no se encuentra la autoría, la consulta puede devolver cero filas. **No significa automáticamente que la persona jamás escribió un libro**.

## 7. Fase 4: publicar RDF y metadatos

Reutiliza identificadores coherentes y propiedades estándares como `dcterms:title`. Declara las clases y propiedades que necesites, sin inventar semántica OWL innecesaria.

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix dcterms: <http://purl.org/dc/terms/> .

ex:libro101
  dcterms:title "Atlas de conexiones"@es ;
  dcterms:identifier "ISBN-101" .
```

La IRI `example.org` es solo de aprendizaje; para publicar datos reales debes diseñar una estrategia estable de identificadores.

**Verificación obligatoria:** parsea el Turtle con RDFLib, consulta los triples y compara sus valores con el catálogo de origen.

## 8. Fase 5: vocabulario y validación SHACL

Representa los **temas** con SKOS si necesitas etiquetas, variantes y jerarquía conceptual. No confundas `skos:broader` con `rdfs:subClassOf`.

Para los datos RDF, define reglas SHACL que exijan al menos un título e identificador por Libro.

Después introduce un error controlado —por ejemplo, un libro sin título— y comprueba que el validador produce **no conformidad**.

**No declares terminado un validador si solo lo has probado con datos correctos.**

## 9. Fase 6: API Python y fallos esperados

Construye una API pequeña con dos rutas: consulta por ISBN y consulta por tema. Separa el servicio del repositorio de datos.

Prueba estos casos:

| Caso | Respuesta esperada |
|---|---|
| ISBN conocido | Devuelve datos correctos |
| ISBN inexistente | Ausencia explícita, según contrato |
| Tema con cero libros | Lista vacía válida |
| Tema vacío | Error de validación |
| Motor de datos no disponible | Error operativo, no respuesta inventada |
| Solicitud sin permisos | No devuelve datos protegidos |

Un test con repositorio simulado no sustituye una prueba de integración con el motor real.

## 10. Fase 7: pruebas, métricas y defensa

**Tests unitarios:** validación de parámetros y lógica de servicio.

**Tests de integración:** carga, consultas, constraints, RDFLib y pySHACL contra entornos definidos.

**Pruebas negativas:** registros incompletos, identidades ambiguas, caídas de conexión y preguntas sin respuesta.

**Rendimiento:** registra versión, volumen, tiempos y condiciones; no afirmes que una tecnología «es más rápida» con una única medida.

**Defensa:** explica qué alternativas consideraste. Por ejemplo, ¿por qué Neo4j en lugar de una base relacional para tus consultas? ¿Por qué SKOS para temas en lugar de clases OWL? ¿Qué inferencias aporta o no OWL?

## 11. Evaluación interna sobre 100 puntos

| Competencia | Puntos | Evidencia que debe revisarse |
|---|---:|---|
| Modelo e identidad | 15 | Decisiones y casos ambiguos |
| Neo4j y consultas | 20 | Datos y consultas reproducibles |
| RDF, vocabularios | 15 | Turtle parseable y semántica justificada |
| SHACL y calidad | 15 | Un caso positivo y uno negativo |
| Python y API | 15 | Contratos y respuestas correctas |
| Pruebas y seguridad | 10 | Tests, secrets, fallos |
| Defensa técnica | 10 | Explicación y límites |
| **Total** | **100** | |

**Umbral pedagógico propuesto:** 80/100 como punto de referencia interno, más condiciones imprescindibles: nada de secretos, datos reproducibles, prueba negativa SHACL y explicación de al menos un límite importante.

**No equivale a una certificación real:** para ello necesitarías evaluación independiente y requisitos oficiales actualizados.

## 12. El reto de autonomía (sin soluciones copiables)

Recibe un **segundo dataset ficticio** que no hayas usado en los tutoriales. Puede incluir dos autores con el mismo nombre, un libro sin tema y dos fichas contradictorias. Sin modificar los requisitos para que encajen en tu código:

1. Explica qué información falta para resolver los conflictos.
2. Diseña identificadores y relaciones.
3. Importa sin duplicar.
4. Exporta RDF válido.
5. Valida SHACL y presenta un informe de errores.
6. Responde las preguntas de competencia.
7. Documenta qué conclusiones no puedes defender.

**Eso es demostrar aprendizaje**, no repetir un script memorizado.

## 13. Y después de este curso, ¿ya eres experto?

No por el hecho de completar esta entrega. Ser experto implica resolver distintos problemas reales, revisar errores, dominar limitaciones y mantener sistemas. Este ejercicio proporciona **evidencias de autonomía básica e intermedia**; no sustituye experiencia profesional ni certificaciones.

**Revisión de preparación:** [auditoría completa de las 24 semanas](../AUDITORIA_COMPLETA_24_SEMANAS.md).

## Referencias primarias

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [RDF Primer W3C](https://www.w3.org/TR/rdf11-primer/)
- [SKOS Primer](https://www.w3.org/TR/skos-primer/)
- [SHACL W3C](https://www.w3.org/TR/shacl/)
- [FastAPI](https://fastapi.tiangolo.com/)

**Estado:** rúbrica y diseño de proyecto detallados. El proyecto integrado real y su evaluación independiente aún no están completamente ejecutados; esta página define qué evidencias faltan, no las da por conseguidas.
