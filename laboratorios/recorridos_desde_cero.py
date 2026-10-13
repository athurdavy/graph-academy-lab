"""Semana 02: BFS, DFS y Dijkstra desde cero. Grafo completamente ficticio."""
from collections import deque

import networkx as nx

GRAFO = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E"],
    "E": ["D"],
    "D": [],
}


def bfs_camino(grafo: dict[str, list[str]], inicio: str, objetivo: str) -> list[str] | None:
    """BFS: explora primero los nodos con menos saltos."""
    if inicio not in grafo or objetivo not in grafo:
        return None
    pendientes = deque([(inicio, [inicio])])
    visitados = {inicio}
    while pendientes:
        nodo, camino = pendientes.popleft()
        if nodo == objetivo:
            return camino
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                pendientes.append((vecino, camino + [vecino]))
    return None


def dfs_camino(grafo: dict[str, list[str]], inicio: str, objetivo: str) -> list[str] | None:
    """DFS: profundiza en una rama y retrocede si hace falta."""
    if inicio not in grafo or objetivo not in grafo:
        return None
    pendientes = [(inicio, [inicio])]
    visitados = set()
    while pendientes:
        nodo, camino = pendientes.pop()
        if nodo == objetivo:
            return camino
        if nodo in visitados:
            continue
        visitados.add(nodo)
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                pendientes.append((vecino, camino + [vecino]))
    return None


def grafo_ponderado() -> nx.DiGraph:
    """Dos rutas: 2 saltos y coste 20, frente a 3 saltos y coste 3."""
    g = nx.DiGraph()
    g.add_edge("A", "B", coste=10)
    g.add_edge("B", "D", coste=10)
    g.add_edge("A", "C", coste=1)
    g.add_edge("C", "E", coste=1)
    g.add_edge("E", "D", coste=1)
    return g


def comparar_caminos() -> tuple[list[str], list[str], int]:
    g = grafo_ponderado()
    return (
        nx.shortest_path(g, "A", "D"),
        nx.shortest_path(g, "A", "D", weight="coste"),
        nx.shortest_path_length(g, "A", "D", weight="coste"),
    )


if __name__ == "__main__":
    print("BFS (menos saltos):", bfs_camino(GRAFO, "A", "D"))
    print("DFS (primer camino según orden):", dfs_camino(GRAFO, "A", "D"))
    ruta_saltos, ruta_coste, coste = comparar_caminos()
    print("Ruta menos saltos:", ruta_saltos)
    print("Ruta menor coste:", ruta_coste)
    print("Coste mínimo:", coste)
