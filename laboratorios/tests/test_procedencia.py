import importlib.util
import sys
from datetime import date
from pathlib import Path

import pytest

src = Path(__file__).resolve().parents[1] / "procedencia.py"
spec = importlib.util.spec_from_file_location("procedencia_lab", src)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def revision(ident, fecha, estado="propuesta"):
    return mod.crear_revision(
        ident, "ISBN-001 TRATA_SOBRE GRAFOS", "FICHA-001",
        "editor-prueba", fecha, estado
    )


def test_historial_guarda_todas_las_revisiones():
    r1 = revision("REV-1", date(2026, 1, 1))
    r2 = revision("REV-2", date(2026, 1, 2), "aceptada")
    assert mod.historial_por_afirmacion([r2, r1], r1.afirmacion) == [r1, r2]


def test_rechaza_estado_desconocido():
    with pytest.raises(ValueError):
        revision("REV-3", date(2026, 1, 3), "publicado")


def test_rechaza_fuente_vacia():
    with pytest.raises(ValueError):
        mod.crear_revision("REV-4", "hecho", "", "editor",
                           date(2026, 1, 4), "propuesta")


def test_no_mezcla_afirmaciones():
    r = revision("REV-1", date(2026, 1, 1))
    assert mod.historial_por_afirmacion([r], "ISBN-002 TRATA_SOBRE GRAFOS") == []
