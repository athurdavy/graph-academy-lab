"""Auditoría de calidad para datos ficticios de una biblioteca.

No modifica los registros y no declara verdadero ningún hecho del mundo real.
Uso: python laboratorios/calidad_catalogo.py
"""
from collections import Counter
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Incidencia:
    codigo: str
    fila: int
    detalle: str


def auditar_libros(registros: Iterable[dict]) -> list[Incidencia]:
    """Examina reglas explícitas: identificador, título, año y ISBN duplicado.

    Los números de fila empiezan en 1 y el orden es el recibido.
    """
    filas = list(registros)
    isbns = [
        str(fila.get("isbn", "") or "").strip()
        for fila in filas
    ]
    recuento = Counter(x for x in isbns if x)
    incidencias = []
    for numero, (fila, isbn) in enumerate(zip(filas, isbns), start=1):
        titulo = fila.get("titulo")
        if not isbn:
            incidencias.append(Incidencia("ISBN_FALTANTE", numero, "ISBN vacío"))
        elif recuento[isbn] > 1:
            incidencias.append(Incidencia("ISBN_DUPLICADO", numero, isbn))
        if not isinstance(titulo, str) or not titulo.strip():
            incidencias.append(Incidencia("TITULO_FALTANTE", numero, "Título no informado"))
        anio = fila.get("anio")
        if type(anio) is not int or not 1450 <= anio <= 2100:
            incidencias.append(Incidencia("ANIO_INVALIDO", numero, str(anio)))
    return incidencias


REGISTROS_VALIDOS = [
    {"isbn": "ISBN-001", "titulo": "El mapa de los grafos", "anio": 2022},
    {"isbn": "ISBN-002", "titulo": "Rutas de conocimiento", "anio": 2024},
]
REGISTROS_CON_PROBLEMAS = [
    {"isbn": "ISBN-001", "titulo": "El mapa de los grafos", "anio": 2022},
    {"isbn": "ISBN-001", "titulo": "Otro libro", "anio": 2024},
    {"isbn": "", "titulo": "", "anio": "desconocido"},
]


if __name__ == "__main__":
    for nombre, filas in [
        ("Datos válidos", REGISTROS_VALIDOS),
        ("Datos con problemas", REGISTROS_CON_PROBLEMAS),
    ]:
        print(nombre)
        errores = auditar_libros(filas)
        if not errores:
            print("  Sin incidencias según las reglas configuradas")
        for error in errores:
            print(f"  Fila {error.fila}: {error.codigo} ({error.detalle})")
