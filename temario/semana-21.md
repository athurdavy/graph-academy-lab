# Semana 21 — GraphRAG desde cero: recuperar evidencia antes de responder

**Antes:** [semana 18, grafo con procedencia](semana-18.md), [semana 19, extracción](semana-19.md) y [semana 20, recuperación](semana-20.md). **Objetivo:** entender un sistema de generación con recuperación, construir un prototipo de recuperación trazable sin servicios externos y evaluar cuándo debe responder «no lo sé».

## 1. El problema: un chatbot no es una fuente fiable por sí solo

Una persona pregunta a la biblioteca ficticia:

> «¿Qué libros de Marina Soler tratan sobre grafos y qué fuentes lo respaldan?»

Un modelo generativo podría producir una respuesta convincente **sin consultar** el catálogo. Si inventa un título o una autoría, tenemos una **alucinación**: una afirmación de apariencia plausible que no está respaldada por las fuentes disponibles.

Queremos que la aplicación encuentre datos concretos en el catálogo y los adjunte como contexto antes de responder.

## 2. Primero RAG, después GraphRAG: qué significa cada nombre

**LLM** significa *Large Language Model*, modelo de lenguaje grande. Es un modelo que procesa y genera texto; no garantiza por sí solo que una afirmación sea verdadera.

**RAG** significa *Retrieval-Augmented Generation*, generación aumentada mediante recuperación. Su idea general:

1. El usuario pregunta.
2. El sistema busca fragmentos o datos relevantes en una fuente.
3. Envía los fragmentos recuperados como contexto al modelo.
4. El modelo produce una respuesta basada en ese contexto.
5. El sistema puede mostrar referencias, aunque debe comprobar si realmente apoyan la respuesta.

**GraphRAG** es una familia de técnicas que utilizan información estructurada como grafos durante la recuperación y/o generación. No describe un único algoritmo ni una API universal. Algunas implementaciones exploran relaciones de entidades; otras crean comunidades o resúmenes de grafos.

No necesitas comprar nada para comprender el flujo. Primero practicaremos **recuperación y evidencias sin LLM**.

## 3. Dibujemos el flujo de la biblioteca

```text
PREGUNTA DEL LECTOR
    |
    v
Extraer autor y tema solicitados
    |
    v
Buscar en el grafo:
Autor --ESCRIBIO--> Libro --TRATA_SOBRE--> Tema
    |
    v
Recuperar títulos y fuentes concretas
    |
    v
Comprobar que el resultado responde a la pregunta
    |
    v
Redactar una respuesta CON referencias
    |
    v
Si no hay evidencia: «No tengo datos suficientes»
```

La recuperación tiene que respetar el **significado de las relaciones**. Si solo buscamos nodos cercanos y encontramos un lector conectado con el libro, no podemos transformarlo en su autor.

## 4. Primer prototipo en Python: recuperar sin inventar

Utilizaremos un conjunto muy pequeño de datos ficticios. No necesitamos API externa ni vector DB:

```python
catalogo = [
    {"autor": "Marina Soler", "titulo": "El mapa de los grafos",
     "tema": "GRAFOS", "fuente": "F-001"},
    {"autor": "Marina Soler", "titulo": "Rutas de conocimiento",
     "tema": "GRAFOS", "fuente": "F-002"},
    {"autor": "Diego Ríos", "titulo": "Historias del océano",
     "tema": "NATURALEZA", "fuente": "F-003"},
]

def recuperar(catalogo, autor, tema):
    return [
        fila for fila in catalogo
        if fila["autor"] == autor and fila["tema"] == tema
        and fila.get("fuente")
    ]

resultado = recuperar(catalogo, "Marina Soler", "GRAFOS")
for fila in resultado:
    print(f'{fila["titulo"]} — fuente {fila["fuente"]}')
```

**Salida esperada:**

```text
El mapa de los grafos — fuente F-001
Rutas de conocimiento — fuente F-002
```

### Entiende cada línea

- `catalogo` contiene información ficticia estructurada que simulamos haber recuperado del grafo.
- `recuperar` filtra por autor y tema; en un sistema real usarías Cypher o SPARQL para localizar las relaciones.
- `fila.get("fuente")` evita devolver hechos sin una referencia registrada, según **nuestra política de laboratorio**.
- El resultado muestra el dato y el identificador de la fuente.

**Límite:** `F-001` es solo un ID ficticio. No sirve como cita verificable para el público mientras no haya un documento concreto asociado. Una fuente no es fiable solo por existir.

## 5. Convertir resultados en contexto para un modelo

Un paso habitual consiste en crear un contexto delimitado que contenga únicamente los resultados respaldados:

```python
contexto = "\n".join(
    f'Título: {fila["titulo"]}; fuente: {fila["fuente"]}'
    for fila in resultado
)
print(contexto)
```

El programa podría enviar ese contexto a un modelo de lenguaje. **No necesitas hacerlo aún** para comprender la idea: la recuperación y la evidencia deben poder evaluarse *antes* de generar texto.

### Dos riesgos importantes

1. **Información falsa en la fuente:** un modelo puede repetir una autoría incorrecta aunque cite bien una ficha. Necesitas gobernanza de fuentes.
2. **Instrucciones dentro de documentos:** un documento recuperado es contenido de datos, no instrucciones confiables para la aplicación. Un sistema real debe evitar que textos de terceros controlen su comportamiento.

## 6. La respuesta correcta a veces es «no sé»

Busca un autor inexistente:

```python
sin_resultados = recuperar(catalogo, "Elena Vidal", "GRAFOS")
print(sin_resultados)
```

**Esperado:** `[]`.

Una aplicación responsable debería responder algo como:

> No encuentro en este catálogo una autoría verificada que cumpla esa consulta.

**No** debería inventar un libro de Elena para completar la conversación. Tampoco debería afirmar «Elena nunca escribió sobre grafos», porque la ausencia de un registro no demuestra el hecho negativo.

## 7. Cómo evaluar GraphRAG sin fiarte de la fluidez

Necesitas preguntas con respuestas de referencia y **fuentes esperadas**.

| Pregunta de prueba | Resultado esperado | Error que revela |
|---|---|---|
| Libros de Marina sobre Grafos | ISBN-001 y ISBN-002, con fuentes | Omisión de hechos |
| Libros de Diego sobre Grafos | Ninguno respaldado | Alucinación por confusión de autores |
| Libros de Marina sobre Naturaleza | Ninguno respaldado | Relación temática inventada |
| Autor de Historias del océano | Diego, con F-003 | Error de identidad |

Podemos evaluar por separado:

- **Recuperación:** ¿aparecieron los documentos o relaciones que necesitábamos?
- **Fidelidad o grounding:** ¿cada afirmación de la respuesta está respaldada por el contexto recuperado?
- **Corrección factual:** ¿coincide con la información verificada y actual?
- **Abstención:** ¿el sistema evita responder cuando carece de evidencia?
- **Seguridad:** ¿respeta permisos, evita revelar datos privados y trata fuentes como contenido no confiable?

No se debe concluir «sistema bueno» simplemente porque responde con un texto bonito.

## 8. Grafo frente a búsqueda vectorial

La [semana 20](semana-20.md) compara similitud aproximada. El grafo permite además imponer restricciones estructurales:

```cypher
MATCH (a:Autor {id:$autor_id})-[:ESCRIBIO]->(l:Libro)
      -[:TRATA_SOBRE]->(t:Tema {codigo:$tema})
RETURN l.isbn AS isbn, l.titulo AS titulo;
```

El patrón exige que exista una autoría **y** una clasificación temática. La búsqueda vectorial, en cambio, puede recuperar descripciones relevantes que luego necesitarás verificar contra los vínculos del grafo.

**No son opciones excluyentes.** Un sistema híbrido puede usar similitud para candidatos y patrones Cypher para comprobar identidad o relaciones.

## 9. Ejercicios graduados

1. Reproduce las dos respuestas respaldadas de Marina.
2. Consulta un autor inexistente y explica qué significa obtener lista vacía.
3. Quita la fuente de un libro y repite la consulta. ¿Qué cambia?
4. Agrega una ficha que clasifique mal el tema y explica qué control editorial necesitas.
5. Diseña un conjunto de diez preguntas, incluidas cuatro cuya respuesta correcta sea no responder con afirmaciones.
6. Escribe una función que genere una respuesta solo si **cada fila incluye fuente**.
7. Propón cómo recuperarías relaciones con Neo4j, incluyendo permisos e identificadores estables.

### Soluciones comentadas

**3.** Al perder el campo fuente, nuestro filtro deja de seleccionar esa fila. Esto detecta **ausencia de procedencia**, no falsedad del libro.

**4.** Debes revisar el hecho con una fuente autorizada; un grafo estructurado puede contener errores semánticos perfectamente válidos para Cypher.

**5.** Incluye homónimos, temas cercanos, libros sin fuente, autorías contradictorias y preguntas fuera del alcance del catálogo.

**6.** Comprueba fuentes antes de crear el texto. Si no quedan resultados, devuelve una respuesta explícita de ausencia de evidencia, sin inventar datos.

## 10. Prueba de autonomía y pasos siguientes

Entrega: catálogo ficticio, función de recuperación, suite de preguntas positivas y negativas, criterios para aceptar referencias y un informe que describa los errores. Después realiza una integración real con un motor de grafos y un modelo generativo, instrumentando la recuperación y las salidas para comprobarlas.

**Siguiente:** [semana 22 — convertirlo en una API](semana-22.md).

## Referencias oficiales

- [Neo4j GraphRAG Python](https://neo4j.com/docs/neo4j-graphrag-python/current/)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [Neo4j Cypher MATCH](https://neo4j.com/docs/cypher-manual/current/clauses/match/)

**Estado:** clase conceptual y práctica local de recuperación, pero **NO** es aún una implementación GraphRAG de extremo a extremo con LLM y evaluación de producción. Falta ese laboratorio de integración para declararla completa.
