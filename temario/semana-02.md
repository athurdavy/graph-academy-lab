# Semana 02 — Recorridos y algoritmos de grafos

**Objetivo:** entender cómo se explora un grafo, cuándo un camino representa una respuesta útil y qué costes tiene.

## Conceptos

- **Vecindad:** nodos conectados directamente.
- **Camino:** secuencia de nodos enlazados por aristas.
- **BFS:** búsqueda en anchura; permite hallar caminos mínimos en número de saltos en grafos no ponderados.
- **DFS:** búsqueda en profundidad; útil para exploración y ciertos análisis estructurales.
- **Ciclos:** un camino que vuelve al origen; pueden ser válidos o señalar errores según la relación.
- **Centralidad:** familia de métricas estructurales; no equivale automáticamente a relevancia de negocio.

## Laboratorio

```python
import networkx as nx

g = nx.DiGraph()
g.add_edges_from([
    ("ConceptoLibro", "CampoCRM"),
    ("CampoCRM", "TablaLibros"),
    ("ConceptoLibro", "InformeVentas"),
    ("InformeVentas", "TablaLibros"),
])
print(nx.shortest_path(g, "ConceptoLibro", "TablaLibros"))
print(list(nx.bfs_tree(g, "ConceptoLibro")))
assert nx.has_path(g, "ConceptoLibro", "TablaLibros")
```

## Ejercicios

1. Añade una relación de «sinónimo» y decide si debe ser dirigida.
2. Comprueba si hay ciclos en una jerarquía que diseñes como acíclica.
3. Mide cómo crece el número de nodos visitados al aumentar el grafo.
4. Explica por qué un camino entre un concepto y una tabla no prueba por sí solo que el mapeo sea correcto.

## Entregable

Un script con tres consultas de recorrido, tres tests y una explicación de la semántica de cada arista.

## Fuentes

- [NetworkX Algorithms](https://networkx.org/documentation/stable/reference/algorithms/index.html)
- [NetworkX shortest_path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html)
