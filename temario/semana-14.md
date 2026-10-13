# Semana 14 — SHACL desde cero: aprende a validar datos RDF

![OWL explica inferencias; SHACL comprueba reglas de calidad](../assets/capas-semanticas.svg)

**Antes:** [semana 13 — ontologías OWL](semana-13.md). **Objetivo:** escribir formas SHACL, ejecutar un validador Python, interpretar errores y diferenciar reglas de calidad de inferencias lógicas. Duración estimada: 8–12 horas con práctica.

## 1. El problema: tener RDF no significa tener buenos datos

Nuestra biblioteca ficticia guarda dos libros. El primero tiene ISBN y título; el segundo solo tiene ISBN porque alguien olvidó introducir el título.

RDF permite representar **lo que sabemos**, sin exigir automáticamente que cada recurso tenga todos los campos de una ficha administrativa. OWL añade significado lógico, pero no funciona como «el esquema obligatorio de un formulario».

Nuestro requisito de calidad es diferente:

> «Todo recurso clasificado como Libro debe tener exactamente un título, y ese título debe ser una cadena de texto».

Eso es precisamente lo que queremos **validar**.

## 2. Qué significan las siglas SHACL

**SHACL** significa *Shapes Constraint Language*: lenguaje de restricciones de formas. Es una recomendación del W3C para expresar condiciones sobre grafos RDF.

Una **shape** o **forma** es un conjunto de comprobaciones. Puedes imaginarla como una lista formal de requisitos sobre qué datos esperamos encontrar. La analogía con un formulario es útil, pero SHACL también puede comprobar valores, tipos, relaciones y condiciones más complejas.

En este ejercicio hay dos archivos separados:

1. **Grafo de datos:** hechos RDF sobre libros.
2. **Grafo de formas:** condiciones SHACL que queremos comprobar.

El **validador** compara ambos y emite un informe.

## 3. Nuestro grafo de datos, leído sin prisas

```turtle
@prefix ex: <https://example.org/biblioteca/> .

ex:libro001 a ex:Libro ;
  ex:titulo "El mapa de los grafos" ;
  ex:isbn "ISBN-001" .

ex:libro002 a ex:Libro ;
  ex:titulo "Rutas de conocimiento" ;
  ex:isbn "ISBN-002" .
```

Cada libro tiene:

- un triple `rdf:type ex:Libro` (abreviado por `a`);
- un título;
- un identificador ficticio.

Esos tres triples no aparecen necesariamente en ese orden cuando el sistema los serializa. El **orden del archivo no forma parte del significado** del grafo RDF.

## 4. Nuestra primera forma: título obligatorio

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:LibroShape a sh:NodeShape ;
  sh:targetClass ex:Libro ;
  sh:property [
    sh:path ex:titulo ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string
  ] .
```

### Traduce el código a palabras normales

- `ex:LibroShape` es el nombre del conjunto de reglas.
- `a sh:NodeShape` declara que se trata de una forma aplicada a nodos.
- `sh:targetClass ex:Libro` selecciona los recursos identificados como libros según las reglas de selección y la configuración de inferencia.
- `sh:property` introduce condiciones sobre una propiedad.
- `sh:path ex:titulo` indica que revisaremos los valores de `ex:titulo`.
- `sh:minCount 1` exige **al menos un valor**.
- `sh:maxCount 1` permite **como máximo un valor**.
- `sh:datatype xsd:string` comprueba el tipo de dato de cada valor.

**Por tanto:** exactamente un título, y de tipo cadena.

No confundas `sh:datatype` con `sh:class`: el primero comprueba el tipo RDF de un **literal**; el segundo se refiere a la pertenencia a una clase, según su semántica SHACL.

## 5. Ejecutar SHACL en Python

Utilizaremos [pySHACL](https://github.com/RDFLib/pySHACL), una implementación de validación SHACL para Python apoyada en RDFLib.

Desde la raíz de una copia del repositorio:

```bash
python -m pip install -r laboratorios/requirements.txt
python ejemplos/ontologias/validar.py
```

El script lee estos archivos públicos:

- [biblioteca.ttl](../ejemplos/ontologias/biblioteca.ttl) — datos.
- [shapes.ttl](../ejemplos/ontologias/shapes.ttl) — reglas.
- [validar.py](../ejemplos/ontologias/validar.py) — programa que ejecuta la validación.

El núcleo del programa es:

```python
from rdflib import Graph
from pyshacl import validate

datos = Graph().parse(
    "ejemplos/ontologias/biblioteca.ttl", format="turtle"
)
formas = Graph().parse(
    "ejemplos/ontologias/shapes.ttl", format="turtle"
)

conforme, informe, texto = validate(
    data_graph=datos,
    shacl_graph=formas,
    inference="none",
)

print(texto)
print("Conforme:", conforme)
```

**Qué significa cada variable:**

- `datos` contiene los triples que estamos revisando.
- `formas` contiene las reglas de validación.
- `conforme` es un booleano que indica si el resultado cumple los requisitos evaluados.
- `informe` contiene el grafo RDF con el informe de validación.
- `texto` contiene una explicación legible del informe.
- `inference="none"` indica que no solicitamos la inferencia opcional del validador durante esta prueba.

**Resultado esperado:** `Conforme: True` con los archivos iniciales.

## 6. Comprobar un fallo de verdad

Vamos a provocar un error **sin modificar los archivos originales**. Carga los datos en memoria y elimina el título de `libro001`:

```python
from rdflib import Graph, Namespace
from pyshacl import validate

ex = Namespace("https://example.org/biblioteca/")
g = Graph().parse(
    "ejemplos/ontologias/biblioteca.ttl", format="turtle"
)
formas = Graph().parse(
    "ejemplos/ontologias/shapes.ttl", format="turtle"
)

for titulo in list(g.objects(ex.libro001, ex.titulo)):
    g.remove((ex.libro001, ex.titulo, titulo))

conforme, _, texto = validate(
    data_graph=g,
    shacl_graph=formas,
    inference="none",
)

print("Conforme:", conforme)
print(texto)
```

**Resultado esperado:** `Conforme: False`. El informe debe mostrar una violación por la ausencia del número mínimo de valores para el título.

**Este experimento enseña más que leer la definición:** el dato sigue siendo RDF válido, pero **incumple nuestra política SHACL**.

### Compruébalo automáticamente

```bash
python -m pytest laboratorios/tests/test_ontologias.py -q
```

Entre sus pruebas hay una que elimina un título en memoria y comprueba que la validación falla.

## 7. Más restricciones: número de valores y tipos

### Exactamente un título

La combinación de `sh:minCount 1` y `sh:maxCount 1` exige uno. Si añades dos títulos **diferentes** al mismo recurso, puede producirse una violación de máximo.

### Un ISBN como cadena

```turtle
sh:property [
  sh:path ex:isbn ;
  sh:minCount 1 ;
  sh:datatype xsd:string
] ;
```

Este fragmento debe incluirse dentro de tu `ex:LibroShape`. No es un documento completo por sí solo.

### ¿Por qué usar una IRI para el autor?

Si la propiedad `ex:escritoPor` apunta a una entidad Autor identificada por IRI, podríamos comprobar su pertenencia a una clase:

```turtle
sh:property [
  sh:path ex:escritoPor ;
  sh:class ex:Autor
] ;
```

**Atención:** que el rango en RDFS sea Autor no implica que cada dato incumplido se rechace automáticamente; el diseño de validaciones e inferencias es distinto.

## 8. Un error silencioso: ¿qué nodos estamos validando?

Recuerda `sh:targetClass ex:Libro`. Si un recurso no está reconocido como instancia de esa clase bajo la selección de objetivos aplicable, podría **no ser validado** por nuestra forma.

Supón que añadimos:

```turtle
ex:recursoDesconocido ex:titulo "Sin tipo" .
```

No hemos declarado `ex:recursoDesconocido a ex:Libro`. El validador no puede asumir sin más que ese recurso pertenece a la clase objetivo, salvo que existan declaraciones o inferencias que lo seleccionen.

**Lección profesional:** una prueba SHACL «conforme» solo garantiza cumplimiento **de las condiciones y de los objetivos que configuraste**. No demuestra que todos los recursos reales estén bien clasificados ni que los contenidos sean verdaderos.

## 9. Comparación que debes memorizar comprendiendo

| Pregunta | OWL | SHACL |
|---|---|---|
| ¿Qué es LibroDigital respecto a Libro? | Define subclase e inferencias | Puede usar clases como criterio de validación |
| ¿Qué inferencias son lógicas? | Modela axiomas | No sustituye un razonador OWL completo |
| ¿Existe un título obligatorio en un registro de datos? | Mundo abierto: no es simplemente NOT NULL | Puede comprobar `minCount` |
| ¿Qué ocurre cuando falta información? | No concluyas automáticamente falsedad | Puede producir una violación de una regla específica |
| ¿Cómo sé si el resultado es verdadero? | Ni OWL ni SHACL verifican automáticamente hechos del mundo | Igual: hace falta gobernanza y revisión de fuentes |

## 10. Ejercicios graduados con soluciones

**E1.** Elimina un título de un libro en memoria y ejecuta el validador. ¿Qué ocurre?

**E2.** Añade dos títulos distintos a un mismo Libro. ¿Qué regla detecta el problema?

**E3.** Añade un Libro sin ISBN. ¿Qué condición necesitas?

**E4.** Añade un nodo con título pero sin `rdf:type Libro`. ¿Se selecciona necesariamente como objetivo? ¿Qué implica?

**E5.** Diseña una política de calidad que distinga una **violación grave** de una **advertencia** y explica qué debería hacer tu sistema con cada una.

### Soluciones razonadas

**E1:** debe fallar `sh:minCount 1`, porque la propiedad requerida no aparece en el recurso objetivo.

**E2:** `sh:maxCount 1` detecta múltiples valores diferentes para el mismo camino.

**E3:** añade una forma de propiedad para ISBN con `sh:path ex:isbn` y `sh:minCount 1`; si quieres cadena, también `sh:datatype xsd:string`.

**E4:** no presupongas que el nodo es objetivo; verifica selección y el régimen de inferencia. Puede ser necesario mejorar el modelo o añadir otros objetivos de validación.

**E5:** la gravedad puede expresarse y gestionarse mediante la política de publicación. Una forma correcta no hace que una clasificación editorial sea verdadera: sigue siendo necesaria la gobernanza de los datos.

## 11. Autoevaluación antes de GraphDB y Protégé

Explica sin mirar: forma, grafo de datos, grafo de formas, objetivo, `sh:property`, `sh:path`, `sh:minCount`, `sh:maxCount`, `sh:datatype`, informe de validación, diferencia entre OWL y SHACL.

**Continúa:** [taller GraphDB](especializacion-graphdb.md) para trabajar con un motor RDF, o [taller Protégé](especializacion-protege-owl.md) para editar ontologías OWL.

## Fuentes normativas

- [SHACL — W3C](https://www.w3.org/TR/shacl/)
- [RDF 1.1 Primer — W3C](https://www.w3.org/TR/rdf11-primer/)
- [pySHACL — implementación](https://github.com/RDFLib/pySHACL/)
- [OWL 2 Primer — W3C](https://www.w3.org/TR/owl2-primer/)
