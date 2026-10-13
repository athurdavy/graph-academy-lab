# Semana 05 — Consultas Cypher: de SQL a patrones

![Modelo de biblioteca digital](../assets/biblioteca-grafo.svg)

## Objetivos

Consultar nodos y relaciones con `MATCH`, filtrar con `WHERE`, proyectar con `RETURN`, agrupar con `WITH` y controlar resultados con `ORDER BY` y `LIMIT`.

## 1. Pensar en patrones

En SQL escribes `JOIN` entre tablas. En Cypher expresas el patrón que quieres encontrar:

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
RETURN a.nombre, l.titulo;
```

La flecha `->` es parte de la semántica del patrón. Una consulta sin dirección `-[:ESCRIBIO]-` encuentra relaciones en cualquiera de los dos sentidos; eso no significa que el significado de la relación sea simétrico.

## 2. Consultas progresivas

### Filtrar

```cypher
MATCH (l:Libro)
WHERE l.anio >= 2020
RETURN l.titulo AS titulo, l.anio AS anio
ORDER BY anio DESC, titulo;
```

### Recorrer dos saltos

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema)
RETURN DISTINCT a.nombre AS autor, t.nombre AS tema
ORDER BY autor, tema;
```

### Agregar

```cypher
MATCH (t:Tema)<-[:TRATA_SOBRE]-(l:Libro)
RETURN t.nombre AS tema, count(DISTINCT l) AS total
ORDER BY total DESC, tema;
```

### Encadenar con WITH

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)
WITH a, count(l) AS numeroLibros
WHERE numeroLibros >= 1
RETURN a.nombre AS autor, numeroLibros
ORDER BY numeroLibros DESC;
```

### Relaciones opcionales

```cypher
MATCH (l:Libro)
OPTIONAL MATCH (l)-[:TRATA_SOBRE]->(t:Tema)
RETURN l.titulo AS libro, collect(t.nombre) AS temas;
```

**Matiz:** `OPTIONAL MATCH` conserva filas incluso cuando no hay coincidencia, usando `null` para lo que falte. Comprueba cómo afecta `null` a tus agregaciones.

## 3. Errores frecuentes

- `MATCH (a)-[r]->(b)` sin etiquetas ni filtros en grafos grandes puede recorrer demasiados datos.
- `RETURN a, b` no es equivalente a seleccionar propiedades concretas.
- `DISTINCT` elimina duplicados de filas proyectadas, no «corrige» datos duplicados.
- Una relación no implica que la afirmación sea verdadera: depende de la calidad de la carga.

## 4. Laboratorio: doce retos

1. Lista todos los libros.
2. Lista todos los autores ordenados.
3. Filtra libros posteriores a 2020.
4. Busca un libro por ISBN.
5. Muestra autores y libros.
6. Cuenta libros por autor.
7. Cuenta libros por tema.
8. Encuentra libros de un tema dado.
9. Encuentra autores que escribieron sobre el mismo tema.
10. Lista lectores y sus libros leídos.
11. Muestra libros sin relaciones `TRATA_SOBRE`.
12. Obtén temas relacionados con un autor a dos saltos.

### Soluciones orientativas de los retos 8 y 11

```cypher
MATCH (l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo: 'GRAFOS'})
RETURN l.titulo ORDER BY l.titulo;
```

```cypher
MATCH (l:Libro)
WHERE NOT EXISTS { MATCH (l)-[:TRATA_SOBRE]->(:Tema) }
RETURN l.titulo ORDER BY l.titulo;
```

## 5. Entregable

Archivo `consultas.cypher` con doce consultas, una captura de resultados y explicación de por qué cada patrón encuentra lo que buscas.

## Fuentes

- [Cypher: cláusulas](https://neo4j.com/docs/cypher-manual/current/clauses/)
- [GraphAcademy: Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/)
