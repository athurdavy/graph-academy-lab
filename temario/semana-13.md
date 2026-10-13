# Semana 13 — OWL 2 desde cero: axiomas, razonamiento y sus límites

![RDF, OWL y SHACL: distintos objetivos](../assets/capas-semanticas.svg)

**Antes:** [semana 11: qué es una ontología](semana-11.md) y [semana 12: RDF, SKOS y consultas](semana-12.md). **Después:** [semana 14: validar datos con SHACL](semana-14.md).

**Objetivo:** comprender qué es un axioma, de dónde aparece una inferencia, por qué OWL no se comporta como una tabla con columnas obligatorias y cómo distinguir hechos declarados de conclusiones lógicas.

## 1. Una pregunta sencilla

En nuestro catálogo hay un libro que solo hemos clasificado como **LibroDigital**. También hemos afirmado que **todo LibroDigital es un Libro**.

¿Podemos concluir que el libro es un Libro? **Sí, lógicamente**.

No hemos añadido manualmente una nueva etiqueta al registro. La conclusión se deriva de dos afirmaciones:

1. LibroDigital es subclase de Libro.
2. libro001 pertenece a LibroDigital.

Por tanto: libro001 pertenece a Libro.

Esa operación de derivar conclusiones se llama **inferencia**.

## 2. Axioma, inferencia y razonador: tres palabras distintas

**Axioma**: afirmación formal que añadimos a la ontología. Por ejemplo, «LibroDigital es subclase de Libro».

**Inferencia**: conclusión que se sigue lógicamente de los axiomas y hechos. Por ejemplo, «libro001 es Libro».

**Razonador**: programa que aplica reglas de interpretación lógica para comprobar o derivar consecuencias bajo una semántica determinada.

Un razonador **no averigua datos que nadie conoce**. Si dices que dos clases son equivalentes, puede deducir pertenencias a partir de esa afirmación, pero no sabe si la equivalencia elegida describe correctamente el mundo real.

## 3. Qué significan las siglas OWL y RDFS

**OWL** es *Web Ontology Language*: lenguaje de ontologías de la web. **OWL 2** es una familia estandarizada por W3C que aporta expresividad para clases, propiedades y axiomas.

**RDFS**, *RDF Schema*, define vocabulario básico para clases, subclases, dominios y rangos. Es menos expresivo que muchas construcciones OWL.

En Turtle:

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Libro a owl:Class .
ex:LibroDigital a owl:Class ;
  rdfs:subClassOf ex:Libro .

ex:libro001 a ex:LibroDigital .
```

**Léelo paso a paso:**

- `a` es una abreviatura de Turtle para `rdf:type`.
- `owl:Class` indica que describimos clases OWL.
- `rdfs:subClassOf` expresa la relación lógica «subclase de».
- `ex:libro001 a ex:LibroDigital` clasifica al individuo como LibroDigital.
- La pertenencia a Libro es una **consecuencia semántica**, aunque ese triple no aparezca escrito físicamente.

## 4. Mundo abierto: por qué no funciona como un formulario

La **suposición de mundo abierto** (OWA, *Open World Assumption*) significa que la falta de una afirmación no la convierte automáticamente en falsa.

Supongamos que solo declaramos:

```turtle
ex:libro002 a ex:Libro .
```

**No hay** una propiedad de título. ¿Concluimos que el libro no tiene título? No: solo sabemos que no lo hemos declarado en el grafo.

En un sistema de formularios podrías exigir que el campo título sea obligatorio. Eso es un **requisito de calidad de datos**, distinto de la semántica general de OWL.

### Axiomas existenciales no son «NOT NULL»

Imagina que declaras en OWL que todo Libro está relacionado mediante `escritoPor` con **algún Autor**. En mundo abierto un razonador puede considerar que el autor existe pero su identidad no está descrita. No tiene por qué informar de un error de «autor obligatorio ausente».

Para ese tipo de comprobación operacional se utiliza a menudo SHACL, que estudiarás en la siguiente clase.

## 5. Propiedad de objeto y propiedad de datos

Una **propiedad de objeto** conecta recursos entre sí, por ejemplo un Libro con un Autor.

Una **propiedad de datos** relaciona un recurso con un literal, por ejemplo el título o el año.

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Libro a owl:Class .
ex:Autor a owl:Class .

ex:escritoPor a owl:ObjectProperty ;
  rdfs:domain ex:Libro ;
  rdfs:range ex:Autor .

ex:titulo a owl:DatatypeProperty ;
  rdfs:domain ex:Libro ;
  rdfs:range xsd:string .
```

`rdfs:domain` y `rdfs:range` no actúan automáticamente como una clave foránea SQL que rechaza registros. Bajo la semántica adecuada permiten inferir tipos. **Esa diferencia no es un detalle menor**: cambia por completo cómo diseñar y validar una ontología.

## 6. OWL añade propiedades inversas

Una propiedad inversa expresa dos formas de mirar una relación:

- libro001 `escritoPor` autor001.
- autor001 `escribio` libro001.

Puedes declarar ambas propiedades como inversas:

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ex:escritoPor a owl:ObjectProperty .
ex:escribio a owl:ObjectProperty ;
  owl:inverseOf ex:escritoPor .

ex:libro001 ex:escritoPor ex:autor001 .
```

Un razonador OWL que implemente correctamente esa característica puede derivar `ex:autor001 ex:escribio ex:libro001`. No es obligatorio almacenar también el triple inverso para que sea una consecuencia lógica.

## 7. Clases equivalentes y clases disjuntas

**Clases equivalentes:** declarar `owl:equivalentClass` significa que ambas clases contienen exactamente los mismos individuos en la interpretación lógica de OWL. **No** significa «sus nombres son parecidos».

**Clases disjuntas:** declarar `owl:disjointWith` significa que **ningún individuo puede pertenecer a ambas clases** en una interpretación consistente.

Si declaras `LibroFisico` y `LibroDigital` disjuntas, y después clasificas un libro en ambas, un razonador adecuado puede detectar **inconsistencia**.

**¿Es correcto declararlas disjuntas en nuestra biblioteca?** Depende. ¿El mismo recurso puede tener versión física y digital? ¿Un registro representa una obra abstracta o una edición? Antes del axioma debes resolver el problema de modelado.

## 8. Identidad: cuidado con owl:sameAs

`owl:sameAs` afirma identidad entre **individuos**. Si dos registros tienen un título parecido, **eso no demuestra que sean el mismo libro**.

Por ejemplo:

- «Historia de los grafos», primera edición.
- «Historia de los grafos», segunda edición.

Puede haber dos recursos diferentes. Usar `owl:sameAs` sin evidencia y sin definir qué identidad se representa puede propagar inferencias equivocadas por todo el sistema.

## 9. ¿Cómo lo practico sin instalar una infraestructura compleja?

Primero comprueba los triples **explícitos** con RDFLib:

```python
from rdflib import Graph, Namespace, RDF, RDFS

ex = Namespace("https://example.org/biblioteca/")
g = Graph()
g.add((ex.LibroDigital, RDFS.subClassOf, ex.Libro))
g.add((ex.libro001, RDF.type, ex.LibroDigital))

print("Triples explícitos:", len(g))
print("Triple explícito rdf:type Libro:",
      (ex.libro001, RDF.type, ex.Libro) in g)
```

**Resultado esperado:**

```text
Triples explícitos: 2
Triple explícito rdf:type Libro: False
```

Esto **no refuta** la inferencia. Demuestra que **RDFLib, en este código y sin razonador, no materializa la conclusión**.

### Ejercicio adicional: Protégé

**Protégé** es un editor de ontologías desarrollado en Stanford. Te permite crear y examinar clases, propiedades y axiomas OWL. No es equivalente a Neo4j ni a GraphDB.

En la [guía de Protégé](especializacion-protege-owl.md):

1. Abre una ontología con Libro y LibroDigital.
2. Declara la relación de subclase.
3. Crea un individuo libro001 de LibroDigital.
4. Activa un razonador compatible en la versión instalada.
5. Comprueba la clasificación inferida de libro001.
6. Documenta qué razonador, versión y opciones utilizaste.

**No atribuyas a un razonador consecuencias que no has comprobado.**

## 10. Perfiles de OWL: por qué hay varios

OWL 2 define perfiles como **EL, QL y RL**. Son subconjuntos con restricciones y propiedades computacionales pensadas para distintos contextos de razonamiento. No necesitas memorizarlos sin contexto:

- **EL:** útil en ontologías grandes con estructuras conceptuales y determinados tipos de axiomas.
- **QL:** orientado a escenarios donde resulta relevante responder consultas sobre grandes conjuntos de datos.
- **RL:** orientado a formas de razonamiento implementables mediante técnicas de reglas.

El soporte exacto depende de las herramientas. No asumas que elegir un perfil convierte automáticamente cualquier triple store en un razonador OWL 2 DL completo.

## 11. Ejercicios, de sencillos a profesionales

1. Identifica clase, individuo y propiedad en el ejemplo de libro001.
2. Explica la inferencia derivada de `LibroDigital rdfs:subClassOf Libro`.
3. Un libro no tiene autor declarado. ¿Qué sabes y qué no sabes?
4. Declara una propiedad inversa de `escritoPor`.
5. Diseña dos clases que **realmente deban ser disjuntas**. Justifica por qué.
6. Propón una situación donde `owl:sameAs` sería incorrecto.
7. Compara una inconsistencia OWL y una violación SHACL.
8. Documenta qué conclusiones necesitarías comprobar al intercambiar la ontología entre Protégé y GraphDB.

### Soluciones razonadas

**2:** si libro001 pertenece a LibroDigital y toda instancia de LibroDigital pertenece a Libro, la pertenencia a Libro es una consecuencia lógica.

**3:** solo sabemos que nuestro grafo no declara el autor. Bajo mundo abierto no podemos concluir que no existe autor.

**5:** antes de declarar disjunción, define exactamente qué representan ambas clases. Un modelo «obra» vs «edición» puede cambiar la respuesta.

**6:** dos libros con idéntico título o dos personas con el mismo nombre no son necesariamente el mismo individuo.

**7:** OWL detecta contradicciones bajo sus axiomas; SHACL compara un grafo de datos con condiciones explícitas de validación. Los dos procesos no son intercambiables.

## 12. Comprobación antes de SHACL

Debes poder explicar: axioma, inferencia, razonador, mundo abierto, subclase, propiedad inversa, disjunción y por qué una propiedad «obligatoria» de negocio no se obtiene automáticamente mediante OWL.

**Siguiente:** [Semana 14 — SHACL y validación reproducible](semana-14.md).

## Fuentes oficiales

- [OWL 2 Primer — W3C](https://www.w3.org/TR/owl2-primer/)
- [OWL 2 Profiles — W3C](https://www.w3.org/TR/owl2-profiles/)
- [OWL 2 Syntax — W3C](https://www.w3.org/TR/owl2-syntax/)
- [Protégé — Stanford](https://protege.stanford.edu/)
