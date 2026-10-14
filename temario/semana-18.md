# Semana 18 — Crear un grafo de conocimiento desde cero y comprobar sus fuentes

**Antes:** [semana 01](semana-01.md), [semana 03](semana-03.md), [semana 11](semana-11.md) y [semana 16](semana-16.md). **Después:** [semana 19, extracción de entidades](semana-19.md). Tiempo: 8–12 horas. **Objetivo:** diseñar un pequeño grafo de conocimiento con identidad y procedencia, consultarlo y detectar afirmaciones no respaldadas.

## 1. El problema antes de la tecnología

Tenemos una biblioteca ficticia. Una ficha afirma que **Marina Soler escribió El mapa de los grafos**. Otro documento menciona «Marina Soler», pero no especifica su identificador. ¿Tenemos dos menciones de la misma persona? **No lo sabemos aún.** Coincidir en el nombre no demuestra identidad.

Un **grafo de conocimiento** representa entidades y afirmaciones conectadas, con significado e identificadores. Para construir sistemas confiables nos interesa registrar también **de dónde proviene cada afirmación**. No cualquier conjunto de flechas se convierte automáticamente en una base de conocimiento confiable.

| Palabra | Explicación | Ejemplo |
|---|---|---|
| Entidad | Algo que distinguimos de otras cosas | Libro ISBN-001 |
| Identificador | Código estable que usamos para referirnos a una entidad | A-001 |
| Afirmación | Un dato expresado como relación | A-001 escribió ISBN-001 |
| Fuente | Documento del que procede una afirmación | Ficha F-001 |
| Procedencia | Rastro de cómo se obtuvo una afirmación | Importación de F-001 |
| Reconciliación | Decidir si dos registros apuntan a una entidad común | Comparar A-001 y A-999 |

## 2. ¿Por qué no basta con Autor — ESCRIBIO — Libro?

En el catálogo podríamos guardar una relación directa:

```text
[Marina] --ESCRIBIO--> [Libro]
```

Pero un auditor pregunta: «¿qué ficha respalda esa autoría?». Si guardamos una fuente para todo el libro, no sabremos si la fuente justifica la autoría, el tema o la fecha. Por eso modelaremos una **afirmación de autoría** como entidad con vínculo a una ficha:

```text
[Afirmación C-001] --> [Autor A-001]    (sujeto)
[Afirmación C-001] --> [Libro ISBN-001] (objeto)
[Afirmación C-001] --> [Ficha F-001]    (fuente)
```

Es una opción didáctica de modelado. Existen otros métodos, entre ellos propiedades de relación, grafos nombrados RDF y vocabularios de procedencia como PROV-O. Lo importante es que sepas justificar **qué detalle necesitas rastrear**.

## 3. Construir el primer ejemplo en Python, línea por línea

Usaremos **NetworkX**, biblioteca para trabajar con grafos en memoria. No necesitas una base Neo4j para empezar.

Desde la raíz del repositorio:

```bash
python -m pip install -r laboratorios/requirements.txt
```

En un archivo llamado `conocimiento.py`:

```python
import networkx as nx

grafo = nx.DiGraph()
grafo.add_node("autor:A-001", tipo="Autor", nombre="Marina Soler")
grafo.add_node("libro:ISBN-001", tipo="Libro", titulo="El mapa de los grafos")
grafo.add_node("ficha:F-001", tipo="Fuente")
grafo.add_node("afirmacion:C-001", tipo="Afirmacion", relacion="ESCRIBIO")

grafo.add_edge("afirmacion:C-001", "autor:A-001", papel="sujeto")
grafo.add_edge("afirmacion:C-001", "libro:ISBN-001", papel="objeto")
grafo.add_edge("afirmacion:C-001", "ficha:F-001", papel="fuente")

print("Nodos:", grafo.number_of_nodes())
print("Relaciones:", grafo.number_of_edges())
```

**Salida esperada:**

```text
Nodos: 4
Relaciones: 3
```

### ¿Qué significa cada instrucción?

- `nx.DiGraph()` crea un grafo con relaciones **dirigidas**.
- `add_node` crea un elemento al que asignamos un identificador y propiedades.
- `tipo` es solo un atributo Python que hemos elegido: **no es una clase formal OWL**.
- `add_edge` conecta dos identificadores y guarda datos de esa conexión.
- `papel` describe si la conexión indica sujeto, objeto o fuente.
- `number_of_nodes` y `number_of_edges` cuentan elementos y conexiones.

**Pregunta:** ¿por qué hay cuatro nodos y tres relaciones? Porque contamos Autor, Libro, Ficha y Afirmación, conectados desde la afirmación.

## 4. Consultar y exigir una fuente

```python
def obtener_fuentes(grafo, afirmacion):
    return [
        destino
        for _, destino, atributos in grafo.out_edges(afirmacion, data=True)
        if atributos.get("papel") == "fuente"
    ]

print(obtener_fuentes(grafo, "afirmacion:C-001"))
```

**Esperado:** `['ficha:F-001']`.

`out_edges` recorre aristas salientes; `data=True` incluye atributos; la condición busca aristas cuyo papel es `fuente`.

Ahora elimina ese vínculo:

```python
grafo.remove_edge("afirmacion:C-001", "ficha:F-001")
print(obtener_fuentes(grafo, "afirmacion:C-001"))
```

**Resultado esperado:** `[]`. ¿La afirmación pasó a ser falsa? **No lo sabemos.** Solo hemos demostrado que ya no conserva una fuente registrada.

## 5. Identidad: nombres iguales no significan personas iguales

Añade:

```python
grafo.add_node("autor:A-999", tipo="Autor", nombre="Marina Soler")
```

Ahora hay dos entidades con el mismo nombre. ¿Se deben fusionar? No sin evidencia y reglas de identificación suficientes. Una fusión incorrecta puede atribuir obras a otra persona.

Una política profesional distingue **coincidencia candidata**, **identidad verificada** e **identidad descartada**. Un sistema que utiliza OWL debe ser especialmente cuidadoso con `owl:sameAs`, porque significa identidad entre individuos, no «tienen nombres parecidos».

## 6. ¿Y cómo lo representamos en RDF?

**RDF** (*Resource Description Framework*) representa afirmaciones mediante triples: sujeto, predicado y objeto. **Turtle** es un formato de escritura textual de RDF.

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix dcterms: <http://purl.org/dc/terms/> .

ex:afirmacion001 ex:sujeto ex:autor001 ;
  ex:objeto ex:libro001 ;
  ex:relacion "ESCRIBIO" ;
  dcterms:source ex:ficha001 .
```

`ex:sujeto`, `ex:objeto` y `ex:relacion` son propiedades **inventadas para el ejercicio**, no términos estándares que cualquier herramienta comprenderá automáticamente. Para interoperar hay que estudiar vocabularios como PROV-O y definir qué significan los términos propios.

**Un grafo de propiedades y RDF pueden representar hechos similares, pero no tienen automáticamente la misma semántica ni el mismo mecanismo de inferencia.**

## 7. Pruebas negativas: también debes saber cuándo NO responder

Caso A: la ficha existe pero no está conectada a ninguna afirmación. La función `obtener_fuentes` debe devolver una lista vacía.

Caso B: dos nodos Autor comparten nombre. No puedes deducir identidad usando solo igualdad textual.

Caso C: una fuente afirma que Marina «revisó» el libro, no que lo «escribió». No debes convertir la relación REVISÓ en ESCRIBIÓ.

**La ausencia de datos y la evidencia contradictoria son problemas distintos.** Diseña estados para tratarlos sin inventar conclusiones.

## 8. Ejercicios progresivos

**Nivel 1:** añade otro libro ficticio, una afirmación y una ficha. Obtén su fuente con la función anterior.

**Nivel 2:** añade un libro sin afirmación de autoría. Consulta cuáles tienen al menos una afirmación respaldada.

**Nivel 3:** registra dos fuentes para una misma afirmación y explica si deben mantenerse separadas.

**Nivel 4:** crea dos autores homónimos y documenta qué evidencia necesitarías para decidir si son la misma persona.

**Nivel 5:** diseña tres preguntas de competencia: consultas que el grafo deba responder antes de considerar válido el modelo.

### Soluciones orientativas

**Nivel 1:** replica el patrón de nodos `ficha`, `autor`, `libro` y `afirmacion` con identificadores diferentes; conecta los extremos con el papel correcto y consulta las fuentes.

**Nivel 3:** utiliza dos nodos Fuente y dos relaciones desde la misma Afirmación con `papel="fuente"`. La lista de procedencias tendrá dos elementos; no es necesario duplicar el libro ni el autor.

**Nivel 4:** nombres y títulos no son identificadores suficientes. Comprueba IDs de confianza y fuentes antes de declarar identidad.

## 9. Prueba de autonomía

Sin copiar el código, explica por qué elegiste una afirmación como nodo, cómo localizarías sus fuentes, cómo representarías una corrección y qué preguntas **no** puede responder tu sistema sin más datos.

**Siguiente:** [semana 19 — extracción de entidades](semana-19.md).

## Fuentes oficiales

- [W3C RDF Primer](https://www.w3.org/TR/rdf11-primer/)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [NetworkX DiGraph](https://networkx.org/documentation/stable/reference/classes/digraph.html)
- [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)

**Estado editorial:** ejemplo ilustrativo con salidas previstas; queda pendiente ejecutar y verificarlo con las dependencias en CI.
