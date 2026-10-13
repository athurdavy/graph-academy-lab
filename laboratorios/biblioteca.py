"""Modelo público y ficticio de una biblioteca para practicar grafos."""
from __future__ import annotations

import networkx as nx


def construir_biblioteca() -> nx.MultiDiGraph:
    """Devuelve un grafo reproducible: cinco entidades y cuatro relaciones."""
    grafo = nx.MultiDiGraph()
    grafo.add_node("autor:A-001", tipo="Autor", nombre="Marina Soler")
    grafo.add_node("libro:ISBN-001", tipo="Libro", titulo="El mapa de los grafos")
    grafo.add_node("libro:ISBN-002", tipo="Libro", titulo="Rutas de conocimiento")
    grafo.add_node("tema:GRAFOS", tipo="Tema", nombre="Grafos")
    grafo.add_node("lector:L-001", tipo="Lector", alias="lector_demo")

    grafo.add_edge("autor:A-001", "libro:ISBN-001", tipo="ESCRIBIO")
    grafo.add_edge("autor:A-001", "libro:ISBN-002", tipo="ESCRIBIO")
    grafo.add_edge("libro:ISBN-001", "tema:GRAFOS", tipo="TRATA_SOBRE")
    grafo.add_edge("lector:L-001", "libro:ISBN-001", tipo="LEYO")
    return grafo


def libros_de_autor(grafo: nx.MultiDiGraph, id_autor: str) -> list[str]:
    """Busca libros por aristas salientes ESCRIBIO, sin confundir otras aristas."""
    origen = f"autor:{id_autor}"
    if origen not in grafo:
        return []
    libros = {
        destino
        for _, destino, datos in grafo.out_edges(origen, data=True)
        if datos["tipo"] == "ESCRIBIO" and grafo.nodes[destino]["tipo"] == "Libro"
    }
    return sorted(libros)


def libros_sobre_tema(grafo: nx.MultiDiGraph, codigo: str) -> list[str]:
    """Recorre aristas entrantes TRATA_SOBRE hasta el tema indicado."""
    destino = f"tema:{codigo}"
    if destino not in grafo:
        return []
    return sorted({
        origen
        for origen, _, datos in grafo.in_edges(destino, data=True)
        if datos["tipo"] == "TRATA_SOBRE"
    })


if __name__ == "__main__":
    g = construir_biblioteca()
    print(f"Nodos: {g.number_of_nodes()}, relaciones: {g.number_of_edges()}")
    print("Libros de Marina:", libros_de_autor(g, "A-001"))
    print("Libros sobre grafos:", libros_sobre_tema(g, "GRAFOS"))
