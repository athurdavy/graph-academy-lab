# Semana 23 — Pruebas, seguridad y rendimiento: de «funciona» a «es confiable»

**Antes:** [semana 22 — API con FastAPI](semana-22.md), [semana 07 — transacciones](semana-07.md). **Después:** [semana 24 — proyecto final](semana-24.md). **Objetivo:** aprender a distinguir tipos de pruebas, medir consultas sin engañarte y reducir riesgos de seguridad antes de publicar una aplicación.

## 1. ¿Por qué no basta con que mi programa se ejecute?

La API de biblioteca devuelve dos libros del tema GRAFOS. Parece funcionar. Pero un día la conexión falla y tu código devuelve `[]` en vez de informar del problema. Un usuario podría creer que no hay libros sobre ese tema.

Un sistema profesional debe diferenciar:

- **Consulta sin resultados:** es una respuesta válida.
- **Entrada inválida:** el usuario envió una petición que no cumple el contrato.
- **Error de aplicación:** un error de programación o configuración.
- **Indisponibilidad temporal:** el servicio de datos no responde.
- **Dato incorrecto:** el código devuelve algo que está almacenado, pero contradice la fuente de verdad.

Las pruebas deben cubrir esos casos, no solo el más sencillo.

## 2. Tres niveles de pruebas explicados sin jerga

| Tipo | Qué comprueba | Ejemplo |
|---|---|---|
| Unitaria | Una función aislada | Filtrar libros por tema en memoria |
| Integración | Varias partes funcionando juntas | Driver Python ejecuta Cypher contra Neo4j real |
| Extremo a extremo (E2E) | Flujo completo desde la entrada hasta la respuesta | Cliente llama a API, API consulta y devuelve JSON |

Una prueba con un driver simulado puede verificar parámetros y lógica, pero **no prueba que el servidor AuraDB esté disponible ni que Cypher sea compatible con él**.

## 3. Tu primera función de negocio con errores explícitos

```python
def buscar_libros(repositorio, tema):
    if not isinstance(tema, str) or not tema.strip():
        raise ValueError("Tema obligatorio")
    return repositorio.buscar_por_tema(tema.strip())
```

¿Qué hemos decidido?

- El **servicio** valida la entrada.
- El **repositorio** se ocupa de los datos.
- Una lista vacía significa que no hubo coincidencias.
- Una excepción de conexión del repositorio **debe propagarse o gestionarse explícitamente**; no convertirse en lista vacía.

## 4. Prueba unitaria con pytest y un doble de prueba

```python
from unittest.mock import Mock
import pytest

def buscar_libros(repositorio, tema):
    if not isinstance(tema, str) or not tema.strip():
        raise ValueError("Tema obligatorio")
    return repositorio.buscar_por_tema(tema.strip())

def test_devuelve_datos():
    repo = Mock()
    repo.buscar_por_tema.return_value = [{"isbn": "ISBN-001"}]
    assert buscar_libros(repo, " GRAFOS ") == [{"isbn": "ISBN-001"}]
    repo.buscar_por_tema.assert_called_once_with("GRAFOS")

def test_rechaza_entrada_vacia():
    repo = Mock()
    with pytest.raises(ValueError):
        buscar_libros(repo, "")
    repo.buscar_por_tema.assert_not_called()

def test_no_oculta_fallo_de_infraestructura():
    repo = Mock()
    repo.buscar_por_tema.side_effect = ConnectionError("motor inaccesible")
    with pytest.raises(ConnectionError):
        buscar_libros(repo, "GRAFOS")
```

Ejecuta este archivo con `python -m pytest -q` tras instalar pytest.

**Resultado esperado:** tres pruebas pasan. Se comprueban: éxito, entrada inválida y error de infraestructura. Ninguna prueba necesita conectarse a Neo4j.

### ¿Qué significa `Mock`?

Es un **doble de prueba**: un objeto que imita el contrato de una dependencia. Lo usamos para controlar sus resultados. **No demuestra** que la dependencia real funcione.

## 5. Seguridad: cinco decisiones antes de publicar

**1. Credenciales.** Las contraseñas y los URI internos no se guardan en GitHub. Los valores de configuración públicos y privados deben mantenerse separados.

**2. Consultas parametrizadas.** Usa `$codigo` y parámetros del driver, no concatenación de entradas de usuarios en texto Cypher.

**3. Mínimos permisos.** Un servicio que solo consulta libros no necesita una cuenta que pueda administrar toda la base.

**4. Control de acceso.** Si hay datos privados, comprueba autorización en cada operación. No basta con ocultar un botón en la interfaz.

**5. Registro de errores.** Necesitas diagnosticar fallos, pero sin registrar contraseñas, tokens o datos sensibles innecesarios.

**No publiques el servidor de desarrollo de FastAPI directamente como servicio abierto.** El despliegue real requiere configuración de red, HTTPS, límites y autenticación según el contexto.

## 6. Medir rendimiento sin confundir conceptos

**Latencia** es el tiempo entre enviar una petición y recibir la respuesta. **Rendimiento** o *throughput* mide cuánto trabajo completa el sistema por unidad de tiempo.

Dos mediciones habituales:

- **p50**: valor por debajo del cual se encuentran aproximadamente la mitad de las latencias medidas.
- **p95**: valor por debajo del cual se encuentran aproximadamente el 95 % de las latencias medidas.

No pruebes una consulta una sola vez y declares «Neo4j es más rápido». Repite, mide tamaños del dataset, versiones, límites de red, consultas e índices.

### Primer benchmark en Python

```python
from statistics import median
from time import perf_counter

def medir(funcion, repeticiones=30):
    tiempos = []
    for _ in range(repeticiones):
        inicio = perf_counter()
        funcion()
        tiempos.append((perf_counter() - inicio) * 1000)
    return median(tiempos)

datos = list(range(1000))
print("Mediana en milisegundos:", medir(lambda: sum(datos)))
```

**El número concreto varía** según el equipo: no hay una salida numérica fija. Esta prueba solo enseña a medir tiempo local, **no** compara motores de bases de datos ni demuestra que un producto sea más rápido.

## 7. EXPLAIN y PROFILE de Cypher

**EXPLAIN** permite examinar el plan previsto para una consulta sin ejecutarla. **PROFILE** ejecuta la consulta y aporta medidas de ejecución.

```cypher
EXPLAIN
MATCH (l:Libro {isbn:'ISBN-001'})
RETURN l.titulo;
```

En una base de práctica puedes observar si se utiliza un índice adecuado. **Nunca ejecutes PROFILE sobre escrituras destructivas en un entorno importante sin entender su efecto**: PROFILE sí ejecuta la consulta.

## 8. Matriz de fallos del proyecto

| Fallo simulado | ¿Qué comportamiento esperar? |
|---|---|
| Tema vacío | Rechazo por validación |
| Tema inexistente | Resultado vacío y válido |
| Contraseña errónea | Error operativo, sin revelar secretos |
| Libro con ISBN duplicado | Constraint o política de calidad detecta problema |
| Fuente bibliográfica ausente | No presentar afirmación como verificada |
| Consulta lenta | Revisar plan, índices, volúmenes y red |
| Dato privado pedido por usuario sin permisos | No divulgarlo |

## 9. Ejercicios y soluciones razonadas

**E1.** Amplía el servicio para recibir un tema y un año mínimo. Prueba que rechaza años no válidos según tu política.

**E2.** Simula un fallo de base de datos con `Mock` y comprueba que no devuelve `[]`.

**E3.** Diseña una política para registrar errores sin exponer credenciales.

**E4.** Compara dos consultas con `EXPLAIN`. Explica qué diferencias en los planes podrían afectar a la ejecución.

**E5.** Define una prueba que no pueda resolverse con un mock: necesita una base Neo4j real y comprobar que una restricción de unicidad impide duplicados.

### Soluciones orientativas

**E2:** configura `repo.buscar_por_tema.side_effect = ConnectionError("no disponible")` y utiliza `pytest.raises(ConnectionError)`. Esto comprueba que el error no se oculta.

**E3:** registra identificadores de operación, causa y tiempo; evita volcar variables de entorno, respuestas privadas o tokens.

**E5:** crea una instancia aislada de pruebas, ejecuta dos escrituras con el mismo ISBN y verifica el error bajo la constraint. La suite actual de mocks no sustituye esta integración.

## 10. Comprobación de autonomía

Recibe una pequeña API y añade una prueba unitaria, una prueba negativa, un plan para prueba de integración y un informe de medición donde separe latencia local, de red y de base. Debes explicar el límite de cada evidencia.

**Siguiente:** [semana 24 — entrega profesional](semana-24.md).

## Referencias oficiales

- [pytest — documentación](https://docs.pytest.org/)
- [Neo4j Query Tuning](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/query-tuning/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

**Estado:** ejemplos educativos de tests y métricas; falta conectar una suite de integración Neo4j y un despliegue seguro reales.
