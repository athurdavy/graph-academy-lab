# Semana 14 — SHACL: validaciones reproducibles de datos RDF

![OWL frente a SHACL](../assets/capas-semanticas.svg)

**Objetivo:** declarar condiciones de calidad que RDF y OWL, por sí solos, no imponen como validaciones de registros.

## 1. ¿Qué valida SHACL?

El grafo de **datos** contiene recursos y triples. El grafo de **formas** (shapes) indica requisitos. El validador produce un informe con conformidad y, si procede, violaciones.

Un requisito del catálogo: cada recurso de tipo `Libro` debe tener exactamente un título de tipo cadena.

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

## 2. Ejecutar la validación

Los ejemplos del repositorio incluyen:

- [Datos Turtle](../ejemplos/ontologias/biblioteca.ttl)
- [Reglas SHACL](../ejemplos/ontologias/shapes.ttl)
- [Script de comprobación](../ejemplos/ontologias/validar.py)

Instala dependencias:

```bash
python -m pip install "rdflib>=7,<8" "pyshacl>=0.30,<1"
python ejemplos/ontologias/validar.py
```

El script debe imprimir que el conjunto **cumple** las formas.

## 3. Prueba negativa

Elimina el triple `ex:titulo` de un libro en una copia del archivo. Vuelve a ejecutar: el resultado debe mostrar una violación por `sh:minCount`. Esto es mejor que memorizar una regla sin comprobarla.

## 4. Errores de interpretación

- `sh:targetClass ex:Libro` selecciona recursos de esa clase en el grafo que se valida. Si los tipos no están declarados y no hay inferencia configurada, algunos recursos no serán objetivos.
- SHACL no garantiza que cada dato sea verdadero; comprueba condiciones definidas.
- Una ontología OWL y una validación SHACL pueden coexistir, pero resuelven problemas diferentes.
- Un esquema rígido puede rechazar datos válidos para otros casos de uso: documenta el alcance de cada shape.

## 5. Ejercicios con soluciones orientativas

1. Exige ISBN como cadena y al menos un valor.
2. Haz que `sh:maxCount 1` detecte títulos duplicados en el mismo recurso.
3. Añade un libro sin `rdf:type ex:Libro` y observa qué ocurre. Justifica la diferencia.
4. Crea un test automatizado que falle cuando el validador devuelva `conforms=False`.

**Solución (1):**

```turtle
sh:property [
  sh:path ex:isbn ;
  sh:minCount 1 ;
  sh:datatype xsd:string
] ;
```

Esta forma se añade dentro del nodo `ex:LibroShape`.

## Fuentes normativas

- [SHACL — W3C](https://www.w3.org/TR/shacl/)
- [pySHACL — RDFLib](https://github.com/RDFLib/pySHACL)
