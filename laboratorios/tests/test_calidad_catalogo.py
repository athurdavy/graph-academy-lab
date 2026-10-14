"""Pruebas locales: casos correctos, errores y límites de una política de calidad."""
import importlib.util
from pathlib import Path

source = Path(__file__).resolve().parents[1] / "calidad_catalogo.py"
spec = importlib.util.spec_from_file_location("calidad_catalogo", source)
mod = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_datos_validos_no_generan_incidentes():
    assert mod.auditar_libros(mod.REGISTROS_VALIDOS) == []


def test_identificadores_duplicados_se_detectan_en_ambas_filas():
    errores = mod.auditar_libros(mod.REGISTROS_CON_PROBLEMAS)
    assert [(e.codigo, e.fila) for e in errores if e.codigo == "ISBN_DUPLICADO"] == [
        ("ISBN_DUPLICADO", 1), ("ISBN_DUPLICADO", 2),
    ]


def test_registro_incompleto_identifica_tres_problemas():
    errores = mod.auditar_libros(mod.REGISTROS_CON_PROBLEMAS)
    codigos = {e.codigo for e in errores if e.fila == 3}
    assert codigos == {"ISBN_FALTANTE", "TITULO_FALTANTE", "ANIO_INVALIDO"}


def test_no_modifica_datos_de_entrada():
    origen = [{"isbn": " ISBN-005 ", "titulo": "Prueba", "anio": 2020}]
    antes = [dict(x) for x in origen]
    mod.auditar_libros(origen)
    assert origen == antes


def test_texto_en_anyo_no_es_entero_valido():
    errores = mod.auditar_libros(
        [{"isbn": "ISBN-777", "titulo": "Ficción", "anio": "2022"}]
    )
    assert [e.codigo for e in errores] == ["ANIO_INVALIDO"]


def test_diferentes_isbn_pueden_tener_mismo_titulo():
    registros = [
        {"isbn": "ISBN-101", "titulo": "El mar imaginario", "anio": 2020},
        {"isbn": "ISBN-102", "titulo": "El mar imaginario", "anio": 2021},
    ]
    assert mod.auditar_libros(registros) == []
