"""Demostración de arquitectura hexagonal mínima, sin infraestructura externa."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Libro:
    isbn: str
    titulo: str


class LibroRepository(Protocol):
    def buscar(self, isbn: str) -> Libro | None:
        ...


class RepositorioMemoria:
    def __init__(self, libros: list[Libro]):
        self._libros = {libro.isbn: libro for libro in libros}

    def buscar(self, isbn: str) -> Libro | None:
        return self._libros.get(isbn)


class ConsultarLibro:
    def __init__(self, repositorio: LibroRepository):
        self._repositorio = repositorio

    def ejecutar(self, isbn: str) -> Libro | None:
        clave = isbn.strip()
        if not clave:
            raise ValueError("El ISBN no puede estar vacío")
        return self._repositorio.buscar(clave)
