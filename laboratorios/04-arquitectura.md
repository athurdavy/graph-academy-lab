# Laboratorio 04 — Arquitectura Python sin acoplar la lógica a una BBDD

![Arquitectura de biblioteca](../assets/arquitectura-biblioteca.svg)

**Duración:** 60–90 minutos. **No requiere PostgreSQL ni Neo4j** para ejecutar los tests.

## El problema

En una aplicación real, si cada método de negocio está lleno de sentencias Cypher, cambiar el motor o probar las reglas se vuelve difícil. Separaremos un **caso de uso** de la **implementación de persistencia**, sin introducir capas innecesarias.

## 1. Modelo y contrato

El archivo [\`laboratorios/servicios.py\`](../laboratorios/servicios.py) define:

- \`Libro\`: objeto de dominio inmutable.
- \`LibroRepository\`: protocolo de acceso por ISBN.
- \`RepositorioMemoria\`: implementación de pruebas.
- \`ConsultarLibro\`: caso de uso que valida la entrada y solicita datos al repositorio.

## 2. Ejecutar tests

\`\`\`bash
python -m pytest laboratorios/tests/test_servicios.py -q
\`\`\`

**Resultado esperado:** tres tests pasan: consulta existente/inexistente, rechazo de identificador vacío y normalización de espacios.

## 3. Por qué es útil

Al probar \`ConsultarLibro\` con un repositorio en memoria, podemos verificar reglas de negocio **sin acceso de red**. Más adelante se añade un adaptador Neo4j que ejecute Cypher parametrizado, y eventualmente uno de PostgreSQL que utilice SQLAlchemy.

Esto no significa que los tests unitarios reemplacen a pruebas de integración. En una BBDD real habrá restricciones, transacciones, fallos de conectividad y diferencias de aislamiento.

## 4. Ejercicio: crear adaptador Neo4j

Implementa \`Neo4jLibroRepository\` con el driver oficial y consulta:

\`\`\`cypher
MATCH (l:Libro {isbn:$isbn})
RETURN l.isbn AS isbn, l.titulo AS titulo;
\`\`\`

Convierte el resultado a la clase \`Libro\` o devuelve \`None\` si no existe. No abras ni cierres un driver en cada consulta: usa el ciclo de vida apropiado de tu aplicación.

## 5. ¿SQLAlchemy, neomodel o driver?

- **SQLAlchemy ORM**: mapeo relacional, útil para PostgreSQL.
- **neomodel OGM**: mapeo objeto-grafo para Neo4j; abstracción distinta.
- **Driver Neo4j oficial**: permite Cypher explícito y control de transacciones.
- **RDFLib**: bibliotecas y triples RDF; no es un ORM SQL ni un motor OWL completo.

**Solución razonada:** para aprender grafos, empieza con el driver oficial. Si el dominio crece, evalúa un OGM por productividad y restricciones técnicas, no por moda.

## 6. Ejercicio de arquitectura híbrida

Supón que PostgreSQL gestiona los préstamos y Neo4j una proyección de relaciones entre libros y temas. ¿Qué ocurre si se confirma la transacción SQL y falla la actualización del grafo?

**Respuesta:** no existe atomicidad global por defecto. Necesitas un mecanismo de eventos/outbox, reintentos idempotentes y reconciliación; registra qué base es fuente de verdad.

## Fuentes

- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Neo4j Aura: múltiples bases de datos](https://neo4j.com/docs/aura/managing-instances/multiple-databases/)
