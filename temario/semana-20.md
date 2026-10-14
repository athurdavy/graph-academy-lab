# Semana 20 — Búsqueda por significado: embeddings, vectores y evaluación

**Antes:** [semana 19 — extraer entidades y medir errores](semana-19.md). **Después:** [semana 21 — GraphRAG](semana-21.md). Tiempo recomendado: 8–12 horas. **Objetivo:** entender por qué dos frases pueden parecerse aunque usen palabras distintas, cómo representarlas con números y por qué una búsqueda vectorial puede equivocarse.

## 1. El problema que vamos a resolver

Nuestro catálogo ficticio incluye tres libros:

- *El mapa de los grafos*: introducción a redes y conexiones.
- *Rutas de conocimiento*: métodos para organizar información.
- *Historias del océano*: relatos sobre vida marina.

Un lector escribe «quiero aprender sobre conexiones entre cosas». Una búsqueda que exige la palabra exacta «grafos» quizá no encuentre el libro más adecuado. ¿Podemos comparar el **significado aproximado** de la consulta con las descripciones?

Para eso existen representaciones numéricas conocidas como **embeddings**. No necesitamos saber todavía usar inteligencia artificial para entender la operación básica.

## 2. Qué es un vector, explicado sin matemáticas previas

Un **vector** es una lista ordenada de números. Por ejemplo:

```python
libro_grafos = [0.9, 0.1]
libro_oceano = [0.1, 0.9]
pregunta = [0.8, 0.2]
```

En este **ejemplo inventado**, imaginemos que el primer número representa cercanía al tema «grafos» y el segundo cercanía al tema «océano».

La pregunta se parece más a `libro_grafos` que a `libro_oceano`.

**Advertencia:** los embeddings generados por modelos reales no tienen necesariamente dimensiones tan fáciles de interpretar. Pueden tener cientos o miles de números, y una dimensión aislada no suele significar literalmente «grafos». Nuestro vector de dos números solo sirve para comprender el cálculo.

## 3. ¿Qué significa embedding?

Un **embedding** es una representación numérica que coloca elementos en un espacio matemático donde ciertas relaciones de similitud pueden estimarse. Un modelo de lenguaje puede producir embeddings para textos y consultas.

No significa que la representación sea una verdad semántica. Un embedding puede:
- acercar documentos conceptualmente relacionados;
- confundir distintos sentidos de una palabra;
- equivocarse con negaciones;
- aproximar similitud sin verificar hechos bibliográficos.

Por tanto, **similitud no es identidad, ni evidencia, ni corrección factual**.

## 4. Distancia y similitud: ¿qué estamos comparando?

Tenemos dos vectores, por ejemplo `[0.9, 0.1]` y `[0.8, 0.2]`. Una forma sencilla de comparar es la **distancia euclídea**, que generaliza la distancia entre puntos. Valores más pequeños indican mayor cercanía en ese espacio, pero no garantizan relevancia humana.

En búsquedas vectoriales también se utiliza la **similitud coseno**: compara la dirección de dos vectores. Sus resultados y límites dependen de cómo se generan y normalizan las representaciones.

### Código Python sin ninguna API externa

```python
from math import sqrt

def similitud_coseno(a, b):
    if len(a) != len(b):
        raise ValueError("Las dimensiones deben coincidir")
    producto = sum(x * y for x, y in zip(a, b))
    norma_a = sqrt(sum(x * x for x in a))
    norma_b = sqrt(sum(x * x for x in b))
    if norma_a == 0 or norma_b == 0:
        raise ValueError("No se permite vector de norma cero")
    return producto / (norma_a * norma_b)

pregunta = [0.8, 0.2]
libros = {
    "El mapa de los grafos": [0.9, 0.1],
    "Historias del océano": [0.1, 0.9],
}
resultados = sorted(
    ((nombre, similitud_coseno(pregunta, vector))
     for nombre, vector in libros.items()),
    key=lambda item: item[1],
    reverse=True,
)
for nombre, _similitud in resultados:
    print(nombre)
```

**Resultado esperado:**

```text
El mapa de los grafos
Historias del océano
```

### Explica el código, no lo copies

- `zip(a, b)` empareja posiciones; primero comprobamos que ambas listas tengan la misma longitud.
- `sum(x*y ...)` calcula el producto escalar.
- `sqrt` obtiene la raíz cuadrada para calcular la longitud de los vectores.
- Si alguna norma es cero, **no dividimos por cero**.
- `sorted(..., reverse=True)` ordena la similitud de mayor a menor.
- La función devuelve una medida numérica, **no una prueba** de que un libro responda correctamente.

## 5. Búsqueda léxica frente a búsqueda vectorial

**Búsqueda léxica**: encuentra palabras o expresiones según reglas del motor. Puede ser excelente para ISBN, nombres exactos y códigos.

**Búsqueda vectorial**: compara representaciones numéricas para aproximar similitud semántica.

Ejemplo: si el usuario pide ISBN-001, conviene una búsqueda exacta. Si pide «manual para aprender conexiones entre entidades», puede interesar una búsqueda semántica.

**Búsqueda híbrida**: combina señales léxicas y vectoriales. No existe una regla universal según la cual «usar embeddings» mejore la calidad; hay que medir cada método.

## 6. ¿Qué hace un índice vectorial?

Un **índice** es una estructura que ayuda a recuperar candidatos sin comparar manualmente todos los elementos. Los índices vectoriales están diseñados para localizar vecinos cercanos en espacios numéricos.

En Neo4j hay funcionalidades de índices vectoriales, pero su sintaxis y capacidades dependen de versiones. Antes de programar, consulta la documentación de la versión concreta.

**No confundas tres tareas:**

1. Generar embeddings, normalmente mediante un modelo externo o local.
2. Almacenar esos vectores como propiedades de elementos del grafo.
3. Recuperar vecinos próximos usando el índice del motor.

Crear un índice por sí solo **no convierte descripciones en embeddings ni valida resultados**.

## 7. Cómo se mide una recuperación

Necesitas preguntas de prueba con libros considerados relevantes. Si no defines relevancia, no puedes afirmar que la búsqueda es buena.

Ejemplo:

```text
Pregunta: «quiero conocer grafos y conexiones»
Relevante: ISBN-001
No relevante: ISBN-003
```

Si el resultado top-1 es ISBN-001, la búsqueda acertó este ejemplo. Pero un solo acierto no demuestra nada sobre otras consultas.

### Recall@k, explicado

**Recall@k** mide qué proporción de los elementos relevantes aparece entre los primeros `k` resultados recuperados.

Si hay **dos** libros relevantes y entre los tres primeros resultados recuperas solo uno, Recall@3 es `1/2 = 0,5`. La cifra no evalúa por sí sola si la respuesta generada después de recuperar es correcta.

También conviene medir errores donde la búsqueda vectorial encuentra un libro de título parecido, pero con tema diferente.

## 8. Pruebas negativas obligatorias

**Caso 1:** introduce dos vectores de dimensiones distintas. Nuestra función debe lanzar `ValueError`.

**Caso 2:** introduce un vector de ceros. No debe hacer una división inválida.

**Caso 3:** pregunta por un ISBN exacto. Justifica si utilizarías primero una búsqueda por código en vez de un embedding.

**Caso 4:** dos libros tienen descripciones similares, pero uno aporta evidencia bibliográfica y el otro no. La similitud no basta para seleccionar una respuesta fiable.

## 9. Ejercicios con soluciones

1. Calcula a mano qué libro se parece más a `[0.8, 0.2]` por el criterio inventado de dos dimensiones.
2. Modifica la consulta a `[0.1, 0.9]` y predice el nuevo orden.
3. Añade un tercer libro con vector `[0.5, 0.5]` y ordénalos.
4. Diseña cinco preguntas reales sobre el catálogo y anota qué libros deberían recuperarse.
5. Compara recuperación exacta por ISBN y recuperación aproximada por tema.
6. Documenta cuándo el sistema debería abstenerse de recomendar un libro.

### Soluciones orientativas

**1.** El vector de grafos apunta en una dirección similar a la consulta. El código lo coloca primero; el valor es una medida de cercanía numérica, no una conclusión lógica.

**2.** Con una consulta cercana al segundo vector, debe salir primero *Historias del océano*. Confírmalo ejecutando el programa.

**4.** La colección de evaluación debe incluir consultas positivas y negativas, información ambigua y distintas formas de preguntar. No reutilices las mismas preguntas para desarrollar el método y para proclamar su calidad.

**6.** Una política de abstención necesita umbrales medidos y un criterio de relevancia; no inventes un valor universal de similitud «segura».

## 10. Demostración de autonomía

Diseña un conjunto de 10 libros ficticios y 10 consultas de prueba. Compara una búsqueda simple por palabras con la representación vectorial que elijas y mide Recall@k con etiquetas de relevancia revisadas. Entrega código, datos, criterios de evaluación y al menos un caso de error.

**Siguiente:** [semana 21 — cómo GraphRAG utiliza recuperación y evidencias](semana-21.md).

## Fuentes y límites

- [Neo4j — índices vectoriales](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)
- [scikit-learn — similitud coseno](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- [Information retrieval — métricas](https://scikit-learn.org/stable/modules/model_evaluation.html)

**Estado:** introducción práctica a similitud y evaluación. Aún falta un laboratorio completo con modelos de embeddings reales, índices de motor y comparación reproducible antes de declarar esta clase cerrada.
