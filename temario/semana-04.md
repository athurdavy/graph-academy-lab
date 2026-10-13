# Semana 04 — Neo4j AuraDB desde cero: nodos, relaciones y Cypher

![Biblioteca ficticia: nodos y relaciones](../assets/biblioteca-grafo.svg)

**Itinerario:** fundamentos → esta clase → [semana 05: consultar Cypher](semana-05.md). **Tiempo:** 7–10 horas. **Entrada:** sabes algo de Python/SQL pero nunca has usado una base de grafos. **Objetivo final:** crear, consultar y verificar una biblioteca ficticia sin copiar las soluciones.

## 1. ¿Para qué sirve Neo4j?

La biblioteca almacena autores, libros, temas y lectores. En SQL usaríamos tablas y claves foráneas. En Neo4j usamos un **grafo de propiedades**: nodos con etiquetas y propiedades, unidos por relaciones **dirigidas y tipadas**.

| Concepto | Ejemplo | Explicación |
|---|---|---|
| Nodo | `(:Autor)` | Representa una entidad identificable |
| Etiqueta | `Autor` | Agrupa nodos de una categoría; no es automáticamente una clase OWL |
| Propiedad | `id:'A-001'` | Atributo para describir o identificar |
| Relación | `-[:ESCRIBIO]->` | Conexión con dirección y significado |
| Patrón | `(a:Autor)-[:ESCRIBIO]->(l:Libro)` | Estructura que buscamos en Cypher |

**No presupongas que grafos sustituyen siempre a SQL.** Si una consulta es más expresiva en Cypher, eso aún no prueba que rinda más rápido. Lo evaluaremos con criterios reales.

### Lee el diagrama antes del código

Marina Soler `ESCRIBIO` un libro. Ese libro `TRATA_SOBRE` Grafos. Un lector `LEYO` el libro. La flecha indica desde qué entidad parte la afirmación; `ESCRIBIO` no significa lo mismo que `LEYO`. Cada tipo de relación responde preguntas distintas.

## 1.1. Aprende a leer Cypher como una frase

**Cypher es el lenguaje de Neo4j.** Igual que en Python `print()` tiene un significado, Cypher tiene símbolos propios. No interpretes sus dos puntos como los de un texto Python o como un prefijo RDF.

Empezamos con una única línea que todavía **no se ejecuta**:

~~~cypher
(a:Autor {id: "A-001", nombre: "Marina Soler"})
~~~

- `(` y `)`: señalan que hablamos de un **nodo** dentro de un patrón.
- `a`: **variable temporal** para utilizar ese nodo más adelante en la consulta. No es su identificador.
- `:Autor`: **etiqueta**; clasifica al nodo como Autor.
- `{` y `}`: agrupan las **propiedades**, los datos de la entidad.
- `id` y `nombre`: son nombres de propiedades.
- `"A-001"` y `"Marina Soler"`: son los valores de esas propiedades.

En lenguaje natural significa: **«Un nodo de la categoría Autor, al que llamo a durante esta consulta, con id A-001 y nombre Marina Soler»**.

### ¿En qué se diferencian CREATE, MATCH y MERGE?

Estas instrucciones utilizan patrones similares, pero **hacen cosas diferentes**:

~~~cypher
CREATE (a:Autor {id: "A-001"})
~~~

Lee: **«crea un nodo nuevo»**. Si lo ejecutas dos veces, intentará crear dos nodos; una restricción de unicidad puede impedir la duplicación.

~~~cypher
MATCH (a:Autor {id: "A-001"})
RETURN a
~~~

Lee: **«busca un nodo Autor cuyo id sea A-001 y muéstralo»**. No crea ninguno.

~~~cypher
MERGE (a:Autor {id: "A-001"})
RETURN a
~~~

Lee: **«busca el patrón y créalo si no existe»**. No es una deduplicación mágica de personas: depende de las claves y restricciones que hayas modelado.

### ¿Por qué las relaciones usan corchetes?

~~~cypher
(a:Autor)-[:ESCRIBIO]->(l:Libro)
~~~

Léelo con calma, sin ejecutarlo todavía:

1. `(a:Autor)` representa un nodo Autor.
2. `-` es parte de la conexión.
3. `[` y `]` delimitan el **patrón de relación**.
4. `:ESCRIBIO` indica el **tipo de relación**. Los dos puntos aquí **no indican una etiqueta de nodo**, sino un tipo de relación.
5. `->` indica que la relación **apunta hacia el Libro**.
6. `(l:Libro)` representa el segundo nodo.

**Traducción:** «Un autor escribió un libro». Eso representa la **dirección y el significado** de la relación. El patrón no tiene efecto por sí mismo: `MATCH` busca esa estructura; `CREATE` intenta crearla; `MERGE` busca o crea según su semántica.

### Prueba de comprensión antes de abrir Neo4j

**Pregunta A.** ¿Qué significa `a`? Respuesta: una variable que identifica temporalmente un nodo en la consulta, no la clave permanente del autor.

**Pregunta B.** ¿Qué significa `:Autor`? Respuesta: la etiqueta de **nodo**.

**Pregunta C.** ¿Qué significa `:ESCRIBIO` dentro de los corchetes? Respuesta: el tipo de **relación**; un símbolo parecido puede tener funciones distintas según dónde se coloque.

**Pregunta D.** ¿Por qué no podemos invertir la flecha sin pensar? Respuesta: porque estaríamos buscando o expresando otra orientación de la afirmación.

**No continúes** hasta poder leer los tres ejemplos de este apartado como frases en castellano.

---

## 2. AuraDB, instancias y herramientas: qué es cada cosa

**Neo4j** es la base de datos; **Cypher** es su lenguaje; **AuraDB** es el servicio gestionado. Una **instancia** de AuraDB es el entorno del servicio; una **base de datos** contiene los datos. Los planes pueden diferir en el soporte de varias bases de datos por instancia.

**Prepara un laboratorio:**

1. Entra en [Neo4j Aura Console](https://console.neo4j.io/).
2. Crea una instancia de pruebas según las opciones de tu cuenta y espera a que esté disponible.
3. Guarda la contraseña y el URI de conexión **en privado**. No los subas a GitHub.
4. Abre la consola de consultas de la instancia y ejecuta:

```cypher
RETURN 1 AS comprobacion;
```

**Resultado esperado:** una tabla con una columna `comprobacion` y una única fila con valor `1`. Si no aparece, comprueba la instancia y el acceso antes de continuar.

**¿Qué aprendiste?** `RETURN` devuelve expresiones aunque aún no exista ningún nodo; `AS` da nombre a la columna.

## 3. El primer nodo: CREATE y MATCH

En una instancia de laboratorio **limpia**:

```cypher
CREATE (a:Autor {id:'A-DEMO', nombre:'Marina Soler'});
```

Línea por línea:
- `CREATE` crea un patrón nuevo.
- `a` es una variable que representa el nodo durante la consulta.
- `:Autor` es su etiqueta.
- `id` y `nombre` son propiedades.
- El identificador `A-DEMO` es inventado y se usa solo para estudiar.

Ahora recupera el nodo:

```cypher
MATCH (a:Autor {id:'A-DEMO'})
RETURN a.id AS id, a.nombre AS nombre;
```

**Resultado esperado:** una fila con `A-DEMO` y `Marina Soler`. `MATCH` **busca** patrones: no crea datos.

**Experimento:** repite `CREATE` y consulta de nuevo. Sin restricciones, podrías tener dos nodos con el mismo ID. Acabas de descubrir por qué el modelado necesita integridad y una estrategia idempotente.

## 4. Dos nodos y una relación: MERGE y SET

En un entorno limpio ejecuta:

```cypher
MERGE (a:Autor {id:'A-001'})
SET a.nombre = 'Marina Soler'
MERGE (l:Libro {isbn:'ISBN-001'})
SET l.titulo = 'El mapa de los grafos', l.anio = 2022
MERGE (a)-[:ESCRIBIO]->(l);
```

**Interpreta cada operación:**

1. `MERGE` intenta encontrar un Autor con ese ID y crearlo si no existe.
2. `SET` asigna o actualiza propiedades.
3. El segundo `MERGE` identifica el Libro por su ISBN ficticio.
4. El último `MERGE` localiza o crea la relación `ESCRIBIO` entre **esos nodos ya vinculados a variables**.

**Matiz importante:** `MERGE` no detecta que dos identificadores distintos representan a la misma persona. La unicidad y la normalización de identidades se diseñan por separado.

Pregunta: ¿qué autora escribió el libro?

```cypher
MATCH (a:Autor {id:'A-001'})-[:ESCRIBIO]->(l:Libro)
RETURN a.nombre AS autora, l.titulo AS libro;
```

**Resultado esperado:** Marina Soler — El mapa de los grafos.

### La dirección importa

Cambia `->` por `<-` en la relación anterior. **Esperas cero filas** porque el patrón ya no coincide con la dirección registrada. Después prueba:

```cypher
MATCH (l:Libro {isbn:'ISBN-001'})<-[:ESCRIBIO]-(a:Autor)
RETURN l.titulo, a.nombre;
```

Encontrarás de nuevo la autora. Buscar desde el libro **no cambia la dirección almacenada**.

## 5. ¿Por qué no basta con MERGE? Restricciones

En un entorno sin duplicados existentes:

```cypher
CREATE CONSTRAINT libro_isbn IF NOT EXISTS
FOR (l:Libro) REQUIRE l.isbn IS UNIQUE;

CREATE CONSTRAINT autor_id IF NOT EXISTS
FOR (a:Autor) REQUIRE a.id IS UNIQUE;
```

Una restricción `IS UNIQUE` impide que dos nodos con la etiqueta indicada compartan el mismo **valor presente** de la propiedad. **No** exige que todos los nodos tengan esa propiedad. Las restricciones de existencia y de clave de nodo tienen requisitos específicos por edición.

Si el experimento inicial generó dos `Autor` con el mismo ID, la restricción puede fallar. No es un problema del comando: los datos ya incumplen la regla. Usa una base limpia para repetir la actividad o investiga de forma controlada antes de limpiar.

**Diagnóstico de IDs duplicados (solo lectura):**

```cypher
MATCH (a:Autor)
WHERE a.id IS NOT NULL
WITH a.id AS id, count(*) AS total
WHERE total > 1
RETURN id, total;
```

No ejecutes comandos de borrado indiscriminados en una base compartida.

## 6. Cargar la biblioteca completa y comprobarla

Ahora carga el fichero público ficticio [01_biblioteca.cypher](../ejemplos/neo4j/01_biblioteca.cypher). Lee sus comandos antes de ejecutarlos. El dataset contiene tres libros, dos autores, tres temas y un lector, más sus relaciones. Trabaja preferiblemente en un entorno de pruebas limpio para que los recuentos sean predecibles.

Consulta los autores de los libros:

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
RETURN a.nombre AS autora, collect(l.titulo) AS libros
ORDER BY autora;
```

**Resultado esperado:** Marina tiene dos libros (*El mapa de los grafos*, *Rutas de conocimiento*), y Diego Ríos tiene *Historias del océano*. `collect` agrupa resultados relacionados en una lista.

Encuentra libros de Grafos:

```cypher
MATCH (l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo:'GRAFOS'})
RETURN l.isbn AS isbn, l.titulo AS titulo
ORDER BY isbn;
```

**Resultado esperado:** `ISBN-001` y `ISBN-002`.

Pregunta de dos saltos: ¿sobre qué temas escribe cada autor?

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema)
RETURN DISTINCT a.nombre AS autora, t.nombre AS tema
ORDER BY autora, tema;
```

`DISTINCT` evita repetir un par autora/tema si varios libros de la autora pertenecen al mismo tema. **No elimina datos duplicados almacenados**; únicamente elimina filas repetidas del resultado.

## 7. Errores que debes comprender

| Problema | Causa habitual | Comprobación |
|---|---|---|
| No aparecen filas | Flecha, etiqueta o tipo incorrectos | Dibuja el patrón |
| Se duplican autores | `CREATE` repetido o claves inconsistentes | Busca IDs duplicados |
| Falla una constraint | Ya existen duplicados | Consulta los valores repetidos |
| `MATCH` no crea relación | `MATCH` solo busca | Usa `MERGE` de forma controlada |
| Una consulta devuelve demasiado | Patrón sin restricciones ni filtros | Examina selectividad y resultados |
| Hay resultados inesperados | Se mezcló el experimento con la carga | Usa IDs separados y entorno limpio |

## 8. Ejercicios: primero intenta, después mira las soluciones

**Nivel 1 — Reproducción**

1. Crea un Autor nuevo `A-003` y un Libro nuevo `ISBN-004` con `MERGE`. Relaciónalos con `ESCRIBIO`.
2. Busca libros publicados desde 2020, ordenados por año.
3. Consulta qué lector ha leído `ISBN-001`.

**Nivel 2 — Adaptación**

4. Añade `Tema:HISTORIA` y conecta tu libro nuevo con `TRATA_SOBRE`.
5. Ejecuta dos veces la carga del nuevo libro y verifica que no duplicas su ID.
6. Recupera libros sin tema mediante una comprobación de ausencia de patrón.

**Nivel 3 — Diseño**

7. Un lector puede leer un libro varias veces. ¿Guardarías fechas en relaciones, múltiples relaciones o una entidad Lectura? Razona según el historial.
8. Dos autoras tienen el mismo nombre pero distinto ID. ¿Por qué no fusionarlas automáticamente?
9. Diseña una consulta de dos saltos y explica el significado de cada arista.

## 9. Soluciones razonadas

### Ejercicios 1 y 2

```cypher
MERGE (a:Autor {id:'A-003'})
SET a.nombre='Elena Vidal'
MERGE (l:Libro {isbn:'ISBN-004'})
SET l.titulo='Atlas de conexiones', l.anio=2025
MERGE (a)-[:ESCRIBIO]->(l);
```

El patrón usa claves estables. `SET` actualiza propiedades del mismo nodo.

```cypher
MATCH (l:Libro)
WHERE l.anio >= 2020
RETURN l.isbn, l.titulo, l.anio
ORDER BY l.anio DESC, l.titulo;
```

`WHERE` filtra **antes** de devolver las columnas. `ORDER BY` controla el orden visual del resultado.

### Ejercicios 3 y 6

```cypher
MATCH (p:Lector)-[:LEYO]->(l:Libro {isbn:'ISBN-001'})
RETURN p.id AS id, p.alias AS lector;
```

```cypher
MATCH (l:Libro)
WHERE NOT EXISTS {
  MATCH (l)-[:TRATA_SOBRE]->(:Tema)
}
RETURN l.isbn, l.titulo;
```

Una ausencia de relación describe el **estado almacenado**, no una verdad sobre el mundo real. La segunda consulta no demuestra que el libro carezca de tema fuera de la base.

## 10. Comprobación antes de pasar a Cypher avanzado

Responde sin mirar:

- ¿Qué diferencia hay entre `CREATE`, `MATCH` y `MERGE`?
- ¿Por qué importa la flecha de `ESCRIBIO`?
- ¿Para qué sirve `SET`?
- ¿Por qué `IS UNIQUE` no obliga a tener ISBN?
- ¿Qué hacen `collect` y `DISTINCT`?
- ¿Por qué no se deben mezclar ejemplos de prueba con datos de producción?

**Prueba final:** añade un autor, un libro y un tema nuevos, conecta ambos patrones, ejecuta una consulta de dos saltos y repite la carga sin duplicar IDs. Guarda el código, el resultado y una explicación.

**Siguiente:** [Semana 05 — MATCH, WHERE, WITH, OPTIONAL MATCH y agregación](semana-05.md).

## Documentación oficial

- [AuraDB: crear una instancia](https://neo4j.com/docs/aura/getting-started/create-instance/)
- [Cypher Manual: MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/)
- [Cypher Manual: MERGE](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
- [Cypher Manual: restricciones](https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/)
- [GraphAcademy: Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/)

**Estado editorial:** ejemplos descritos y fundamentados en documentación oficial, todavía no verificados en una instancia Aura real durante esta actualización. No se marca como práctica validada hasta ejecutar y comprobar los resultados.
