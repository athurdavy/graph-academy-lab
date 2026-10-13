# Semana 12 — SKOS y SPARQL: crea un vocabulario y aprende a consultarlo

![RDF, SKOS, OWL y SHACL tienen funciones diferentes](../assets/capas-semanticas.svg)

**Prerrequisitos:** [semana 11](semana-11.md), comprender qué son los triples RDF, una IRI y un literal. **Objetivo:** representar materias bibliográficas en SKOS, consultarlas con SPARQL desde Python y entender qué significa realmente una jerarquía de conceptos.

## 1. El problema que queremos resolver

Una biblioteca ficticia clasifica sus libros por tema. Un lector busca «grafos», otro escribe «teoría de grafos» y otro «graph theory».

¿Tenemos tres temas diferentes? No necesariamente: podríamos tratar esas expresiones como **etiquetas diferentes de un mismo concepto**.

Además, «Teoría de grafos» pertenece a una rama general llamada «Ciencia». Queremos representar esa relación sin afirmar que toda materia de Ciencia es una instancia o subclase OWL.

Para esto utilizamos **SKOS**.

## 2. SKOS: significado de las siglas

**SKOS** viene de *Simple Knowledge Organization System*, en español «sistema simple de organización del conocimiento». Es una recomendación del W3C para representar **conceptos** organizados en vocabularios, taxonomías o tesauros.

Las piezas fundamentales son:

| Término SKOS | Qué significa | Ejemplo |
|---|---|---|
| `skos:Concept` | Un concepto de clasificación | Teoría de grafos |
| `skos:ConceptScheme` | Un esquema que organiza conceptos | Temas de biblioteca |
| `skos:prefLabel` | Etiqueta preferida en un idioma | «Teoría de grafos»@es |
| `skos:altLabel` | Etiqueta alternativa | «Grafos»@es |
| `skos:broader` | Concepto más general | Grafos → Ciencia |
| `skos:narrower` | Concepto más específico | Ciencia → Grafos |
| `skos:related` | Concepto relacionado no jerárquicamente | Grafos ↔ Redes |
| `skos:definition` | Definición textual | «Estructuras con vértices y aristas» |

**Una aclaración importante:** `skos:broader` vincula conceptos de organización temática. No es lo mismo que `rdfs:subClassOf`, que conecta clases con semántica lógica de subclases.

## 3. Escribe el vocabulario en Turtle

Turtle es una forma textual de representar triples RDF. El fichero de nuestro repositorio es [temas.ttl](../ejemplos/ontologias/temas.ttl).

```turtle
@prefix ex: <https://example.org/temas/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

ex:esquema a skos:ConceptScheme ;
  skos:prefLabel "Temas de biblioteca"@es .

ex:ciencia a skos:Concept ;
  skos:inScheme ex:esquema ;
  skos:prefLabel "Ciencia"@es .

ex:grafos a skos:Concept ;
  skos:inScheme ex:esquema ;
  skos:prefLabel "Teoría de grafos"@es ;
  skos:altLabel "Grafos"@es ;
  skos:broader ex:ciencia .
```

### Lee el ejemplo sin saltarte nada

- `ex:esquema` es el recurso que representa el vocabulario.
- `a skos:ConceptScheme` equivale en Turtle a usar el predicado RDF `rdf:type` con la clase `skos:ConceptScheme`.
- `skos:inScheme` relaciona cada concepto con el esquema al que pertenece.
- `prefLabel` proporciona el nombre preferido.
- `altLabel` aporta una etiqueta alternativa.
- `broader` afirma que Ciencia es más general que Teoría de grafos.

**Regla de calidad importante:** SKOS impone integridad sobre etiquetas, como que un concepto no tenga dos etiquetas preferidas en el mismo idioma bajo la semántica especificada. Eso no significa que un parser Turtle rechace automáticamente cualquier incumplimiento. Para comprobar calidad de datos de forma operativa pueden diseñarse validaciones específicas.

## 4. SPARQL: el lenguaje para preguntar a RDF

**SPARQL** es un nombre del estándar de consultas de RDF, expandido habitualmente como *SPARQL Protocol and RDF Query Language*. No es Cypher: SPARQL consulta **patrones de triples RDF**, mientras Cypher se utiliza fundamentalmente para patrones de grafos de propiedades.

Primera consulta:

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concepto ?nombre
WHERE {
  ?concepto a skos:Concept ;
            skos:prefLabel ?nombre .
  FILTER(LANG(?nombre) = "es")
}
ORDER BY ?nombre
```

Descompongámosla:

1. `PREFIX` define la abreviatura del vocabulario SKOS.
2. `SELECT` elige qué variables devolver.
3. El signo `?` identifica una variable de consulta, no un valor conocido.
4. `WHERE` especifica qué triples necesitamos que existan.
5. `FILTER` permite exigir condiciones adicionales.
6. `LANG(?nombre)` recupera el idioma de un literal RDF.
7. `ORDER BY` ordena las filas resultantes.

**Esperado con los datos iniciales:**

| concepto | nombre |
|---|---|
| ex:ciencia | Ciencia |
| ex:grafos | Teoría de grafos |

No verás «Grafos» en esta consulta porque es una **etiqueta alternativa**, no la etiqueta preferida. Si quieres buscar también alternativas, tendrás que formular otra consulta.

## 5. Buscar etiquetas alternativas

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?concepto ?alternativa
WHERE {
  ?concepto skos:altLabel ?alternativa .
}
```

Con nuestros datos devuelve el concepto `ex:grafos` y la etiqueta alternativa «Grafos». No devuelve automáticamente los sinónimos de todos los idiomas: solo las afirmaciones presentes.

### ¿Cómo incluir datos opcionales?

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?concepto ?preferida ?alternativa
WHERE {
  ?concepto skos:prefLabel ?preferida .
  FILTER(LANG(?preferida) = "es")
  OPTIONAL {
    ?concepto skos:altLabel ?alternativa .
    FILTER(LANG(?alternativa) = "es")
  }
}
ORDER BY ?preferida
```

`OPTIONAL` deja que un concepto sin etiqueta alternativa siga apareciendo; la variable alternativa quedará sin valor en esa fila. Esto se parece conceptualmente a un LEFT JOIN, pero se construye a partir de patrones RDF.

## 6. Jerarquía: relaciones directas y caminos

Pregunta: «¿de qué tema general depende Teoría de grafos?»

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?concepto ?general
WHERE {
  ?concepto skos:broader ?general .
}
```

Resultado esperado: `ex:grafos → ex:ciencia`.

Si añadimos un nivel:

```turtle
ex:matematicas a skos:Concept ;
  skos:prefLabel "Matemáticas"@es ;
  skos:broader ex:ciencia .
ex:grafos skos:broader ex:matematicas .
```

**Cuidado:** en una práctica real retirarías la afirmación directa `ex:grafos skos:broader ex:ciencia` si deseas que Grafos dependa *solo directamente* de Matemáticas. De otro modo tendrás dos padres directos.

Ahora el camino jerárquico es Grafos → Matemáticas → Ciencia.

Con **property paths** (caminos de propiedades) de SPARQL 1.1 puedes preguntar por todos los ancestros accesibles con una o más aristas `skos:broader`:

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT DISTINCT ?ancestro
WHERE {
  <https://example.org/temas/grafos> skos:broader+ ?ancestro .
}
```

El signo `+` significa aquí **una o más repeticiones de la relación**. No es el operador de suma aritmética. No estamos declarando nuevas relaciones en el archivo RDF: estamos **consultando caminos**.

## 7. Práctica Python: RDFLib y SPARQL

**RDFLib** es una librería de Python para crear, leer, serializar y consultar RDF. Ejecuta desde la raíz del proyecto:

```bash
python -m pip install -r laboratorios/requirements.txt
```

Prueba:

```python
from rdflib import Graph

g = Graph()
g.parse("ejemplos/ontologias/temas.ttl", format="turtle")

consulta = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?concepto ?nombre WHERE {
  ?concepto a skos:Concept ;
            skos:prefLabel ?nombre .
  FILTER(LANG(?nombre) = "es")
}
ORDER BY ?nombre
"""

for fila in g.query(consulta):
    print(fila.nombre)
```

**Salida esperada:**

```text
Ciencia
Teoría de grafos
```

No has necesitado GraphDB porque RDFLib puede consultar este conjunto pequeño **en memoria**. Eso no significa que RDFLib tenga todas las capacidades operativas de un motor RDF empresarial o soporte razonamiento OWL completo automáticamente.

## 8. SPARQL SELECT frente a CONSTRUCT

`SELECT` devuelve filas de variables. `CONSTRUCT` devuelve **triples RDF construidos mediante una plantilla**.

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX ex: <https://example.org/temas/>

CONSTRUCT {
  ?concepto ex:nombrePublico ?etiqueta .
}
WHERE {
  ?concepto skos:prefLabel ?etiqueta .
  FILTER(LANG(?etiqueta) = "es")
}
```

Aquí no hemos modificado la base: construimos un grafo de resultados con la propiedad ficticia `ex:nombrePublico`. Es útil al transformar datos para exportar o integrar sistemas.

## 9. Errores comunes y por qué suceden

| Error | Motivo | Corrección |
|---|---|---|
| Confundir `skos:broader` y `rdfs:subClassOf` | Jerarquía temática no es herencia lógica | Identificar primero si modelas conceptos o clases |
| Usar `prefLabel` para todas las variantes | Las alternativas tienen su propia propiedad | Utilizar `altLabel` para sinónimos pertinentes |
| Esperar que SPARQL encuentre datos no declarados | Falta de triples o de inferencia configurada | Inspeccionar el grafo y el régimen de inferencia |
| Confundir `SELECT` con una actualización | SELECT solo consulta | Estudiar SPARQL UPDATE cuando corresponda |
| Creer que un `broader+` escribe nuevos triples | Property paths consultan caminos | Diferenciar consulta y materialización |

## 10. Ejercicios con soluciones comentadas

**Ejercicio A.** Agrega el concepto «Bases de datos» y una etiqueta alternativa «BD» en español.

**Ejercicio B.** Consulta todas las etiquetas alternativas, mostrando IRI y texto.

**Ejercicio C.** Añade una jerarquía de tres niveles. Consulta padres directos y todos los ancestros.

**Ejercicio D.** Explica la diferencia entre un concepto sin etiqueta alternativa y un concepto que no aparece en una consulta que exige `skos:altLabel`.

**Ejercicio E.** Escribe un `CONSTRUCT` que produzca los nombres públicos de los conceptos.

### Pistas y soluciones

**A:**

```turtle
ex:basesdatos a skos:Concept ;
  skos:prefLabel "Bases de datos"@es ;
  skos:altLabel "BD"@es ;
  skos:broader ex:ciencia .
```

**B:** usa el patrón `?concepto skos:altLabel ?texto` dentro de `WHERE`.

**C:** usa `skos:broader` para padres directos y `skos:broader+` para recorrer uno o más niveles. El segundo patrón tiene significado **consultivo**; no inserta triples.

**D:** no aparecer no significa que una etiqueta alternativa esté prohibida ni que el concepto sea inválido; puede no haberse declarado todavía.

## 11. Autoevaluación

Antes de pasar a la siguiente clase debes poder explicar, **sin mirar**: concepto, esquema de conceptos, etiqueta preferida, etiqueta alternativa, `broader`, prefijo, IRI, variable SPARQL, SELECT, FILTER, OPTIONAL y property path. Ejecuta y modifica al menos dos consultas.

**Siguiente:** [Semana 13 — axiomas e inferencias OWL](semana-13.md).

## Fuentes oficiales

- [SKOS Primer — W3C](https://www.w3.org/TR/skos-primer/)
- [SKOS Reference — W3C](https://www.w3.org/TR/skos-reference/)
- [SPARQL 1.1 Query — W3C](https://www.w3.org/TR/sparql11-query/)
- [RDFLib — documentación](https://rdflib.readthedocs.io/)
