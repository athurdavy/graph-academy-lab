# Laboratorio 02 — RDF, clases OWL y validación SHACL

![Capas RDF SKOS OWL SHACL](../assets/capas-semanticas.svg)

**Duración:** 90 minutos. **No requiere servicio externo.** Se ejecuta con RDFLib y pySHACL.

## Pregunta que vas a responder

¿Por qué declarar \`Libro\` como clase OWL **no** basta para comprobar que todos los libros tengan título? Porque **inferencia** y **validación** son conceptos distintos.

## Preparación

\`\`\`bash
python -m pip install -r laboratorios/requirements.txt
python ejemplos/ontologias/validar.py
\`\`\`

**Salida esperada:** informe de validación conforme y mensaje «Validación completada: datos conformes».

Archivos del caso:

- [\`biblioteca.ttl\`](../ejemplos/ontologias/biblioteca.ttl) — datos RDF y clases.
- [\`shapes.ttl\`](../ejemplos/ontologias/shapes.ttl) — requisitos del catálogo.
- [\`validar.py\`](../ejemplos/ontologias/validar.py) — validador Python.

## Comprender el ejemplo

El fichero de datos declara:

\`\`\`turtle
ex:libro001 a ex:Libro ;
  ex:titulo "El mapa de los grafos" ;
  ex:isbn "ISBN-001" .
\`\`\`

La forma SHACL exige al menos un título y un ISBN. En SHACL, \`sh:minCount 1\` indica una condición de completitud para los nodos seleccionados. En OWL, la ausencia de una propiedad no implica por sí sola un error de datos.

## Prueba negativa reproducible

\`\`\`bash
python -m pytest laboratorios/tests/test_ontologias.py -q
\`\`\`

El test \`test_quitar_titulo_produce_error_shacl\` elimina el título de un **grafo en memoria** y comprueba que la validación falla. El archivo original permanece intacto.

## Ejercicios

1. Añade \`sh:maxCount 1\` al ISBN y comprueba qué sucede con dos ISBN para el mismo libro.
2. Añade un tercer libro sin título en una copia de \`biblioteca.ttl\`. ¿Qué informe genera?
3. Añade un libro sin el triple \`rdf:type ex:Libro\`. ¿Es seleccionado por la forma \`sh:targetClass ex:Libro\` sin inferencia?
4. Explica por qué \`rdfs:subClassOf\` y \`skos:broader\` no son intercambiables.

## Soluciones orientativas

**Ejercicio 1:** añade \`sh:maxCount 1\` al \`sh:property\` asociado a \`ex:isbn\`. El validador debería detectar un recurso con dos valores distintos de ISBN.

**Ejercicio 3:** si el recurso no es objetivo de la forma y no hay inferencia adecuada, puede no comprobarse. Debes diseñar el alcance de las validaciones.

## Fuentes normativas

- [OWL 2 Primer — W3C](https://www.w3.org/TR/owl2-primer/)
- [SHACL — W3C](https://www.w3.org/TR/shacl/)
- [RDF 1.1 Primer — W3C](https://www.w3.org/TR/rdf11-primer/)
