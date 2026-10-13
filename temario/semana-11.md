# Semana 11 — Introducción rigurosa a las ontologías

**Caso ficticio:** catálogo de biblioteca. **Dedicación:** 10 h.

![Capas semánticas](../assets/capas-semanticas.svg)

## 1. Vocabulario, taxonomía, tesauro y ontología

Un **vocabulario controlado** fija denominaciones aceptadas. Una **taxonomía** organiza categorías. Un **tesauro** incorpora relaciones como términos preferidos, alternativos, jerárquicos y asociativos. Una **ontología formal** añade un modelo lógico de clases, propiedades, restricciones y axiomas.

No todo catálogo necesita OWL. Primero identifica las preguntas que necesitas responder y qué inferencias son realmente útiles.

## 2. Mundo abierto y ausencia de información

OWL utiliza habitualmente la **suposición de mundo abierto**: no conocer una afirmación no equivale a saber que es falsa. Esto es muy distinto de muchas validaciones de datos tradicionales.

Ejemplo: si no sabemos si un libro tiene autor, OWL no concluye automáticamente «el libro no tiene autor». Para verificar que un registro cumple requisitos de completitud se suele usar SHACL.

## 3. Clases e individuos

- `ex:Libro`: clase.
- `ex:LibroDigital`: subclase de Libro.
- `ex:libro001`: individuo.
- `ex:escritoPor`: propiedad de objeto que vincula recursos.
- `ex:titulo`: propiedad de datos con valor literal.

**Cuidado:** `rdfs:subClassOf` no significa «es un ejemplar de». El individuo se expresa con `rdf:type`.

## 4. Laboratorio Turtle

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:BibliotecaOntology a owl:Ontology .
ex:Libro a owl:Class .
ex:LibroDigital a owl:Class ; rdfs:subClassOf ex:Libro .
ex:Autor a owl:Class .
ex:escritoPor a owl:ObjectProperty ;
  rdfs:domain ex:Libro ; rdfs:range ex:Autor .
ex:titulo a owl:DatatypeProperty ;
  rdfs:domain ex:Libro ; rdfs:range xsd:string .
ex:libro001 a ex:LibroDigital ;
  ex:titulo "El mapa de los grafos" ;
  ex:escritoPor ex:autor001 .
ex:autor001 a ex:Autor .
```

**Inferencia esperable bajo semántica OWL/RDFS:** si `ex:libro001` es un `ex:LibroDigital` y `ex:LibroDigital rdfs:subClassOf ex:Libro`, entonces `ex:libro001` es un `ex:Libro`. Un almacén RDF sin razonador puede no materializar ni devolver esa inferencia automáticamente.

## 5. Errores típicos

- Confundir `rdfs:domain` y `rdfs:range` con comprobaciones de tipos: en RDFS/OWL producen inferencias.
- Creer que `owl:FunctionalProperty` significa «campo obligatorio».
- Usar `owl:sameAs` para dos etiquetas parecidas: declara identidad muy fuerte.
- Confundir SKOS `broader` con `rdfs:subClassOf`: expresan relaciones diferentes.

## 6. Ejercicios

1. Añade la clase `Revista`. ¿Debe ser subclase de `Libro`? Justifica tu respuesta.
2. Declara `Lector` y `lee` con dominio y rango.
3. Añade un libro sin título. ¿Puedes concluir con OWL que el dato es inválido?
4. Escribe una afirmación `rdf:type` y una `rdfs:subClassOf` y explica sus diferencias.
5. Describe dos casos donde un vocabulario SKOS es suficiente y OWL sería innecesario.

### Respuestas razonadas

**3:** no. La falta de un triple no implica necesariamente una violación OWL. Para imponer «todo libro debe tener un título» como requisito de calidad de datos usa SHACL.

**4:** `rdf:type` vincula un individuo con una clase; `rdfs:subClassOf` vincula clases y permite inferir pertenencia a una superclase.

## Fuentes normativas

- [OWL 2 Primer — W3C](https://www.w3.org/TR/owl2-primer/)
- [RDF 1.1 Primer — W3C](https://www.w3.org/TR/rdf11-primer/)
- [SKOS Reference — W3C](https://www.w3.org/TR/skos-reference/)
