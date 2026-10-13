# Semana 01 — Pensar en grafos: de una pregunta a un modelo

![Biblioteca ficticia: autor, libro, tema y lector](../assets/biblioteca-grafo.svg)

**Unidad 1 de 42 · Bloque: fundamentos.** Tiempo orientativo: 8–12 horas. **Antes de comenzar:** saber ejecutar Python y comprender qué es una tabla SQL. **Después:** [Semana 02 — recorridos](semana-02.md).

## 1. ¿Qué problema vamos a resolver?

Una biblioteca ficticia almacena libros, autores, temas y lectores. Queremos responder:

> ¿Qué libros ha escrito Marina Soler? ¿Cuáles tratan sobre grafos? ¿Qué lectores los han leído?

En SQL tendríamos entidades en tablas con claves primarias y relaciones mediante claves foráneas. En un grafo representamos esas entidades como **nodos** y sus vínculos como **aristas** con significado explícito.

La decisión **no** es «SQL es malo y los grafos son buenos». Un sistema relacional responde perfectamente a estas preguntas. La diferencia práctica aparece al trabajar con muchos recorridos y patrones conectados que evolucionan; deberás justificar el modelo con requisitos y medidas.

### Ejemplo tabular

| libro | autor | tema |
|---|---|---|
| El mapa de los grafos | Marina Soler | Grafos |
| Rutas de conocimiento | Marina Soler | Grafos |
| Historias del océano | Diego Ríos | Naturaleza |

Esta tabla presenta datos, pero si la autora escribe veinte libros, repetir su nombre en cada fila no es una buena forma de identificarla. Necesitamos identificadores estables y normalización, sea cual sea la tecnología.

## 2. Anatomía de un grafo

Un grafo dirigido es \(G=(V,E)\): `V` es el conjunto de vértices y `E` representa aristas ordenadas. La arista `(A,B)` no implica `(B,A)`.

En nuestra biblioteca:

- `Autor:A-001` es un **nodo** que representa a Marina.
- `Libro:ISBN-001` representa un libro.
- `(Autor:A-001)-[:ESCRIBIO]->(Libro:ISBN-001)` es una **relación dirigida y tipada**.
- `(Libro:ISBN-001)-[:TRATA_SOBRE]->(Tema:GRAFOS)` es otra relación, con un significado diferente.

¿Por qué las relaciones llevan nombre? Porque una línea entre Autor y Libro no nos dice si el autor escribió, tradujo, ilustró o recomendó el libro. Sin tipos, el grafo resulta ambiguo.

### Propiedades, etiquetas e identificadores

- **Etiqueta** `Libro`: agrupa nodos del mismo tipo de entidad en un grafo de propiedades.
- **Propiedad** `titulo`: atributo del libro.
- **Identificador** `ISBN-001`: clave ficticia para recuperar un ejemplar de datos de forma consistente.
- **Tipo de relación** `ESCRIBIO`: explica el vínculo.

El ISBN del laboratorio es inventado y no es un ISBN comercial válido. No utilices el título como única clave: pueden existir libros con el mismo título o ediciones diferentes.

## 3. Dirección y cardinalidad: dos decisiones distintas

`Autor -[:ESCRIBIO]-> Libro` apunta del autor al libro. Aunque puedas consultar esa arista en sentido contrario, su **significado** sigue siendo «autor escribió libro».

La *cardinalidad* contesta otra pregunta: ¿un libro puede tener varios autores? Sí, en nuestro modelo puede. No guardaremos un único `autor_id` obligatorio dentro de Libro como regla universal: permitiremos varias relaciones `ESCRIBIO`.

Otros ejemplos:

- Un `Libro` puede tener varios `Tema`.
- Un `Lector` puede haber leído varios `Libro`.
- Un mismo `Libro` puede ser leído por varios lectores.

No transformes estas afirmaciones en restricciones arbitrarias de unicidad. Son reglas de negocio que deben comprobarse con el caso real.

## 4. Grafo de propiedades frente a ontología

Hasta ahora hablamos de entidades del catálogo. **Todavía no hemos definido una ontología OWL**.

Si utilizamos `:Libro` como etiqueta Neo4j, eso no significa automáticamente que hayamos declarado una clase `owl:Class`. Tampoco garantiza inferencia, consistencia lógica o interoperabilidad RDF.

Distinguirás estas capas a lo largo del curso:

1. **Datos conectados:** autor, libro, tema y lectura.
2. **Vocabulario de temas:** «Grafos», «Ciencia», sus etiquetas y jerarquías (SKOS).
3. **Ontología:** clases, propiedades y axiomas con semántica formal (OWL).
4. **Validación:** condiciones explícitas que deben cumplir los datos RDF (SHACL).

Esta separación será esencial en la [semana 03](semana-03.md) y, más adelante, en el bloque de ontologías.

## 5. Laboratorio ejecutable con NetworkX

Instala las dependencias **desde la raíz del repositorio**:

~~~bash
python -m venv .venv
# Linux / macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r laboratorios/requirements.txt
python laboratorios/biblioteca.py
~~~

El programa usa `nx.MultiDiGraph`: un multigrafo dirigido que permite más de una relación entre los mismos nodos.

**Salida esperada:**

~~~text
Nodos: 5, relaciones: 4
Libros de Marina: ['libro:ISBN-001', 'libro:ISBN-002']
Libros sobre grafos: ['libro:ISBN-001']
~~~

¿Por qué solo 5 nodos si en una tabla hay tres libros? Porque este ejemplo **mínimo** contiene dos libros, un autor, un tema y un lector. Más adelante ampliarás el dataset; no confundas los diferentes ejemplos de laboratorio con una única base ya cargada.

### Entender una consulta sobre la estructura

La función `libros_de_autor(grafo, "A-001")` parte del autor y examina sus relaciones **salientes**. Filtra `tipo == "ESCRIBIO"`, porque podríamos tener otras relaciones salientes, por ejemplo «RECOMENDO».

La función `libros_sobre_tema(grafo,"GRAFOS")` parte del tema y examina las relaciones **entrantes** `TRATA_SOBRE`. La dirección de la relación importa incluso si empezamos la búsqueda por el destino.

## 6. Pruebas automáticas y propósito de cada una

~~~bash
python -m pytest laboratorios/tests/test_biblioteca.py -q
~~~

Los tests comprueban, entre otras cosas:

- Número conocido de nodos y relaciones.
- Qué libros recupera una consulta por autor.
- Qué se obtiene al consultar un identificador inexistente.
- Que `Autor → Libro` no equivale a `Libro → Autor`.
- Que las relaciones llevan un tipo.

**Por qué comprobar dirección:** una consulta mal orientada puede devolver un resultado vacío sin producir un error técnico. Ese es un bug semántico silencioso.

## 7. Ejercicios para resolver sin copiar

**A. Comprensión.** Explica por qué `ESCRIBIO` y `LEYO` no pueden fusionarse en una relación llamada `CONECTADO_CON` sin perder significado.

**B. Modelado.** Un libro puede estar coescrito. Añade `Autor:A-002` y una segunda relación hacia `Libro:ISBN-001`. Dibuja el resultado.

**C. Código.** Implementa `libros_leidos_por(grafo, lector_id)`, filtrando las aristas salientes `LEYO`. Comprueba que `L-001` ha leído `ISBN-001`.

**D. Diseño.** El lector puede leer el mismo libro en diferentes fechas. ¿Guardarías varias aristas, propiedades en la relación o una entidad `Lectura`? Argumenta cómo recuperarías el historial.

**E. Diagnóstico.** Invierte la dirección de `TRATA_SOBRE` sin cambiar la consulta. Explica por qué el resultado queda vacío.

## 8. Soluciones razonadas

**A.** Al usar `CONECTADO_CON` ya no puedes distinguir autoría de lectura sin información adicional. La consulta «libros escritos por Marina» podría devolver libros que solo leyó.

**C.** Solución de referencia:

~~~python
def libros_leidos_por(grafo, lector_id):
    origen = f"lector:{lector_id}"
    if origen not in grafo:
        return []
    return sorted({
        destino
        for _, destino, datos in grafo.out_edges(origen, data=True)
        if datos["tipo"] == "LEYO"
    })
~~~

**D.** Si necesitas fechas, valoraciones y múltiples lecturas, una entidad intermedia `Lectura` con identificador y metadatos puede facilitar auditoría. Una arista con propiedades sirve para casos más simples. No hay una decisión universal.

## 9. ¿Estás preparado para la semana 02?

Responde sin consultar: ¿qué diferencia hay entre etiqueta, propiedad y tipo de relación? ¿Qué significa la dirección? ¿Cómo evitas confundir identidades? Ejecuta los tests y guarda tu solución de los ejercicios B y C.

**Continúa:** [Semana 02 — caminos y recorridos](semana-02.md). **Practica:** [Laboratorio 01](../laboratorios/01-modelado.md).

## Documentación primaria

- [NetworkX MultiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html)
- [GraphAcademy: Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/)
- [RDF Primer — W3C](https://www.w3.org/TR/rdf11-primer/)
