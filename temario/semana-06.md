# Semana 06 — Importar, escribir y proteger datos en Neo4j

![La biblioteca digital usada en todo el bloque Neo4j](../assets/biblioteca-grafo.svg)

**Bloque Neo4j · Clase 3/4 · Duración 8–12 h.** Vienes de [semana 05: consultas Cypher](semana-05.md). Terminarás pudiendo repetir una importación sin duplicar entidades, detectar datos incorrectos y comprender cuándo necesitas una transacción. Después pasarás a [semana 07: Python y Neo4j](semana-07.md).

## 1. El problema: cargar registros no es lo mismo que crear un grafo correcto

Una biblioteca recibe este CSV ficticio:

| isbn | titulo | anio |
|---|---|---:|
| ISBN-101 | El mapa invisible | 2022 |
| ISBN-102 | Ciudades de datos | 2024 |
| ISBN-103 | Rutas del océano | 2021 |

Quieres que un script se ejecute una vez, dos veces o después de un corte de conexión sin crear seis o nueve libros. Eso se llama **idempotencia**: repetir la operación produce el mismo estado lógico, aunque las métricas de ejecución puedan variar.

Para conseguirlo debes distinguir tres tareas:
1. **Identificar** la entidad mediante una clave estable.
2. **Crear o actualizar** sus datos.
3. **Comprobar** el resultado y registrar errores o referencias que no se pudieron resolver.

## 2. CREATE, MATCH, MERGE y SET: cuándo usar cada uno

```cypher
CREATE (:Libro {isbn:'ISBN-101', titulo:'El mapa invisible'});
```

`CREATE` siempre crea un nuevo nodo; si lo repites, aparece otro, salvo que una constraint impida ese duplicado.

```cypher
MATCH (l:Libro {isbn:'ISBN-101'})
RETURN l.titulo;
```

`MATCH` recupera nodos existentes; no crea nada. Para escribir datos idempotentes:

```cypher
MERGE (l:Libro {isbn:'ISBN-101'})
ON CREATE SET l.creado = datetime()
SET l.titulo='El mapa invisible', l.anio=2022;
```

- `MERGE` busca o crea un nodo que satisfaga el **patrón completo** especificado.
- `ON CREATE SET` se ejecuta solo cuando se crea ese patrón.
- `SET` actualiza propiedades tanto si existía como si se acaba de crear.

**Antipatrón:** `MERGE (l:Libro {isbn:'ISBN-101', titulo:'El mapa invisible'})`. Si cambia el título, un `MERGE` que use ambas propiedades puede intentar crear otro nodo; con una restricción única puede fallar. Identifica por clave estable y actualiza otros atributos con `SET`.

La documentación oficial advierte además que **MERGE no proporciona unicidad por sí solo bajo cargas concurrentes**. Usa restricciones sobre las claves de identificación. <https://neo4j.com/docs/cypher-manual/current/clauses/merge/>

## 3. Crear reglas de integridad ANTES de importar

En un entorno de prácticas limpio:

```cypher
CREATE CONSTRAINT libro_isbn IF NOT EXISTS
FOR (l:Libro) REQUIRE l.isbn IS UNIQUE;

CREATE CONSTRAINT autor_id IF NOT EXISTS
FOR (a:Autor) REQUIRE a.id IS UNIQUE;
```

Esta restricción evita dos nodos `Libro` con el mismo ISBN presente. **No exige que todos los Libros tengan ISBN**: eso es una condición de existencia distinta y su disponibilidad depende de la edición/plan.

Antes de añadir una constraint a una base con datos, comprueba duplicados:

```cypher
MATCH (l:Libro)
WHERE l.isbn IS NOT NULL
WITH l.isbn AS isbn, count(*) AS cantidad
WHERE cantidad > 1
RETURN isbn, cantidad;
```

Si la consulta devuelve filas, **investiga** primero: borrar duplicados automáticamente podría eliminar relaciones válidas.

## 4. Importación pequeña con UNWIND

`UNWIND` convierte cada elemento de una lista en una fila para las cláusulas siguientes. Para aprenderlo no necesitas cargar archivos ni depender de la red.

```cypher
UNWIND [
  {isbn:'ISBN-101', titulo:'El mapa invisible', anio:2022},
  {isbn:'ISBN-102', titulo:'Ciudades de datos', anio:2024},
  {isbn:'ISBN-103', titulo:'Rutas del océano', anio:2021}
] AS fila
MERGE (l:Libro {isbn:fila.isbn})
SET l.titulo=fila.titulo,
    l.anio=fila.anio;
```

**Paso a paso:** `UNWIND` produce tres filas; cada `fila` tiene claves `isbn`, `titulo` y `anio`; `MERGE` resuelve su Libro; `SET` actualiza sus propiedades.

Ejecuta el bloque dos veces y verifica:

```cypher
MATCH (l:Libro)
WHERE l.isbn IN ['ISBN-101','ISBN-102','ISBN-103']
RETURN count(l) AS libros_importados;
```

**Esperado en un entorno sin duplicados previos:** 3 en ambas ejecuciones. La consulta está filtrada para no contar los tres libros de las semanas anteriores.

## 5. LOAD CSV: del fichero a la base gestionada

Neo4j AuraDB ejecuta la importación desde el servidor. Eso significa que **no puede leer una ruta arbitraria de tu portátil**. El CSV de ejemplo está publicado en GitHub y accesible a través de una URL:

```cypher
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/athurdavy/graph-academy-lab/main/ejemplos/neo4j/libros.csv'
AS fila
WITH fila
WHERE fila.isbn IS NOT NULL AND trim(fila.isbn) <> ''
MERGE (l:Libro {isbn:fila.isbn})
SET l.titulo = fila.titulo,
    l.anio = CASE
      WHEN trim(coalesce(fila.anio,'')) = '' THEN null
      ELSE toInteger(fila.anio)
    END;
```

**Qué está ocurriendo:**

1. `LOAD CSV WITH HEADERS` interpreta la primera línea como nombres de columnas.
2. `fila.isbn` es texto extraído del CSV.
3. `WHERE` descarta filas sin identificador.
4. `MERGE` localiza o crea nodos por ISBN.
5. `toInteger` convierte el año de texto a número; en este ejemplo se trata de forma explícita la cadena vacía.

**No presumas que una conversión fallida, una cabecera inesperada o un año fuera de rango son datos válidos.** En producción define un contrato de datos, valida previamente y registra filas rechazadas. El ejemplo es introductorio; todavía no implementa una canalización robusta de errores.

### Por qué no conviene improvisar con información confidencial

Un CSV alojado en GitHub público **se vuelve público**. Este laboratorio solo utiliza datos inventados. Para datos privados necesitarías un mecanismo de transferencia autorizado, controles de acceso y trazabilidad.

## 6. Importar relaciones: primero nodos, después vínculos

Imagina que el autor `A-001` escribió `ISBN-101`. Solo puedes crear correctamente esa autoría si ambos nodos existen y se resuelven por clave.

```cypher
MATCH (a:Autor {id:'A-001'})
MATCH (l:Libro {isbn:'ISBN-101'})
MERGE (a)-[:ESCRIBIO]->(l);
```

**Importante:** si no existe `A-001`, el `MATCH` produce cero filas y **no se crea la relación**; la consulta puede finalizar sin error. No interpretes ausencia de error como prueba de importación completa.

Para revisar referencias faltantes:

```cypher
UNWIND ['ISBN-101','ISBN-DESCONOCIDO'] AS isbn
OPTIONAL MATCH (l:Libro {isbn:isbn})
WITH isbn,l
WHERE l IS NULL
RETURN isbn AS referencia_no_resuelta;
```

Esperado: `ISBN-DESCONOCIDO`. Esta comprobación valida referencias; no inventa nodos para tapar errores.

## 7. Transacciones: agrupar lo que debe ocurrir conjuntamente

Una **transacción** agrupa cambios que tienen que confirmarse o revertirse de forma conjunta. Neo4j ofrece transacciones ACID para operaciones en su propia base, pero **no** convierte automáticamente una operación simultánea en PostgreSQL y Neo4j en una única transacción distribuida.

En el driver Python practicarás transacciones gestionadas. Por ahora, comprende esta regla: *si crear una lectura requiere comprobar que existe lector, libro y una regla de negocio, no hagas llamadas independientes que puedan dejar un estado parcialmente actualizado*.

**Matiz:** la capacidad de reintentos del driver implica que cualquier callback de transacción debe ser seguro de repetir. No envíes correos ni hagas cobros dentro de la función reintentable.

## 8. ¿Cómo se diagnostica una carga lenta?

Antes de crear índices por intuición, compara patrones de consulta y volumen. En Cypher:

```cypher
EXPLAIN
MATCH (l:Libro {isbn:'ISBN-101'})
RETURN l.titulo;
```

`EXPLAIN` muestra el plan sin ejecutar el patrón de consulta; `PROFILE` sí ejecuta y mide. Una constraint de unicidad crea estructuras de índice aprovechables para sus búsquedas. Un índice para un campo que nunca filtras probablemente aporta menos valor que mejorar el modelo o la consulta.

## 9. Ejercicios por niveles

**Reproducción**

1. Carga la lista del apartado 4 dos veces y registra el recuento tras cada ejecución.
2. Cambia el título de `ISBN-102`, ejecuta `MERGE` por ISBN y comprueba si se crea otro nodo.
3. Importa el CSV público y compara las propiedades con la carga realizada con `UNWIND`.

**Adaptación**

4. Añade un libro con año vacío; define la política de aceptación/rechazo.
5. Añade una referencia a `ISBN-INEXISTENTE` y encuentra el fallo antes de crear una relación.
6. Haz que dos registros compartan ISBN y títulos distintos. ¿Qué debe hacer una política de calidad? ¿Actualizar, rechazar o enviar a revisión?

**Diseño**

7. Explica dónde pondrías las claves de negocio y por qué.
8. Diseña una carga de 100.000 registros, con lotes, revisión de fallos y verificación de recuentos.
9. Una aplicación actualiza PostgreSQL y después Neo4j, pero Neo4j falla. ¿Cómo registrarías el desfase y lo reconciliarías?

## 10. Soluciones razonadas

**Ejercicio 2:** usa `MERGE (l:Libro {isbn:'ISBN-102'}) SET l.titulo='Nuevo título'`. Al separar identificación y atributos, el cambio de nombre modifica la misma entidad.

**Ejercicio 5:**

```cypher
UNWIND ['ISBN-101','ISBN-INEXISTENTE'] AS isbn
OPTIONAL MATCH (l:Libro {isbn:isbn})
WITH isbn,l WHERE l IS NULL
RETURN isbn;
```

La única fila esperada es la referencia inexistente.

**Ejercicio 8:** no impongas una cifra de lote sin medir; documenta transacciones, reintentos idempotentes, métricas, registros rechazados y un plan de recuperación. Las cargas de producción no se resuelven únicamente aumentando `UNWIND`.

## 11. Comprobación antes de avanzar

- ¿Qué diferencia hay entre `CREATE` y `MERGE`?
- ¿Por qué una unicidad no obliga a que exista ISBN?
- ¿Por qué `LOAD CSV` no puede acceder a una ruta local arbitraria en AuraDB?
- ¿Qué hace `UNWIND`?
- ¿Cómo detectas referencias no resueltas y duplicados?
- ¿Por qué no debemos afirmar que PostgreSQL y Neo4j son atómicos conjuntamente?

**Entrega:** script de carga idempotente, consulta de recuento, detección de referencia inexistente, política de calidad documentada y resultados esperados.

**Siguiente:** [Semana 07 — Python Driver, sesiones y transacciones](semana-07.md).

## Documentación primaria

- [MERGE — Neo4j](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
- [LOAD CSV — Neo4j](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/)
- [Constraints — Neo4j](https://neo4j.com/docs/cypher-manual/current/schema/constraints/)
- [Query Tuning — Neo4j](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/query-tuning/)
- [Neo4j Python Driver: transactions](https://neo4j.com/docs/python-manual/current/transactions/)

**Validación:** ejemplos derivados del dataset público y de la documentación oficial. Queda pendiente la ejecución integral contra AuraDB para marcar esta unidad como verificada en infraestructura real.
