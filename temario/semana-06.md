# Semana 06 — Escritura, restricciones e importación de datos

## Objetivos

Crear y actualizar datos sin duplicarlos, entender `CREATE` frente a `MERGE`, importar CSV y comprobar el resultado.

## 1. CREATE y MERGE no significan lo mismo

`CREATE` crea un patrón nuevo. `MERGE` busca el patrón completo y lo crea si no existe. **No es una instrucción mágica de desduplicación**: necesitas una clave consistente y, preferentemente, una restricción de unicidad.

```cypher
MERGE (a:Autor {id: 'A-001'})
ON CREATE SET a.creado = datetime()
SET a.nombre = 'Marina Soler';
```

El valor `creado` se asigna solo al crear. La propiedad `nombre` se actualiza en cada ejecución.

## 2. Importación pequeña con UNWIND

```cypher
UNWIND [
  {isbn:'ISBN-101', titulo:'El mapa invisible', anio:2022},
  {isbn:'ISBN-102', titulo:'Ciudades de datos', anio:2024}
] AS fila
MERGE (l:Libro {isbn:fila.isbn})
SET l.titulo=fila.titulo, l.anio=fila.anio;
```

Repite la consulta y verifica:

```cypher
MATCH (l:Libro)
WHERE l.isbn IN ['ISBN-101','ISBN-102']
RETURN count(l) AS libros;
```

**Resultado esperado:** 2, no 4.

## 3. Importar CSV desde una URL accesible

Para `LOAD CSV`, Neo4j necesita poder acceder a la URL. Un archivo en tu ordenador no se vuelve accesible a Aura por estar en tu equipo.

```cypher
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/athurdavy/graph-academy-lab/main/ejemplos/neo4j/libros.csv' AS fila
WITH fila WHERE fila.isbn IS NOT NULL AND trim(fila.isbn) <> ''
MERGE (l:Libro {isbn:fila.isbn})
SET l.titulo = fila.titulo,
    l.anio = toInteger(fila.anio);
```

La URL anterior apunta al CSV ficticio publicado en este repositorio. Comprueba permisos de acceso y políticas de red de tu instancia.

## 4. Orden correcto de importación

1. Define claves y restricciones.
2. Importa entidades principales.
3. Resuelve referencias a nodos existentes.
4. Importa relaciones.
5. Valida recuentos, claves faltantes y relaciones huérfanas.

Para una relación:

```cypher
MATCH (a:Autor {id:'A-001'})
MATCH (l:Libro {isbn:'ISBN-101'})
MERGE (a)-[:ESCRIBIO]->(l);
```

**Importante:** si no existe el autor o el libro, `MATCH` no produce fila y la relación no se crea. Esto debe validarse, no ignorarse.

## 5. Calidad y rendimiento

- Las restricciones de unicidad protegen frente a duplicados por clave, pero no garantizan completitud ni calidad de nombres.
- Las cargas grandes requieren lotes y evaluación de memoria/transacciones.
- Usa `EXPLAIN` para inspeccionar el plan sin ejecutar y `PROFILE` para analizar una consulta ejecutada.
- No ejecutes operaciones destructivas en bases compartidas. Si pruebas `DETACH DELETE`, usa una instancia de laboratorio y filtros específicos.

## 6. Ejercicios y soluciones

**A.** Importa el CSV dos veces y verifica que no aparecen libros adicionales.

**B.** Añade una fila con `anio` vacío. Decide cómo gestionar `null` y registra tu política.

**C.** Intenta importar una relación hacia un ISBN inexistente. ¿Cómo detectarías el fallo?

Solución orientativa C:

```cypher
UNWIND ['ISBN-101', 'ISBN-INEXISTENTE'] AS isbn
OPTIONAL MATCH (l:Libro {isbn:isbn})
WITH isbn, l
WHERE l IS NULL
RETURN isbn AS referencia_sin_resolver;
```

## Entregable

CSV, script de importación, comprobaciones y un documento de decisiones sobre duplicados y valores faltantes.

## Referencias

- [Cypher: cláusulas](https://neo4j.com/docs/cypher-manual/current/clauses/)
- [Cypher: restricciones](https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/)
- [Cypher: LOAD CSV](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/)
