# Semana 16 — Procedencia y versionado desde cero: saber de dónde viene cada afirmación

**Antes:** [semana 15, calidad de datos](semana-15.md). **Después:** [semana 17, arquitectura](semana-17.md). Tiempo: 8–12 horas. **Objetivo:** conservar los orígenes y cambios de una afirmación bibliográfica, distinguir revisión de verdad y practicar un historial inmutable en Python.

## 1. Una pregunta que no resuelve la búsqueda de libros

La biblioteca ficticia afirma:

> «El libro ISBN-001 trata sobre Grafos».

Pero alguien pregunta: «¿Quién lo clasificó así? ¿Qué ficha consultó? ¿Cuándo cambió de estado de pendiente a aceptado?».

Tener una arista `TRATA_SOBRE` solo representa la relación. No nos dice necesariamente de dónde procede. Para contestar necesitamos **procedencia**, también llamada *provenance*.

## 2. Palabras que conviene diferenciar

| Palabra | Significado | Ejemplo |
|---|---|---|
| Afirmación | Algo registrado como dato | ISBN-001 TRATA_SOBRE GRAFOS |
| Fuente | Documento o registro que la respalda | FICHA-001 |
| Revisión | Evento donde se examina una afirmación | REV-002 |
| Agente | Persona, sistema o proceso que realiza una actividad | editor-02 |
| Fecha | Cuándo se registra el evento | 2026-01-11 |
| Estado | Decisión de un flujo de trabajo | propuesta, aceptada, rechazada |
| Historial | Serie de revisiones que conservamos | REV-001 y REV-002 |
| Versión | Identificación de una edición de datos o esquema | vocabulario v2 |

**No son sinónimos:** la fecha de revisión de una ficha no es necesariamente la fecha en que se escribió el libro. Tampoco «aceptada» significa «verdadera en el mundo real».

## 3. Por qué sobrescribir un estado destruye información

Supón que guardas una sola propiedad:

```text
afirmacion.estado = "aceptada"
```

¿Cómo sabrás que el día anterior estaba `propuesta`? No podrás, salvo que tengas un sistema de auditoría independiente.

En el laboratorio guardamos dos objetos `Revision`:

```text
REV-001  propuesta  FICHA-001  editor-01  2026-01-10
REV-002  aceptada   FICHA-002  editor-02  2026-01-11
```

Ambos describen la **misma afirmación**, pero son eventos diferentes. Guardarlos en una secuencia permite reconstruir qué se registró, **no** garantizar que la revisión se hizo correctamente.

## 4. Laboratorio Python: crear revisiones

Ejecuta desde la raíz de la copia del repositorio:

```bash
python laboratorios/procedencia.py
python -m pytest laboratorios/tests/test_procedencia.py -q
```

Lee el [código completo](../laboratorios/procedencia.py), especialmente esta estructura:

```python
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
```

### Qué significa cada línea

- `@dataclass` es una ayuda estándar de Python que construye métodos para objetos de datos.
- `frozen=True` impide cambiar fácilmente los atributos de esa instancia después de crearla. **No es un sustituto de una base de datos inmutable ni de una auditoría externa.**
- `identificador` distingue un evento de otro; no usamos el nombre del revisor como ID.
- `afirmacion` guarda la clave lógica del hecho revisado.
- `fuente` apunta a la ficha que sustenta o motiva esa revisión.
- `fecha` contiene una fecha Python y no una cadena de formato arbitrario.
- `estado` representa una decisión definida por nuestro flujo.

### Crear una revisión con datos correctos

```python
from datetime import date
from laboratorios.procedencia import crear_revision

revision = crear_revision(
    identificador="REV-003",
    afirmacion="ISBN-002 TRATA_SOBRE GRAFOS",
    fuente="FICHA-003",
    revisor="editor-03",
    fecha=date(2026, 2, 1),
    estado="propuesta",
)
print(revision.estado)
```

**Resultado esperado:** `propuesta`.

Si cambias `estado="publicado"`, la función genera `ValueError` porque no forma parte de los estados permitidos. Para añadir un nuevo estado necesitarías cambiar y documentar las reglas, no aceptar cualquier cadena inesperada.

## 5. Historial sin perder eventos

```python
from datetime import date
from laboratorios.procedencia import crear_revision, historial_por_afirmacion

primera = crear_revision(
    "REV-001", "ISBN-001 TRATA_SOBRE GRAFOS",
    "FICHA-001", "editor-01", date(2026, 1, 10), "propuesta",
)
segunda = crear_revision(
    "REV-002", "ISBN-001 TRATA_SOBRE GRAFOS",
    "FICHA-002", "editor-02", date(2026, 1, 11), "aceptada",
)

for evento in historial_por_afirmacion([segunda, primera],
                                        "ISBN-001 TRATA_SOBRE GRAFOS"):
    print(evento.identificador, evento.estado)
```

**Resultado esperado:**

```text
REV-001 propuesta
REV-002 aceptada
```

El orden lo decide la fecha y, en caso de empate, el identificador. **Una fecha de calendario no tiene precisión temporal de segundos ni zona horaria**; si necesitas auditoría real, deberías registrar instantes, actores autenticados y registros resistentes a alteraciones.

## 6. ¿Qué es PROV-O?

**PROV-O** significa *PROV Ontology*, una ontología W3C para describir procedencia de entidades, actividades y agentes.

En términos sencillos:

- **Entidad:** algo de lo que guardamos información, como un documento.
- **Actividad:** un proceso que produce o usa entidades, como una revisión.
- **Agente:** una persona o sistema responsable de la actividad.

Ejemplo simplificado en Turtle:

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix prov: <http://www.w3.org/ns/prov#> .

ex:revision001 a prov:Activity ;
  prov:wasAssociatedWith ex:editor01 ;
  prov:used ex:ficha001 .

ex:editor01 a prov:Agent .
ex:ficha001 a prov:Entity .
```

**Lee las flechas semánticas:** el evento de revisión es una actividad; el agente editor está asociado a ella; la actividad utilizó una ficha.

No afirmamos que estos tres triples sean un historial de auditoría completo. Se necesitaría modelar resultados, fechas, integridad, permisos y un repositorio real.

## 7. Versionar datos y versionar ontologías no es lo mismo

Si cambias un título bibliográfico, actualizas **datos**. Si cambias el significado de una propiedad o eliminas una clase, cambias el **esquema o la ontología** y puedes afectar a otros sistemas.

Antes de publicar una nueva versión, documenta:

1. Qué afirmaciones cambiaron.
2. Qué identificadores siguen estables.
3. Qué reglas de validación o inferencia pueden cambiar.
4. Qué aplicaciones dependen de los términos.
5. Cómo migrar o mantener compatibilidad.

No cambies arbitrariamente una IRI pública sin una estrategia: otros consumidores podrían usarla para identificar exactamente el mismo recurso.

## 8. Ejercicios por niveles

1. Crea una revisión en estado propuesta y explica qué datos contiene.
2. Crea una segunda revisión aceptada sin sobrescribir la anterior.
3. Intenta crear una revisión sin fuente. Comprueba qué excepción aparece.
4. Intenta un estado no permitido y explica el rechazo.
5. Crea revisiones de dos afirmaciones distintas y comprueba que el historial no las mezcla.
6. Diseña cómo guardarías dos fuentes contradictorias sin inventar una conclusión.
7. Explica cuándo es pertinente una estructura `prov:Activity` y cuándo basta una ficha descriptiva.

### Soluciones comentadas

**2.** Utiliza un nuevo identificador de evento. No mutas el objeto de la revisión anterior.

**3.** El laboratorio lanza `ValueError` ante una fuente vacía, porque su contrato exige procedencia explícita.

**5.** La función `historial_por_afirmacion` filtra primero por la clave del hecho revisado. Tener el mismo revisor o fuente no convierte dos afirmaciones en la misma.

**6.** Conserva las dos fuentes y el estado de conflicto; un algoritmo no debe decidir por intuición cuál es correcta.

## 9. Comprobación de autonomía

Diseña un registro de revisiones para tres afirmaciones ficticias: una aceptada, otra pendiente y una conflictiva. Consulta el historial y escribe al menos dos pruebas de error. Explica por qué conservar revisiones **no garantiza por sí mismo** integridad, inmutabilidad de un servidor ni verdad bibliográfica.

**Siguiente:** [semana 17 — conectar servicios y motores](semana-17.md).

## Fuentes oficiales

- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/)
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html)

**Estado:** laboratorio y pruebas unitarias publicados; integración con un repositorio persistente y verificación de auditoría inmutable todavía pendientes.
