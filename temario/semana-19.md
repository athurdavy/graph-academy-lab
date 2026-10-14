# Semana 19 — Extraer entidades de textos y medir los errores

**Antes:** [semana 18 — afirmaciones y evidencias](semana-18.md). **Después:** [semana 20 — embeddings](semana-20.md). **Objetivo:** convertir una frase de la biblioteca en entidades candidatas, distinguir detección de identificación y evaluar el resultado con ejemplos que fallen. Tiempo estimado: 8–12 horas.

## 1. Partimos de una frase realista, no de siglas

Una ficha ficticia contiene:

> Marina Soler escribió El mapa de los grafos en 2022.

Quieres convertir ese texto en los datos de la biblioteca. Antes de relacionar información necesitas saber **qué fragmentos de texto mencionan entidades**.

En el ejemplo podrías detectar:

- «Marina Soler»: mención de una persona.
- «El mapa de los grafos»: mención de una obra.
- «2022»: fecha o año.
- «escribió»: palabra que sugiere una relación.

**Detectar una mención no demuestra que la información sea verdadera.** Tampoco demuestra que «Marina Soler» sea la persona con ID A-001. Hacen falta contexto, criterios de identidad y procedencia.

## 2. ¿Qué es NLP y qué es NER?

**NLP** son siglas de *Natural Language Processing*, «procesamiento del lenguaje natural»: técnicas para trabajar con textos en lenguajes humanos.

**NER** significa *Named Entity Recognition*, «reconocimiento de entidades nombradas». Un sistema NER encuentra partes del texto que probablemente mencionan personas, organizaciones, lugares, etc., según las categorías y el modelo utilizado.

Un modelo general de NER **no garantiza** reconocer correctamente títulos de libros como una categoría propia. Para eso quizá necesites reglas o un modelo ajustado al dominio.

### Dos tareas distintas

1. **Detectar:** encontrar que la secuencia «Marina Soler» parece el nombre de una persona.
2. **Resolver o enlazar identidad:** decidir si se refiere exactamente a la autora ficticia con ID A-001.

Esta segunda tarea se llama frecuentemente *entity linking* o enlace de entidades. Si la confundes con NER, tu grafo terminará fusionando homónimos.

## 3. Primer extractor explicable con Python estándar

No instalaremos todavía modelos enormes. Empezaremos por un diccionario de nombres ficticios conocidos. **No es un sistema NER general**; es una herramienta de aprendizaje para entender entradas, salidas y límites.

```python
catalogo_autores = {
    "Marina Soler": "A-001",
    "Diego Ríos": "A-002",
}

def extraer_autores_conocidos(texto):
    encontrados = []
    for nombre, identificador in catalogo_autores.items():
        if nombre in texto:
            encontrados.append({"texto": nombre, "id_candidato": identificador})
    return encontrados

frase = "Marina Soler escribió El mapa de los grafos."
print(extraer_autores_conocidos(frase))
```

**Resultado esperado:**

```text
[{'texto': 'Marina Soler', 'id_candidato': 'A-001'}]
```

### Comprende cada decisión

- El diccionario relaciona nombres con identificadores de nuestro dataset de prácticas.
- `items()` permite recorrer parejas nombre/ID.
- La condición `if nombre in texto` comprueba coincidencia **literal** de subcadenas.
- La salida contiene un `id_candidato`, no un ID confirmado.
- La función puede fallar con mayúsculas, abreviaturas, homónimos y menciones dentro de palabras más largas.

**Experimento negativo:** prueba «marina soler» en minúsculas; el extractor tal como está escrito no lo encuentra. Ese fallo te enseña a identificar supuestos del algoritmo.

## 4. Un error peligroso: fusionar personas por nombre

Imagina dos autoras diferentes con el mismo nombre «Marina Soler». Si solo conservas el texto, **no tienes información suficiente** para distinguirlas.

No crees una relación `owl:sameAs` ni fusiones nodos de Neo4j basándote solo en coincidencia de nombres. La extracción produce **candidatos** para revisión; la identidad se confirma con fuentes y reglas específicas.

## 5. Cómo medir la calidad: TP, FP y FN desde cero

Para evaluar necesitas **datos etiquetados de referencia** (*ground truth*): ejemplos donde una persona revisó cuáles menciones deberían detectarse.

Tres siglas:

- **TP** (*True Positive*, verdadero positivo): detectaste una mención que realmente correspondía a la categoría evaluada.
- **FP** (*False Positive*, falso positivo): detectaste algo que no debía contarse como entidad de esa categoría.
- **FN** (*False Negative*, falso negativo): no detectaste una mención que sí debías detectar.

Ejemplo de cinco casos etiquetados:

| Caso | ¿La detección es correcta? | Clasificación |
|---|---|---|
| Detectaste Marina y sí era una autora | Sí | TP |
| Detectaste Diego y sí era autor | Sí | TP |
| Marcaste «El mapa» como persona | No | FP |
| No detectaste Elena, que sí era persona | No | FN |

Aquí contamos 2 TP, 1 FP y 1 FN.

### Precisión y exhaustividad

**Precisión** (*precision*) responde: «de todo lo que afirmé detectar, ¿qué parte era correcta?»

`precision = TP / (TP + FP)`. Aquí: `2 / (2 + 1) = 2/3`, aproximadamente 0,67.

**Exhaustividad** (*recall*) responde: «de lo que debía encontrar, ¿qué parte encontré?»

`recall = TP / (TP + FN)`. Aquí: `2 / (2 + 1) = 2/3`, aproximadamente 0,67.

Si el denominador vale cero, define cómo reportar la métrica según la política de evaluación; evita dividir por cero y ocultarlo.

## 6. Código para comprobar las métricas

```python
def precision_y_recall(tp, fp, fn):
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return precision, recall

p, r = precision_y_recall(tp=2, fp=1, fn=1)
print(round(p, 2), round(r, 2))
```

**Esperado:** `0.67 0.67`.

La métrica está bien calculada para esos recuentos inventados. Eso **no demuestra** que un modelo real tenga esa calidad; para evaluarlo necesitas resultados del sistema sobre un conjunto de prueba que no haya utilizado para ajustarse.

### ¿Y qué es F1?

**F1** combina precisión y recall con su media armónica: `F1 = 2 × precision × recall / (precision + recall)` cuando el denominador es positivo. No es una garantía universal de calidad: depende de la tarea, distribución de casos y coste de los errores.

## 7. spaCy: pasar de reglas manuales a un sistema NLP

**spaCy** es una biblioteca Python de procesamiento de lenguaje natural. Puedes obtener entidades detectadas por uno de sus modelos disponibles para el idioma correspondiente.

Conceptualmente:

```python
import spacy

modelo = spacy.load("es_core_news_sm")
doc = modelo("Marina Soler escribió El mapa de los grafos.")
for entidad in doc.ents:
    print(entidad.text, entidad.label_)
```

**Condición:** antes instala spaCy y descarga el modelo español compatible siguiendo la documentación oficial. No esperamos una salida fija en este curso porque **el resultado depende de la versión y del modelo**, y un modelo genérico puede clasificar títulos de libros de manera distinta.

No añadas resultados inventados a tu informe: guarda versión, texto de entrada y predicciones reales.

## 8. Del extractor al grafo: un flujo reproducible

```text
Texto fuente
  → menciones candidatas
  → normalización de nombres
  → candidatos de identidad
  → resolución con evidencia
  → afirmaciones con fuente
  → pruebas de calidad
  → grafo de conocimiento
```

Cada flecha representa una decisión y una posible fuente de error. Si enlazas una persona equivocada, la relación de autoría del grafo puede parecer técnicamente válida y aun así ser falsa.

**Primero evalúa NER. Después evalúa enlace de entidades. Después evalúa relaciones.** Una sola métrica mezclada oculta dónde aparece el error.

## 9. Ejercicios graduales

1. Ejecuta el extractor manual con «Marina Soler escribió un libro».
2. Cambia a minúsculas el nombre de entrada. Explica por qué falla.
3. Añade «Elena Vidal» al diccionario y prueba una segunda frase.
4. Construye una pequeña tabla de TP, FP y FN y calcula precision y recall.
5. Diseña un caso con dos autoras llamadas igual. Explica qué otra evidencia necesitas.
6. Escribe una política para no convertir automáticamente todas las menciones en relaciones del grafo.
7. Prueba un modelo spaCy indicando modelo y versión. Compara sus errores con el extractor de reglas.

### Soluciones comentadas

**2.** El operador `in` compara subcadenas de manera sensible a mayúsculas/minúsculas. Convertir a minúsculas puede mejorar ciertos casos, pero no resuelve homónimos ni infiere identidad.

**4.** Con TP=2, FP=1 y FN=1, precisión y recall valen 2/3. Si aumentan los falsos positivos, la precisión disminuye, manteniendo los otros valores.

**5.** Necesitas identificadores de confianza, contexto y fuentes. La igualdad textual no constituye una prueba de identidad.

**6.** Guarda las menciones como candidatos y confirma los vínculos cuando haya evidencia suficiente; registra de dónde salió cada decisión.

## 10. Prueba de autonomía

Recibe diez frases de biblioteca no vistas antes. Marca manualmente las entidades de referencia, ejecuta tu extractor, cuenta TP/FP/FN, calcula precisión y recall y explica al menos tres errores de clasificación.

**Siguiente:** [semana 20 — embeddings, similitud y recuperación](semana-20.md).

## Fuentes primarias

- [spaCy — modelos y entidades](https://spacy.io/usage/linguistic-features#named-entities)
- [scikit-learn — precision, recall y F1](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)

**Estado editorial:** ejemplos manuales diseñados para enseñanza; la ejecución real de spaCy y la evaluación sobre datos inéditos quedan como ejercicios obligatorios, no validados automáticamente por esta revisión.
