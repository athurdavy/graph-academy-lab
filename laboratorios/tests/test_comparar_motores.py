import importlib.util
import sys
from pathlib import Path

import pytest

src = Path(__file__).resolve().parents[1] / "comparar_motores.py"
spec = importlib.util.spec_from_file_location("comparar_lab", src)
lab = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lab
spec.loader.exec_module(lab)


def test_mismas_filas_en_orden_diferente():
    a = [{"isbn": "ISBN-001", "titulo": "A"}, {"isbn": "ISBN-002", "titulo": "B"}]
    b = list(reversed(a))
    assert lab.comparar_resultados(a, b)


def test_no_oculta_filas_duplicadas():
    a = [{"isbn": "ISBN-001", "titulo": "A"}]
    b = a + a
    assert not lab.comparar_resultados(a, b)


def test_un_titulo_distinto_es_error_de_equivalencia():
    assert not lab.comparar_resultados(
        [{"isbn": "ISBN-001", "titulo": "A"}],
        [{"isbn": "ISBN-001", "titulo": "B"}],
    )


def test_calculos_ejemplo_sintetico():
    assert lab.resumen_tiempos([7, 9, 8, 10, 41]) == {
        "n": 5, "mediana_ms": 9, "p95_ms": 41
    }


def test_no_admite_tiempos_vacios_o_negativos():
    with pytest.raises(ValueError):
        lab.resumen_tiempos([])
    with pytest.raises(ValueError):
        lab.resumen_tiempos([7, -1])
