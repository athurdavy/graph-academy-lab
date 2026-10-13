# Proyecto transversal — Biblioteca digital ficticia

Este proyecto de formación es **totalmente inventado** y utiliza libros, autores, lectores y temas ficticios. No se basa en información de ninguna empresa.

## Objetivo

Construir un catálogo navegable que permita encontrar libros por autor o tema, registrar lecturas y estudiar la evolución hacia un grafo de conocimiento.

## Entidades

- Libro: ISBN ficticio, título y año.
- Autor: identificador y nombre ficticio.
- Tema: código y nombre.
- Lector: identificador y alias ficticio.

## Relaciones

- `Autor -[:ESCRIBIO]-> Libro`
- `Libro -[:TRATA_SOBRE]-> Tema`
- `Lector -[:LEYO]-> Libro`

## Hitos

1. Modelar el grafo con NetworkX.
2. Implementarlo en Neo4j AuraDB.
3. Consultarlo con Cypher.
4. Importar datos desde CSV.
5. Crear una aplicación CLI con Python.
6. Comparar su representación con RDF/SKOS como ejercicio académico.
7. Evaluar calidad y procedencia de datos.

## Material

- [Neo4j, semanas 4–7](semana-04.md)
- [Laboratorio de código](../ejemplos/neo4j/)
- [Diagrama visual](../assets/biblioteca-grafo.svg)

**Nota:** todos los datos y escenarios de esta academia son ficticios y públicos.
