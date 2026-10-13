# Semana 01 — Fundamentos de grafos

**Duración:** 8–10 h. **Requisitos:** Python básico.

## Objetivos de aprendizaje

Al terminar podrás explicar qué es un grafo dirigido, distinguir concepto de instancia, interpretar tipos de relación y crear un modelo reproducible con Python.

## 1. Grafo y semántica

Formalmente, un grafo se expresa como **G = (V, E)**. V es el conjunto de vértices; E es el conjunto de aristas. En un grafo dirigido, una arista (a,b) no equivale necesariamente a (b,a).

En un diccionario semántico, una arista no debe ser una simple línea sin significado: hay que documentar el tipo de relación. Por ejemplo:

- **Empleado SUBTIPO_DE Persona**: relación entre categorías o clases.
- **Ana ES_INSTANCIA_DE Empleado**: relación entre individuo y categoría.
- **Ana PERTENECE_A DepartamentoVentas**: relación entre entidades.

No es correcto inferir automáticamente que un empleado concreto es un subtipo de persona: es una **instancia** de una categoría.

## 2. Primer ejemplo en Python

Instala NetworkX en un entorno virtual:

```bash
python -m venv .venv
python -m pip install networkx
```

Guarda como `ejercicio_01.py`:

```python
import networkx as nx

g = nx.MultiDiGraph()
g.add_edge("Empleado", "Persona", relacion="SUBTIPO_DE")
g.add_edge("Ana", "Empleado", relacion="INSTANCIA_DE")
g.add_edge("Ana", "Ventas", relacion="PERTENECE_A")

for origen, destino, datos in g.edges(data=True):
    print(origen, datos["relacion"], destino)

assert g.has_edge("Empleado", "Persona")
assert g.number_of_edges() == 3
```

¿Por qué `MultiDiGraph`? Porque permite varias aristas dirigidas entre el mismo par de nodos; esto puede ser útil cuando existen diferentes relaciones. **Atención:** un grafo de Python no es por sí mismo una ontología.

## 3. Ejercicios

**A. Modelado.** Añade Proyecto, Tecnología y los individuos «ProyectoAtlas» y «Python». Justifica qué nodos son conceptos y cuáles instancias.

**B. Cardinalidad.** ¿Una persona puede pertenecer a varios departamentos? El modelo por sí solo no decide la regla: escribe el requisito que necesitarías confirmar.

**C. Dirección.** Compara `Ana PERTENECE_A Ventas` y `Ventas TIENE_MIEMBRO Ana`. ¿Son equivalentes? ¿Cómo documentarías una relación inversa?

**D. Tests.** Añade aserciones para garantizar que no existen relaciones con tipo vacío.

## 4. Aplicación al proyecto

Crea una tabla con las columnas: identificador, nombre, definición, tipo (concepto/instancia), relaciones permitidas y fuente. Es una primera aproximación; más adelante la formalizaremos con SKOS/RDF si los requisitos lo justifican.

## 5. Autoevaluación

1. ¿Por qué importa la dirección de una arista?
2. ¿Qué diferencia existe entre una categoría y un individuo?
3. ¿Puede un grafo contener relaciones ambiguas? ¿Cómo se corrige?
4. ¿Qué aporta NetworkX y qué no aporta frente a una base de datos persistente?

## Fuentes oficiales

- [NetworkX: documentación](https://networkx.org/documentation/stable/)
- [NetworkX MultiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html)
- [Neo4j Graph Data Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/)
- [RDF 1.1 Primer — W3C](https://www.w3.org/TR/rdf11-primer/)
