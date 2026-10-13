# Semana 13 — OWL 2: axiomas, inferencia y límites

**Objetivo:** distinguir afirmaciones explícitas, inferencias de un razonador y validaciones de datos.

## 1. Razonar no es consultar

Una consulta puede encontrar triples declarados, mientras que un **razonador** puede derivar consecuencias lógicas de ciertos axiomas.

Ejemplo:

\`\`\`turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Libro a owl:Class .
ex:LibroDigital a owl:Class ; rdfs:subClassOf ex:Libro .
ex:libro001 a ex:LibroDigital .
\`\`\`

Bajo semántica RDFS/OWL, \`ex:libro001 a ex:Libro\` es una **consecuencia lógica**. No todos los almacenes materializan inferencias automáticamente.

## 2. Propiedades inversas

\`\`\`turtle
ex:escritoPor a owl:ObjectProperty .
ex:escribio a owl:ObjectProperty ;
  owl:inverseOf ex:escritoPor .
ex:libro001 ex:escritoPor ex:autor001 .
\`\`\`

Un razonador compatible puede inferir \`ex:autor001 ex:escribio ex:libro001\` sin almacenar físicamente el segundo triple.

## 3. Mundo abierto y axiomas existenciales

Una restricción del tipo «todos los libros tienen algún autor» **no equivale** a exigir que el campo de autor esté presente en una ficha de catálogo. Bajo mundo abierto podría existir un autor no descrito. Para requisitos de completitud, usa SHACL.

Tampoco \`rdfs:domain\` y \`rdfs:range\` sirven como claves foráneas rígidas: habitualmente inducen inferencias de tipos, no errores de validación.

## 4. Axiomas que debes conocer

- \`owl:equivalentClass\`: equivalencia de clases.
- \`owl:disjointWith\`: incompatibilidad entre extensiones de clases.
- \`owl:inverseOf\`: propiedad inversa.
- \`owl:TransitiveProperty\`: transitividad.
- \`owl:FunctionalProperty\`: como máximo un valor bajo determinadas interpretaciones; **no** implica dato obligatorio.
- \`owl:sameAs\`: identidad entre individuos, afirmación muy fuerte.

## 5. Práctica guiada

1. Crea \`LibroDigital rdfs:subClassOf Libro\`.
2. Declara un individuo solo como \`LibroDigital\`.
3. Anota qué consecuencias esperarías de un razonador RDFS/OWL.
4. Añade \`escribio owl:inverseOf escritoPor\`.
5. Compara triples almacenados con triples inferidos, sin presuponer que el motor de consultas hará inferencias solo.

### Caso de análisis

Si las clases \`LibroFisico\` y \`LibroDigital\` se declaran disjuntas, asignar ambas a un mismo individuo genera una **inconsistencia lógica** en un contexto OWL adecuado. Antes de declarar clases disjuntas piensa si los casos mixtos son posibles en el dominio.

## 6. Ejercicios

- ¿Por qué no usarías \`owl:sameAs\` solo por tener el mismo título?
- ¿Qué diferencia hay entre dos clases equivalentes y dos individuos idénticos?
- ¿Qué cambia si no se ejecuta razonamiento?
- ¿Qué error conceptual hay en decir «OWL valida que cada libro tenga ISBN»?

## Fuentes

- [OWL 2 Primer — W3C](https://www.w3.org/TR/owl2-primer/)
- [OWL 2 Structural Specification](https://www.w3.org/TR/owl2-syntax/)
