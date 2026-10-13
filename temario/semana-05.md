# Semana 05 — Aprender Cypher de verdad: de una relación a consultas complejas

![Biblioteca ficticia: autora, libros, temas y lectores](../assets/biblioteca-grafo.svg)

**Bloque Neo4j · Clase 2 de 4.** Antes: [Semana 04 — Primer grafo](semana-04.md). Después: [Semana 06 — Importación y escrituras](semana-06.md). **Tiempo:** 8–12 horas con prácticas. **Suposición:** ya ejecutaste el fichero de biblioteca ficticia en un entorno limpio.

## 1. La pregunta antes que la sintaxis

Queremos responder: «¿qué libros sobre grafos escribió Marina?» En una tabla SQL, normalmente unirías autores, autoría, libros, clasificación y temas. En Cypher **describes el patrón de relaciones que debe existir**.

```cypher
MATCH (a:Autor {id:'A-001'})-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo:'GRAFOS'})
RETURN l.isbn AS isbn, l.titulo AS titulo;
```

**Léelo de izquierda a derecha:** encuentra a Marina por identificador; sigue una relación `ESCRIBIO` a un Libro; desde el libro sigue `TRATA_SOBRE` a un Tema con código Grafos; devuelve datos del libro.

**Resultado esperado del dataset:** dos títulos, *El mapa de los grafos* y *Rutas de conocimiento*.

Una consulta puede ser **válida sintácticamente y errónea conceptualmente**. Si inviertes una flecha o confundes `TRATA_SOBRE` con `LEYO`, quizá no obtendrás error: obtendrás resultados equivocados o vacíos.

## 2. MATCH, variables, etiquetas y dirección

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
RETURN a.nombre AS autora, l.titulo AS libro
ORDER BY autora, libro;
```

- `MATCH` intenta encontrar coincidencias del patrón.
- `a` y `l` son variables disponibles durante la consulta.
- `:Autor` y `:Libro` filtran por etiqueta.
- `-[:ESCRIBIO]->` exige una relación con ese tipo y dirección.
- `RETURN` devuelve solo las expresiones solicitadas.
- `AS` cambia el nombre de la columna, sin modificar los datos.

**Salida esperada:** Marina → dos libros; Diego → Historias del océano (ordenado alfabéticamente según las columnas).

### Consultar desde el destino

```cypher
MATCH (l:Libro {isbn:'ISBN-001'})<-[:ESCRIBIO]-(a:Autor)
RETURN a.nombre AS autora;
```

Aunque la consulta comienza por el Libro, la flecha sigue orientada de **Autor a Libro**. No hemos invertido la relación física. Una relación tipada suele representar una afirmación direccional, aunque Cypher permita patrones no dirigidos cuando no te importe el sentido.

## 3. WHERE: las condiciones de búsqueda

```cypher
MATCH (l:Libro)
WHERE l.anio >= 2020
RETURN l.isbn AS isbn, l.titulo AS titulo, l.anio AS anio
ORDER BY anio DESC, titulo;
```

**Resultado esperado en el dataset principal:** `ISBN-002` (2024) y `ISBN-001` (2022).

Pueden combinarse condiciones:

```cypher
MATCH (l:Libro)
WHERE l.anio >= 2020 AND l.titulo CONTAINS 'grafos'
RETURN l.titulo, l.anio;
```

En nuestro dataset debe recuperarse *El mapa de los grafos*. **Cuida mayúsculas, acentos y normalización:** las comparaciones de cadenas pueden depender de cómo escribes los valores y de la función empleada. El motor no conoce automáticamente la semántica de «equivalencia lingüística».

### Parámetros, en vez de concatenar texto

```cypher
MATCH (l:Libro)
WHERE l.anio >= $desde
RETURN l.titulo AS titulo
ORDER BY titulo;
```

`$desde` es un **parámetro**. Una aplicación Python puede ejecutarla proporcionando `desde=2020`. Así separa la consulta de los valores de entrada; evita construir texto Cypher a partir de valores arbitrarios del usuario.

## 4. Agregaciones: contar sin engañarte

Pregunta: «¿cuántos libros escribió cada autora o autor?»

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
RETURN a.nombre AS autor, count(l) AS libros
ORDER BY libros DESC, autor;
```

**Esperado:** Marina 2, Diego 1.

Las agregaciones operan sobre **filas del patrón**. Si el mismo Libro se encuentra varias veces por diferentes rutas, `count(l)` puede contar apariciones repetidas.

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema)
RETURN a.nombre AS autor, count(DISTINCT l) AS libros
ORDER BY autor;
```

`DISTINCT` dentro de `count` evita contar dos veces un Libro que aparece en varias filas por sus distintos temas. Aquí Marina tiene dos libros, aunque *Rutas de conocimiento* trata sobre Grafos y Ciencia.

**Error típico:** usar `DISTINCT` para esconder duplicados que realmente se almacenaron por equivocación. Distingue duplicación de filas de consulta y duplicación de entidades.

## 5. WITH: pasar de una fase a otra

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
WITH a, count(DISTINCT l) AS cantidad
WHERE cantidad >= 2
RETURN a.nombre AS autor, cantidad
ORDER BY autor;
```

Paso a paso:

1. Encuentra autorías.
2. Agrupa implícitamente por la variable `a` y calcula `cantidad`.
3. `WITH` pasa **solo** las variables indicadas a la siguiente fase.
4. `WHERE` elimina grupos con menos de dos libros.
5. `RETURN` muestra autor y cantidad.

**Resultado esperado:** Marina Soler, 2.

Prueba a añadir `l.titulo` después de `WITH`. Si la variable `l` no pasó al siguiente ámbito, Cypher no puede utilizarla. Esto es útil: aprende a distinguir el **alcance de variables** y el flujo de la consulta.

## 6. OPTIONAL MATCH: cuando una relación puede faltar

Pregunta: «muestra **todos** los libros, aunque alguno no tenga tema».

Con `MATCH` normal, el libro sin tema desaparece de los resultados. Con `OPTIONAL MATCH` conserva la fila y representa la falta de coincidencia con `null`.

```cypher
MATCH (l:Libro)
OPTIONAL MATCH (l)-[:TRATA_SOBRE]->(t:Tema)
RETURN l.titulo AS libro, collect(t.nombre) AS temas
ORDER BY libro;
```

Con el dataset principal todos los libros tienen algún tema. Para demostrar la diferencia, crea un libro temporal:

```cypher
MERGE (l:Libro {isbn:'ISBN-SIN-TEMA'})
SET l.titulo='Libro sin clasificación';
```

Repite la consulta y observa que también aparece. El hecho de que no tenga una clasificación **registrada** no significa que el libro no trate de ningún tema en la realidad.

### ¿Cómo obtener libros sin tema?

```cypher
MATCH (l:Libro)
WHERE NOT EXISTS {
  MATCH (l)-[:TRATA_SOBRE]->(:Tema)
}
RETURN l.isbn, l.titulo;
```

**Resultado esperado** si creaste solo el libro temporal sin tema: ese libro.

No es equivalente a buscar todos los registros con propiedad `tema = null` si has modelado los temas como **nodos relacionados**.

## 7. Filtrar por longitud de un camino

Consulta un recorrido de dos saltos:

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema)
WHERE t.codigo = 'GRAFOS'
RETURN DISTINCT a.nombre AS autora
ORDER BY autora;
```

**Esperado:** Marina Soler. La consulta no afirma que toda la obra de Marina trate sobre grafos; solo que existe al menos una ruta que cumple el patrón.

Un patrón de más saltos no es necesariamente mejor. Pregúntate qué relación del mundo real representa cada salto y hasta dónde tiene sentido recorrer.

## 8. Orden, paginación y rendimiento

```cypher
MATCH (l:Libro)
RETURN l.isbn AS isbn, l.titulo AS titulo
ORDER BY isbn
SKIP 0 LIMIT 2;
```

`ORDER BY` establece un orden; `SKIP` salta filas y `LIMIT` limita las mostradas. En una API de paginación el orden debe ser estable. Para grandes volúmenes, estudia las estrategias de paginación y el coste de desplazamientos altos antes de elegir `SKIP` sin medir.

**EXPLAIN** muestra el plan sin ejecutar la consulta; **PROFILE** la ejecuta y aporta métricas. No uses `PROFILE` en consultas de escritura sin entender sus efectos.

```cypher
EXPLAIN
MATCH (l:Libro {isbn:'ISBN-001'})
RETURN l.titulo;
```

Inspecciona el uso de índices o restricciones y la cardinalidad estimada. La semana de optimización tratará estos planes con más detalle.

## 9. Practica: doce preguntas que un profesional debería resolver

Sin mirar las soluciones, escribe:

1. Todos los libros ordenados por ISBN.
2. Todas las autoras con nombre e ID.
3. Libros desde 2020.
4. Libro con ISBN concreto.
5. Autores con sus títulos.
6. Recuento de libros por autor.
7. Recuento de libros **distintos** por tema.
8. Autoras con libros relacionados con Grafos.
9. Temas de Marina sin repetición.
10. Todos los libros, incluso sin tema.
11. Libros sin autoría registrada.
12. Libros leídos por `L-001`.

**Entrega:** archivo `consultas.cypher` con las 12 consultas, la salida esperada y una frase que justifique cada patrón.

## 10. Soluciones comentadas de los problemas más importantes

**Reto 7.** Se cuenta por tema, evitando duplicados del mismo libro:

```cypher
MATCH (t:Tema)<-[:TRATA_SOBRE]-(l:Libro)
RETURN t.codigo AS tema, count(DISTINCT l) AS libros
ORDER BY libros DESC, tema;
```

**Reto 9.** Necesitas los dos saltos:

```cypher
MATCH (a:Autor {id:'A-001'})-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema)
RETURN DISTINCT t.codigo AS codigo, t.nombre AS tema
ORDER BY codigo;
```

**Resultado esperado:** Grafos y Ciencia.

**Reto 11.** Expresa la ausencia de una relación dirigida de autoría:

```cypher
MATCH (l:Libro)
WHERE NOT EXISTS {
  MATCH (:Autor)-[:ESCRIBIO]->(l)
}
RETURN l.isbn AS isbn, l.titulo AS titulo;
```

No confundir «no existe autoría registrada» con «no existe autor real». Comprueba si las cargas de datos estuvieron completas antes de sacar conclusiones.

**Reto 12.** El lector es el origen de `LEYO`:

```cypher
MATCH (p:Lector {id:'L-001'})-[:LEYO]->(l:Libro)
RETURN l.isbn AS isbn, l.titulo AS titulo;
```

**Resultado esperado:** `ISBN-001`, El mapa de los grafos.

## 11. Preguntas de autoevaluación antes de avanzar

- ¿Qué diferencias ves entre `MATCH` y `OPTIONAL MATCH`?
- ¿Por qué `WITH` puede hacer que una variable ya no esté disponible?
- ¿Qué cambia entre `count(l)` y `count(DISTINCT l)`?
- ¿Qué asegura `ORDER BY` cuando paginamos?
- ¿Qué significa una consulta con 0 filas?
- ¿Qué efecto puede tener `PROFILE` en una escritura?

**Criterio de avance:** consigue escribir las doce consultas sin copiar y explicar por qué cada una devuelve esas filas. Si tienes fallos, cambia un dato del grafo y repite el análisis antes de seguir.

**Siguiente:** [Semana 06 — escritura, CSV, MERGE y transacciones](semana-06.md).

## Referencias oficiales

- [Cypher: cláusulas](https://neo4j.com/docs/cypher-manual/current/clauses/)
- [Cypher: MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/)
- [Cypher: OPTIONAL MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/)
- [Cypher: WITH](https://neo4j.com/docs/cypher-manual/current/clauses/with/)
- [Cypher: Query Tuning](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/query-tuning/)
- [GraphAcademy: Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/)

**Estado editorial:** explicación extensa con resultados esperados para el dataset ficticio. No se ha ejecutado contra una instancia Aura real en esta revisión; queda pendiente la validación de integración antes de considerarla una clase revisada integralmente.
