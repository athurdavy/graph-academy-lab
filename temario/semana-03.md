# Semana 03 — Grafos de propiedades y RDF

## Dos formas de representar relaciones

En un **grafo de propiedades**, nodos y relaciones pueden llevar propiedades. En **RDF**, la unidad de información es un triple sujeto–predicado–objeto. No son formatos intercambiables sin decisiones de modelado.

### Ejemplo de grafo de propiedades en Cypher

```cypher
MERGE (c:Concepto {id: 'cliente'})
SET c.nombre = 'Cliente'
MERGE (t:Termino {id: 'customer'})
SET t.nombre = 'Customer'
MERGE (t)-[:DENOMINA]->(c)
```

### Ejemplo RDF con SKOS en Turtle

```turtle
@prefix ex: <https://example.org/conceptos/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .

ex:cliente a skos:Concept ;
    skos:prefLabel "Cliente"@es ;
    skos:altLabel "Customer"@en ;
    skos:definition "Entidad que adquiere bienes o servicios."@es .
```

**Matiz importante:** `skos:altLabel` no es el mecanismo para traducir etiquetas preferidas entre idiomas; SKOS permite `skos:prefLabel` por idioma. El ejemplo usa un término alternativo inglés solo a modo ilustrativo.

## Preguntas de diseño

- ¿Necesitamos interoperabilidad RDF con terceros?
- ¿Qué significa una relación `broader` y qué no significa?
- ¿Quién aprueba definiciones y sinónimos?
- ¿Qué identificadores sobreviven a un cambio de etiqueta?

## Práctica

Representa cinco conceptos del negocio en ambos modelos. Documenta qué información se conserva, qué decisiones tomaste y qué consultas serían necesarias.

## Fuentes

- [RDF 1.1 Primer — W3C](https://www.w3.org/TR/rdf11-primer/)
- [SKOS Reference — W3C](https://www.w3.org/TR/skos-reference/)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
