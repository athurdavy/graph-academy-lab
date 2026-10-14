"""Ejemplo educativo: conservar revisiones de afirmaciones sin sobrescribir historia."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Revision:
    identificador: str
    afirmacion: str
    fuente: str
    revisor: str
    fecha: date
    estado: str


ESTADOS = {"propuesta", "aceptada", "rechazada"}


def crear_revision(identificador, afirmacion, fuente, revisor, fecha, estado):
    if not all(isinstance(x, str) and x.strip() for x in
               (identificador, afirmacion, fuente, revisor)):
        raise ValueError("Identificador, afirmación, fuente y revisor obligatorios")
    if not isinstance(fecha, date):
        raise TypeError("La fecha debe ser date")
    if estado not in ESTADOS:
        raise ValueError("Estado no permitido")
    return Revision(
        identificador.strip(), afirmacion.strip(), fuente.strip(),
        revisor.strip(), fecha, estado,
    )


def historial_por_afirmacion(revisiones, afirmacion):
    """Devuelve el historial sin borrar estados anteriores."""
    return sorted(
        (r for r in revisiones if r.afirmacion == afirmacion),
        key=lambda r: (r.fecha, r.identificador),
    )


if __name__ == "__main__":
    filas = [
        crear_revision("REV-001", "ISBN-001 TRATA_SOBRE GRAFOS",
                      "FICHA-001", "editor-01", date(2026, 1, 10), "propuesta"),
        crear_revision("REV-002", "ISBN-001 TRATA_SOBRE GRAFOS",
                      "FICHA-002", "editor-02", date(2026, 1, 11), "aceptada"),
    ]
    for fila in historial_por_afirmacion(filas, "ISBN-001 TRATA_SOBRE GRAFOS"):
        print(fila.identificador, fila.estado, fila.fuente)
