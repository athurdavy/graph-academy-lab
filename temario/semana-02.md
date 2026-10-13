# Semana 02 — Recorridos, caminos y preguntas que puede responder un grafo

![Biblioteca ficticia](../assets/biblioteca-grafo.svg)

**Unidad 2 de 42 · Fundamentos.** Antes: [Semana 01 — modelado](semana-01.md). Después: [Semana 03 — grafo de propiedades y RDF](semana-03.md). Tiempo: 8–12 horas.

## 1. ¿Por qué recorrer relaciones?

En la semana anterior representaste los datos de una biblioteca como nodos y aristas con dirección y tipo. Ahora vamos a **obtener respuestas mediante caminos**.

Dos preguntas no son iguales:

- «¿Qué libros escribió Marina?» es una consulta de **un salto**: \`Autor -ESCRIBIO→ Libro\`.
- «¿Sobre qué temas escribió Marina?» necesita **dos saltos**: \`Autor -ESCRIBIO→ Libro -TRATA_SOBRE→ Tema\`.

No es magia: equivale a combinar relaciones respetando su dirección y filtrando sus tipos. SQL también puede hacerlo con JOIN. En Cypher expresarás patrones de forma muy visual.

## 2. Caminos, alcanzabilidad y ciclos

Un **camino** es una secuencia ordenada de nodos conectados. Si hay un camino desde A hasta B, decimos que B es alcanzable desde A, teniendo en cuenta la dirección cuando el grafo es dirigido.

Un **ciclo** vuelve a un nodo anterior. Los ciclos no son universalmente malos. En una red de amistades pueden ser normales; en una jerarquía que debe ser estrictamente acíclica son errores.

En la biblioteca:

- Autor → Libro → Tema es un recorrido semánticamente coherente.
- Autor → Libro ← Lector también puede responder «¿qué lectores han leído libros de este autor?», **cambiando el sentido de la segunda arista en la consulta**.
- No debemos inferir que un lector es autor porque exista un camino entre ambos.

La existencia de un camino no implica equivalencia, causalidad ni verdad adicional. **El significado lo aportan los tipos de relación y las reglas que hayas definido.**

## 3. BFS y DFS: diferencias reales

### Búsqueda en anchura (BFS)

BFS visita primero vecinos cercanos y después distancias crecientes. En grafos **no ponderados**, permite descubrir caminos mínimos en número de aristas. Su coste típico en una representación de listas de adyacencia es O(V+E).

### Búsqueda en profundidad (DFS)

DFS explora un camino hasta donde puede y luego retrocede. Es útil en exploración, detección de estructuras y algoritmos relacionados. **DFS no garantiza el camino con menos aristas.**

### Grafo ponderado

Si cada arista tiene un coste —por ejemplo, distancia o tiempo— el camino con menos saltos puede no ser el de menor coste. Para pesos no negativos suele utilizarse Dijkstra, que estudiaremos en el bloque de Graph Data Science.

## 4. Laboratorio reproducible

Desde la raíz del repositorio y con las dependencias del curso instaladas:

~~~python
from laboratorios.biblioteca import construir_biblioteca
import networkx as nx

g = construir_biblioteca()
origen = "autor:A-001"
destino = "tema:GRAFOS"

print(nx.shortest_path(g, origen, destino))
print(nx.shortest_path_length(g, origen, destino))
~~~

**Salida esperada:**

~~~text
['autor:A-001', 'libro:ISBN-001', 'tema:GRAFOS']
2
~~~

En este ejemplo la longitud representa **dos aristas**. No es duración, distancia física ni intensidad semántica.

¿Por qué es posible importar \`laboratorios.biblioteca\`? Al ejecutar el código desde la raíz del repositorio, Python incluye esa ruta en la búsqueda de módulos y el directorio del laboratorio funciona como paquete de espacio de nombres en Python moderno. Si tu IDE usa otro directorio de trabajo, configura la raíz del proyecto o adapta la importación.

### Buscar todos los caminos simples

~~~python
caminos = list(nx.all_simple_paths(
    g, source="autor:A-001", target="tema:GRAFOS", cutoff=4
))
for camino in caminos:
    print(camino)
~~~

En este grafo los caminos simples terminan en el tema y pasan por el libro que está etiquetado con Grafos. Si agregas más libros conectados al mismo tema, obtendrás más caminos.

**Atención al rendimiento:** enumerar *todos* los caminos simples puede ser extremadamente costoso en grafos grandes. Acota la longitud, limita resultados y piensa en las consultas que necesita el negocio.

## 5. No confundas búsqueda estructural con consulta semántica

\`nx.shortest_path\` busca según la **estructura y las reglas de coste** del grafo, no según conceptos OWL, restricciones SHACL ni jerarquías SKOS. Tampoco sabe que \`ESCRIBIO\` significa autoría; ve aristas.

Si necesitas permitir únicamente el patrón \`Autor → Libro → Tema\`, debes **validar** el tipo de cada arista. Esa es la razón por la que Cypher y SPARQL permiten especificar patrones con predicados y relaciones concretas.

## 6. Ejercicios graduados

**A.** Implementa una función que encuentre temas asociados a un autor recorriendo \`ESCRIBIO\` y después \`TRATA_SOBRE\`, sin utilizar el camino mínimo genérico.

**B.** Agrega un segundo tema \`CIENCIA\` asociado a \`ISBN-002\`. ¿Qué temas devuelve el autor?

**C.** Cambia la dirección de una arista \`TRATA_SOBRE\`. ¿Qué resultado cambia? ¿Se rompe algún camino?

**D.** Crea un grafo pequeño A→B→D y A→C→D. ¿Qué camino es más corto? ¿Hay necesariamente uno único?

**E.** Añade pesos A→B=10, B→D=10, A→C=1, C→D=1. Calcula la ruta de menor coste con Dijkstra y compara con el número de saltos.

## 7. Soluciones razonadas

**A.** Recorrer tipos es diferente de usar \`shortest_path\` sin filtros:

~~~python
def temas_por_autor(g, autor):
    temas = set()
    for _, libro, edge in g.out_edges(autor, data=True):
        if edge["tipo"] != "ESCRIBIO":
            continue
        for _, tema, edge2 in g.out_edges(libro, data=True):
            if edge2["tipo"] == "TRATA_SOBRE":
                temas.add(tema)
    return sorted(temas)

assert temas_por_autor(g, "autor:A-001") == ["tema:GRAFOS"]
~~~

**D.** Los dos caminos tienen dos saltos. Una función de camino mínimo puede elegir uno; no implica que sea el único.

**E.** La ruta A→C→D tiene coste 2. La ruta A→B→D tiene coste 20. Con pesos es fundamental saber qué representa «coste»: *menor* valor debe ser mejor para Dijkstra.

## 8. Errores que debes poder diagnosticar

- Un recorrido sin filtros puede producir coincidencias **estructuralmente válidas, pero semánticamente incorrectas**.
- DFS puede encontrar una ruta, pero no necesariamente la de menor longitud.
- El camino mínimo por saltos no equivale al mínimo ponderado.
- Enumerar todos los caminos puede provocar una explosión combinatoria.
- Que una consulta devuelva 0 filas no garantiza que no exista información: puede haber un error de dirección.

## 9. Autoevaluación y continuidad

Explica BFS y DFS sin memorizar definiciones, dibuja un camino de dos saltos y justifica la dirección de cada relación. Implementa el ejercicio A con un test.

**Siguiente unidad:** [Semana 03 — de los grafos de propiedades a RDF](semana-03.md). En la semana 04 volveremos al mismo caso usando Neo4j y consultas Cypher.

## Documentación oficial

- [NetworkX Algorithms](https://networkx.org/documentation/stable/reference/algorithms/)
- [NetworkX shortest_path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html)
- [Neo4j Cypher MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/)
