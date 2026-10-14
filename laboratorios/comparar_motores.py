"""Comparación de resultados y estadísticos sin inventar benchmarks reales."""
from math import ceil
from statistics import median


def comparar_resultados(neo4j_rows, arcadedb_rows):
    """Comprueba equivalencia de pares (isbn, titulo) sin considerar orden.

    Usa Counter para no ocultar duplicados que DISTINCT podría enmascarar.
    """
    from collections import Counter

    def normalizar(filas):
        return Counter((fila["isbn"], fila["titulo"]) for fila in filas)

    return normalizar(neo4j_rows) == normalizar(arcadedb_rows)


def resumen_tiempos(valores_ms):
    """Devuelve tamaño, mediana y percentil 95 por rango más próximo.

    Se calculan sobre MEDICIONES APORTADAS por el usuario, no medidas propias.
    """
    tiempos = list(valores_ms)
    if not tiempos or any(type(x) not in (int, float) or x < 0 for x in tiempos):
        raise ValueError("Se necesitan tiempos positivos o cero")
    ordenados = sorted(tiempos)
    p95 = ordenados[ceil(0.95 * len(ordenados)) - 1]
    return {"n": len(tiempos), "mediana_ms": median(tiempos), "p95_ms": p95}


if __name__ == "__main__":
    neo4j = [{"isbn": "ISBN-001", "titulo": "El mapa de los grafos"}]
    arcadedb = [{"isbn": "ISBN-001", "titulo": "El mapa de los grafos"}]
    print("Resultados equivalentes:", comparar_resultados(neo4j, arcadedb))
    print("Tiempos inventados, NO benchmark:", resumen_tiempos([7, 9, 8, 10, 41]))
