# Semana 08 — ArcadeDB desde cero: entender un motor multimodelo

![La biblioteca ficticia del curso](../assets/biblioteca-grafo.svg)

**Antes:** [semana 07: Neo4j desde Python](semana-07.md). **Después:** [semana 09: ArcadeDB y Python](semana-09.md). Tiempo: 6–9 horas. **Objetivo:** comprender documentos, vértices, aristas y tipos en ArcadeDB, sin asumir que lo aprendido sobre Cypher funciona igual en cualquier motor.

## 1. El problema: ¿por qué estudiar otra base de datos?

Con Neo4j has representado «Marina escribió un libro» como dos nodos conectados por una relación. Pero hay otros motores que permiten acceder a datos como registros documentales y como vértices de un grafo.

**ArcadeDB** es un motor que documenta varias formas de acceso a sus registros, incluyendo el modelo de grafo. A esto lo llamamos **multimodelo**: varias formas de trabajar con la información. **No significa** que sea superior a Neo4j ni que cualquier función tenga exactamente el mismo comportamiento.

| Palabra | Explicación | Ejemplo |
|---|---|---|
| Documento | Registro que contiene campos y valores | Una ficha de libro |
| Vértice | Nodo de un grafo | Libro ISBN-001 |
| Arista | Conexión entre dos vértices | ESCRIBIO |
| Tipo de vértice | Categoría de registros de vértice | Libro, Autor |
| Tipo de arista | Categoría de conexiones | ESCRIBIO |
| SQL | *Structured Query Language*: lenguaje estructurado de consultas | Filtrar libros por ISBN |
| API | *Application Programming Interface*: interfaz para aplicaciones | Consultar desde Python |
| HTTP | *Hypertext Transfer Protocol*: protocolo de comunicación web | Solicitud del cliente a ArcadeDB |

## 2. La biblioteca antes del código

Tenemos dos entidades y una afirmación:

```text
Marina Soler (Autor)
        |
        | ESCRIBIO
        v
El mapa de los grafos (Libro)
```

Necesitamos distinguir **definir una categoría** de **crear un registro concreto**. Un tipo de vértice Libro es como decir «en esta base habrá libros». Crear el vértice de ISBN-001 es almacenar un libro específico. En SQL podrías comparar, con cautela, la primera operación con definir la estructura y la segunda con insertar datos.

## 3. Preparar un entorno de pruebas

1. Sigue la documentación oficial para instalar una versión concreta de ArcadeDB. Documenta esa versión.
2. Inicia una instancia local y crea una base de datos de laboratorio llamada `biblioteca`.
3. Accede a su consola de consultas de acuerdo con tu instalación.
4. Trabaja con datos ficticios, sin exponer puertos administrativos a Internet ni publicar credenciales.

**La versión y la edición importan:** las opciones de interfaz, protocolos y compatibilidad pueden variar. Este taller no presupone acceso a un servidor real desde el campus estático.

## 4. Aprende a leer el SQL de ArcadeDB carácter por carácter

```sql
CREATE VERTEX TYPE Libro;
```

**Traducción:** «Crea la definición de un tipo de vértice llamado Libro».

- `CREATE`: crear.
- `VERTEX`: vértice o nodo.
- `TYPE`: aquí define un **tipo**, no crea un libro.
- `Libro`: nombre elegido para esa categoría.
- `;`: final de la sentencia.

Ahora crea tipos de autor y de relación:

```sql
CREATE VERTEX TYPE Autor;
CREATE EDGE TYPE ESCRIBIO;
```

Una **edge** (arista en inglés) es una conexión. Estos comandos definen tipos; **todavía no existe Marina** en la base.

## 5. Crear registros con valores

```sql
CREATE VERTEX Autor SET id = 'A-001', nombre = 'Marina Soler';
CREATE VERTEX Libro SET isbn = 'ISBN-001', titulo = 'El mapa de los grafos';
```

La segunda instrucción se lee: «Crea un vértice del tipo Libro y asigna dos campos: ISBN y título».

- `SET` introduce las asignaciones.
- `isbn` es el **nombre del campo**.
- `=` asigna un valor.
- Las comillas simples rodean cadenas de texto.
- `ISBN-001` es un identificador ficticio, no un ISBN comercial comprobado.

**Esperado en una base nueva:** un vértice Libro y uno Autor. **Si repites estas sentencias puedes crear duplicados**; todavía no existen restricciones ni procedimientos idempotentes.

## 6. Crear una relación entre ellos

```sql
CREATE EDGE ESCRIBIO
FROM (SELECT FROM Autor WHERE id = 'A-001')
TO (SELECT FROM Libro WHERE isbn = 'ISBN-001');
```

Lee cada elemento:

1. `CREATE EDGE ESCRIBIO` solicita crear una conexión del tipo ESCRIBIO.
2. `FROM` indica el **origen**.
3. La primera consulta entre paréntesis busca a la autora.
4. `TO` indica el **destino**.
5. La segunda consulta entre paréntesis busca el libro.

**Requisito oculto que debes comprender:** cada búsqueda debe resolver el vértice adecuado. Si duplicaste autores con el mismo ID o no existe el libro, no debes presumir que la relación se ha creado correctamente.

## 7. Consultar los libros

```sql
SELECT FROM Libro;
SELECT FROM Libro WHERE isbn = 'ISBN-001';
```

La primera consulta recupera registros de tipo Libro; la segunda filtra por ISBN usando `WHERE` («cuando cumpla esta condición»).

En Neo4j una consulta equivalente se escribiría con Cypher:

```cypher
MATCH (l:Libro {isbn: 'ISBN-001'})
RETURN l.titulo;
```

Recuerda la sintaxis: `:Libro` introduce una etiqueta en el patrón de nodo Cypher, mientras que en ArcadeDB aquí se ha indicado el **tipo de registro** después de `FROM`. Que ambos modelos describan entidades y relaciones **no hace intercambiable su sintaxis**.

## 8. ¿Cómo comparar motores sin hacer publicidad?

No afirmes que ArcadeDB es más rápido solo porque soporte varios modelos. Para comparar necesitas:

- mismas entidades ficticias e identificadores;
- mismos tipos de consultas y resultados correctos;
- índices, planes y versiones documentados;
- condiciones operativas equivalentes, incluida la latencia de red;
- métricas de tiempos reproducibles y tamaños de resultados.

Estudiaremos la metodología en la [semana 10](semana-10.md). La mera existencia de una API o un dialecto Cypher tampoco garantiza equivalencia con Neo4j.

## 9. Ejercicios para aprender y no copiar

**Nivel 1 — Comprensión**

1. ¿Qué diferencia hay entre `CREATE VERTEX TYPE Libro` y `CREATE VERTEX Libro`?
2. ¿Qué significan `FROM` y `TO` al crear ESCRIBIO?
3. ¿Por qué el título no es una buena clave única universal?

**Nivel 2 — Experimentación**

4. Crea un segundo libro con otro identificador y consulta ambos.
5. Crea otra relación de autoría; comprueba que apunta al registro adecuado.
6. Ejecuta dos veces una creación en un entorno de prueba limpio, observa el problema y documenta qué regla de unicidad necesitas.

**Nivel 3 — Diseño**

7. Enumera los riesgos de migrar consultas Neo4j a otro dialecto Cypher sin probarlas.
8. Diseña una política para no duplicar los libros por ISBN.
9. Propón cuándo elegirías un motor multimodelo en lugar de usar dos motores separados.

## 10. Soluciones razonadas y autoevaluación

**1.** Definir un tipo de vértice crea una categoría de almacenamiento; crear un vértice crea una entidad concreta.

**2.** FROM indica origen y TO destino. Invertirlos cambia el sentido de la afirmación.

**3.** Un título puede repetirse en diferentes obras o ediciones; necesitas definir qué entidad representa el registro antes de elegir una clave.

**6.** La inserción con CREATE no garantiza idempotencia. Debes estudiar índices únicos, tratamiento de errores y operaciones seguras para la versión instalada.

**7.** Pueden cambiar funciones, restricciones, opciones del lenguaje, planes y semántica. Una prueba de portabilidad debe comprobar **resultados**, no solo que la consulta no dé error.

**Evaluación de salida:** crea los tipos, dos registros y una conexión de autoría, después consulta el libro por clave. Explica por qué cada sentencia es necesaria.

## Fuentes oficiales

- [ArcadeDB — documentación](https://docs.arcadedb.com/)
- [ArcadeDB — visión multimodelo](https://docs.arcadedb.com/arcadedb/concepts/multi-model)
- [ArcadeDB — referencia SQL](https://docs.arcadedb.com/arcadedb/reference/sql/)

**Estado:** diseño del laboratorio y explicación publicados. La ejecución integral en una versión de servidor ArcadeDB concreta todavía está pendiente, por lo que no se presenta como integración validada.
