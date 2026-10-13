# Semana 12 — SKOS, RDF y consultas SPARQL

![Capas semánticas](../assets/capas-semanticas.svg)

**Prerrequisitos:** semana 11. **Objetivo:** construir un vocabulario de temas y consultarlo en RDF.

## 1. ¿Por qué SKOS y no solo OWL?

SKOS está diseñado para tesauros, taxonomías y vocabularios de conceptos. Un tema bibliográfico como «Teoría de grafos» se puede representar como \`skos:Concept\` sin asumir que sea una clase lógica OWL. Una ontología formal es útil si necesitamos axiomas e inferencias; un vocabulario SKOS puede ser suficiente para clasificar libros.

| Elemento | Uso |
|---|---|
| \`skos:Concept\` | Identificar un concepto |
| \`skos:ConceptScheme\` | Agrupar conceptos en un esquema |
| \`skos:prefLabel\` | Etiqueta preferida por idioma |
| \`skos:altLabel\` | Etiquetas alternativas |
| \`skos:broader\` | Concepto jerárquicamente más amplio |
| \`skos:related\` | Asociación semántica |
| \`skos:definition\` | Definición textual |

La relación \`skos:broader\` **no es** equivalente a \`rdfs:subClassOf\`.

## 2. Primer dataset Turtle

Guarda el contenido en \`ejemplos/ontologias/temas.ttl\` (incluido en el repositorio):

\`\`\`turtle
@prefix ex: <https://example.org/temas/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

ex:esquema a skos:ConceptScheme ;
  skos:prefLabel "Temas de la biblioteca"@es .

ex:ciencia a skos:Concept ;
  skos:inScheme ex:esquema ;
  skos:prefLabel "Ciencia"@es .

ex:grafos a skos:Concept ;
  skos:inScheme ex:esquema ;
  skos:prefLabel "Teoría de grafos"@es ;
  skos:altLabel "Grafos"@es ;
  skos:broader ex:ciencia ;
  skos:definition "Estudio de estructuras formadas por vértices y aristas."@es .
\`\`\`

**Identificadores:** se utiliza \`example.org\` únicamente como espacio de nombres ficticio. En un sistema real necesitarías una política de IRIs persistentes bajo un dominio controlado.

## 3. SPARQL: selección y filtros de idioma

\`\`\`sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?concepto ?etiqueta
WHERE {
  ?concepto a skos:Concept ;
            skos:prefLabel ?etiqueta .
  FILTER(lang(?etiqueta) = "es")
}
ORDER BY ?etiqueta
\`\`\`

Buscar relaciones jerárquicas **declaradas directamente**:

\`\`\`sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?concepto ?padre
WHERE { ?concepto skos:broader ?padre }
\`\`\`

La consulta anterior no calcula automáticamente todos los ancestros; para un recorrido de uno o más enlaces directos puedes escribir el camino de propiedades \`skos:broader+\`.

## 4. Laboratorio Python con RDFLib

\`\`\`bash
python -m pip install "rdflib>=7,<8"
\`\`\`

\`\`\`python
from rdflib import Graph
g = Graph()
g.parse("ejemplos/ontologias/temas.ttl", format="turtle")
for fila in g.query("""
 PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
 SELECT ?concepto ?nombre
 WHERE { ?concepto skos:prefLabel ?nombre
         FILTER(lang(?nombre) = "es") }
"""):
    print(fila.concepto, fila.nombre)
\`\`\`

## 5. Ejercicios

1. Añade el tema «Bases de datos» y una etiqueta alternativa en español.
2. Crea una jerarquía de tres niveles. Consulta solo padres directos y después todos los ancestros con un camino de propiedades.
3. Define un término preferido español y otro inglés para el mismo concepto.
4. Explica por qué «Grafo» y «Base de datos de grafos» no deben fusionarse por compartir palabras.
5. Prueba un recurso sin \`skos:prefLabel\`; ¿el parser falla? ¿Qué otro estándar usarías para exigirlo?

**Solución razonada (5):** RDF admite datos incompletos; para comprobar etiquetas obligatorias necesitamos reglas de validación como SHACL, no solo un parser Turtle.

## Lecturas oficiales

- [SKOS Reference — W3C](https://www.w3.org/TR/skos-reference/)
- [SKOS Primer — W3C](https://www.w3.org/TR/skos-primer/)
- [SPARQL 1.1 Query Language — W3C](https://www.w3.org/TR/sparql11-query/)
- [RDFLib](https://rdflib.readthedocs.io/)
