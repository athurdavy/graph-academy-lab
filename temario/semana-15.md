# Semana 15 — Calidad de datos: detectar errores antes de confiar en un grafo

**Antes:** [semana 14, validar RDF con SHACL](semana-14.md). **Después:** [semana 16, procedencia y versionado](semana-16.md). Duración aproximada: 8–12 horas. **Objetivo:** distinguir un error de formato de un hecho falso, construir un auditor con Python y explicar qué reglas pueden automatizarse.

## 1. El problema: una consulta correcta puede devolver un dato incorrecto

Tenemos una biblioteca ficticia. El catálogo afirma que Marina Soler escribió el libro ISBN-001. Si esa relación fue introducida por error, Cypher la devolverá igualmente. La base de datos puede estar funcionando perfectamente y el dato ser falso.

**Calidad de datos** significa comprobar características medibles de un conjunto de datos respecto a necesidades y reglas concretas. No significa que los datos sean automáticamente verdaderos.

Imagina estos registros:

| ISBN | Título | Año |
|---|---|---|
| ISBN-001 | El mapa de los grafos | 2022 |
| ISBN-001 | Otro libro | 2024 |
| *(vacío)* | *(vacío)* | desconocido |

Encontramos distintos problemas: ISBN duplicado, valores obligatorios ausentes y año con formato inadecuado. **No debemos arreglarlos borrando filas sin investigar.**

## 2. Cinco términos que usaremos

| Término | Significado práctico | Comprobación |
|---|---|---|
| Completitud | Tener los valores requeridos para el caso de uso | Libro con título e ISBN |
| Unicidad | Evitar duplicaciones según una clave definida | ISBN no repetido |
| Consistencia | Cumplir reglas coherentes del modelo | ESCRIBIO conecta Autor y Libro |
| Validez | Respetar un formato o rango esperado | Año expresado como entero |
| Procedencia | Conocer origen y transformaciones del dato | Ficha que respalda la autoría |

**Importante:** la regla de rango de año de este laboratorio (1450–2100) es **una decisión didáctica**, no una ley universal para bibliotecas. Debes documentar todas las reglas.

## 3. Primer laboratorio real con Python

Hemos incorporado un programa que revisa estas reglas **sin base de datos y sin modificar datos**:

```bash
python laboratorios/calidad_catalogo.py
python -m pytest laboratorios/tests/test_calidad_catalogo.py -q
```

Lee su [código Python](../laboratorios/calidad_catalogo.py) y las [seis pruebas](../laboratorios/tests/test_calidad_catalogo.py) después de comprender el ejercicio.

Una parte esencial es esta:

```python
from collections import Counter

def comprobar_isbns(registros):
    isbns = [str(fila.get("isbn", "") or "").strip() for fila in registros]
    frecuencia = Counter(isbn for isbn in isbns if isbn)
    return [isbn for isbn, veces in frecuencia.items() if veces > 1]
```

**Línea por línea:**

- `fila.get("isbn", "")` obtiene un valor, incluso si falta la clave del diccionario.
- `or ""` trata un valor nulo como cadena vacía.
- `str(...)` lo convierte a texto y `strip()` elimina espacios laterales.
- `Counter` cuenta cuántas veces aparece cada ISBN.
- `if veces > 1` devuelve solo los identificadores repetidos.

**Resultado esperado** sobre el ejemplo de la primera tabla: `["ISBN-001"]`. El programa completo además identifica filas y otros problemas.

### ¿Por qué no borramos duplicados automáticamente?

Puede haber un error de importación, pero también dos ediciones distintas mal identificadas o una clave que no represente la entidad que creemos. Una limpieza irreversible puede destruir datos y relaciones correctas.

## 4. Auditar el caso correcto y el caso incorrecto

El laboratorio incluye `REGISTROS_VALIDOS` y `REGISTROS_CON_PROBLEMAS`.

Con los registros correctos devuelve **ninguna incidencia** según las reglas configuradas.

Con los registros erróneos debe informar de:

1. ISBN-001 duplicado en las filas 1 y 2.
2. ISBN ausente en la fila 3.
3. Título ausente en la fila 3.
4. Año inválido en la fila 3.

**No confundas seis incidencias con seis registros malos:** varias reglas pueden fallar en un mismo registro. Se informan incidencias, no necesariamente filas únicas.

## 5. Lleva la idea a Cypher

Si ya tienes un Neo4j con la biblioteca cargada, busca ISBN duplicados:

```cypher
MATCH (l:Libro)
WHERE l.isbn IS NOT NULL
WITH l.isbn AS isbn, count(l) AS total
WHERE total > 1
RETURN isbn, total;
```

**Esperado con el dataset limpio y las constraints correctas:** ninguna fila.

Si en una base existen duplicados antes de crear la constraint, la creación de esta puede fallar. Por tanto, **audita antes de imponer reglas**, y nunca practiques operaciones destructivas en una instancia con datos importantes.

Para buscar nodos Libro sin título:

```cypher
MATCH (l:Libro)
WHERE l.titulo IS NULL OR trim(l.titulo) = ''
RETURN l.isbn AS isbn;
```

**Matiz:** si existen datos donde `titulo` no sea cadena de texto, diseña primero cómo vas a tratar ese caso. Las consultas de ejemplo suponen los tipos del dataset ficticio.

## 6. Ahora SHACL: por qué otro mecanismo de validación

Cypher y las restricciones del motor sirven para comprobar ciertas condiciones del grafo de propiedades. Cuando publicas **RDF**, puedes expresar reglas con **SHACL**, que significa *Shapes Constraint Language*.

La [semana 14](semana-14.md) enseña una forma que exige título e ISBN y un test negativo donde borramos un título en memoria.

**No son procedimientos idénticos:**

- Una constraint de Neo4j puede impedir una escritura duplicada según reglas y edición.
- Una consulta de auditoría detecta anomalías que ya existen.
- SHACL genera un informe de conformidad para objetivos y condiciones RDF definidos.

Los tres aportan mecanismos complementarios, pero ninguno comprueba por sí solo si una afirmación bibliográfica es verdadera.

## 7. Diseña una política de calidad operativa

No basta con ejecutar el script una vez. Especifica:

- **Entrada:** de dónde llegan los registros y cuál es su contrato de datos.
- **Reglas:** versión de la política y explicación de cada requisito.
- **Resultado:** lista de incidencias con fila, código y detalle.
- **Decisión:** aceptar, rechazar o enviar una fila a revisión según gravedad.
- **Trazabilidad:** quién revisó el caso y cuál fue la fuente consultada.
- **Reevaluación:** ejecutar de nuevo las reglas tras corregir los datos.

Ejemplo: «ISBN vacío» puede ser motivo para rechazar una carga; «título inusual» podría requerir revisión humana. Estas decisiones dependen del dominio, no de una fórmula universal.

## 8. Ejercicios progresivos

**Nivel inicial:** ejecuta el laboratorio con registros correctos y predice el número de incidencias.

**Nivel intermedio:** añade otro registro con ISBN repetido y explica por qué aparecen avisos en todas las filas que contienen ese valor.

**Nivel intermedio:** conserva dos libros de igual título, pero con ISBN distintos. ¿Deben marcarse duplicados? Explica por qué el programa no lo hace.

**Nivel avanzado:** añade una regla que verifique la presencia de autor en el *modelo de grafo*, no solo una columna. Define qué hará el sistema cuando la autoría no esté confirmada.

**Nivel avanzado:** prepara una entrada con 10 filas problemáticas y documenta las incidencias, decisiones y efectos de la corrección.

### Soluciones comentadas

**Duplicados:** se agrupan por ISBN normalizado mediante el conjunto de reglas del laboratorio. El título no participa en la identidad, porque títulos iguales no demuestran duplicación.

**Dos títulos iguales:** no deben producir por sí solos una incidencia de ISBN repetido; eso sería confundir un atributo descriptivo con una clave estable.

**Autoría desconocida:** no inventes una relación ESCRIBIO. Puedes señalar «pendiente de verificación» sin afirmar que el libro carece de autor en la realidad.

## 9. Comprobación de autonomía

Diseña tres reglas nuevas, escribe un test donde cada una falle y otro donde pase, demuestra que el auditor **no modifica los datos** y justifica qué acciones se automatizan y cuáles requieren revisión.

**Siguiente:** [semana 16 — procedencia y control de cambios](semana-16.md).

## Fuentes

- [Neo4j constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/)
- [SHACL — W3C](https://www.w3.org/TR/shacl/)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)

**Estado de verificación:** código y pruebas unitarias incorporados; aún falta confirmar su ejecución en GitHub Actions y contrastar todo el laboratorio en un entorno Neo4j real.
