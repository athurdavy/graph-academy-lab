# Laboratorio 07 — DCMI Terms, RDF y exportaciones con Python

**Objetivo:** saber producir RDF interoperable, serializarlo, volverlo a importar y comprobar que no se pierde significado. **Datos:** libro y autor ficticios.

## Qué es DCMI Terms

Dublin Core Metadata Initiative publica un vocabulario de metadatos. La familia de términos dcterms permite describir títulos, creadores, fechas, identificadores, licencias y relaciones, entre otros elementos.

La IRI http://purl.org/dc/terms/title identifica la propiedad título. No es un campo específico de Neo4j ni una tabla SQL; es un término RDF que diferentes plataformas pueden reutilizar.

## Ejemplo Turtle

~~~turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix bibo: <http://purl.org/ontology/bibo/> .
ex:libro001 a bibo:Book ;
  dcterms:title "El mapa de los grafos"@es ;
  dcterms:identifier "ISBN-001" ;
  dcterms:creator ex:autor001 ;
  dcterms:issued "2025"^^<http://www.w3.org/2001/XMLSchema#gYear> .
~~~

**Importante:** BIBO es un vocabulario adicional de descripción bibliográfica; usarlo no lo convierte en parte de DCMI. Utiliza sus IRIs y términos con una justificación explícita.

## Python: RDFLib

Ejecuta:

~~~bash
python -m pip install -r laboratorios/requirements.txt
python laboratorios/metadatos_rdf.py
python -m pytest laboratorios/tests/test_metadatos_rdf.py -q
~~~

El programa exporta **Turtle, N-Triples y JSON-LD** en laboratorios/exportaciones/. Los tests reimportan cada formato y comparan los triples.

**Cuidado:** archivos RDF distintos pueden contener los mismos triples en diferente orden, o nodos anónimos diferentes. Este ejemplo solo usa recursos identificados por IRI y puede comparar conjuntos de triples directamente. Para RDF con blank nodes o datasets con grafos nombrados se requieren comparaciones adecuadas, no una comparación textual.

## Ejercicios

1. Añade dcterms:language para el libro, eligiendo una representación documentada.
2. Añade dcterms:license con una IRI ficticia y describe qué significaría en un conjunto real.
3. Añade dos títulos en idiomas diferentes. Comprueba que el test de conversión los conserva.
4. Explica qué información habría que añadir para exportar correctamente las propiedades de una relación Neo4j a RDF.

## Bibliografía oficial

- [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/)
- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/)
- [RDFLib](https://rdflib.readthedocs.io/)
