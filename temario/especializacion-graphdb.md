# Especialización práctica: GraphDB y SPARQL

**Caso público:** biblioteca ficticia. [GraphDB](https://graphdb.ontotext.com/documentation/) (Ontotext) es un motor RDF con repositorios SPARQL e inferencia configurable; no es Neo4j.

## Conceptos

Repositorio RDF, triples, grafos con nombre, regímenes de inferencia, importación y exportación RDF, SHACL y consultas SPARQL. Su comportamiento depende de la **versión y la edición**; no se presupone soporte idéntico entre productos.

## Laboratorio de 2–3 horas

1. Instala GraphDB mediante la documentación oficial y revisa las condiciones de licencia.
2. Abre Workbench y crea un repositorio de pruebas. Anota su configuración de inferencia.
3. Importa los archivos ficticios ejemplos/ontologias/temas.ttl y ejemplos/ontologias/biblioteca.ttl.
4. Ejecuta SELECT para listar libros y temas.
5. Contrasta una consulta sobre tipos explícitos con el resultado bajo el régimen de inferencia configurado.
6. Exporta el dataset en un formato RDF soportado, importa en un repositorio vacío y compara recuentos y consultas.
7. Describe cómo integrarías un cliente Python con el endpoint SPARQL según las opciones de autenticación.

## Consulta SPARQL básica

~~~sparql
PREFIX ex: <https://example.org/biblioteca/>
SELECT ?libro ?titulo WHERE {
  ?libro a ex:Libro ; ex:titulo ?titulo .
}
ORDER BY ?titulo
~~~

Si un resultado no aparece, comprueba tanto los datos cargados como la configuración de inferencia. No concluyas que un dato «no existe» únicamente por no recuperarlo.

## Evaluación

Demuestra las consultas, los resultados esperados, la versión de GraphDB, el régimen de inferencia, la exportación/reimportación y el tratamiento de errores de entrada y autenticación.

## Referencias oficiales

- [GraphDB Documentation](https://graphdb.ontotext.com/documentation/)
- [SPARQL 1.1 Query — W3C](https://www.w3.org/TR/sparql11-query/)
- [RDF 1.1 Concepts — W3C](https://www.w3.org/TR/rdf11-concepts/)
