"""Guardarraíles editoriales: no sustituye la lectura humana ni pruebas de motores."""
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[2]
TEMARIO = ROOT / "temario"


@pytest.mark.parametrize("week", range(1, 25))
def test_todas_las_semanas_tienen_contenido_y_titulo(week):
    path = TEMARIO / f"semana-{week:02d}.md"
    assert path.is_file(), f"Falta la semana {week:02d}"
    content = path.read_text(encoding="utf-8")
    assert content.startswith(f"# Semana {week:02d}"), path.name
    assert len(content) >= 800, f"Lección sospechosamente breve: {path.name}"


@pytest.mark.parametrize("week", range(1, 18))
def test_lecciones_en_desarrollo_no_tienen_fences_escapados(week):
    content = (TEMARIO / f"semana-{week:02d}.md").read_text(encoding="utf-8")
    assert "\\`" not in content, f"Markdown mal escapado en semana {week:02d}"
    starts = re.findall(r"(?m)^([~`]{3,})(?:[A-Za-z0-9_-]+)?\\s*$", content)
    # La validación de fences debe comprobar también cierres.
    assert len(starts) % 2 == 0, f"Bloque de código sin cerrar en semana {week:02d}"


@pytest.mark.parametrize("week", range(18, 25))
def test_material_avanzado_muestra_estado_real(week):
    content = (TEMARIO / f"semana-{week:02d}.md").read_text(encoding="utf-8")
    assert "Estado pedagógico: unidad introductoria" in content
