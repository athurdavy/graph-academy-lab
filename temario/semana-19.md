# Semana 19 — Extracción de entidades y evaluación de NLP

**Caso:** biblioteca digital ficticia · **Dedicación sugerida:** 8–10 horas.

## Objetivos de la unidad

- Entender las decisiones técnicas, sus límites y sus costes.
- Reproducir el ejemplo sin datos ni credenciales reales.
- Aplicar el tema al proyecto público de biblioteca y justificar resultados.
- Crear pruebas y documentación antes de declarar la funcionalidad terminada.

## 1. Fundamentos

La extracción automática de entidades puede encontrar autores, libros y temas en descripciones, pero una coincidencia de texto no demuestra identidad. Un pipeline robusto distingue detección, normalización, enlace a entidades existentes y validación humana. Evalúa con un conjunto etiquetado, evitando medir exclusivamente sobre los datos empleados para crear las reglas.

## 2. Ejemplo comentado

```python
def precision(tp: int, fp: int) -> float:
    return tp / (tp + fp) if tp + fp else 0.0

def recall(tp: int, fn: int) -> float:
    return tp / (tp + fn) if tp + fn else 0.0

assert precision(8, 2) == 0.8
assert recall(8, 2) == 0.8
```

**Qué debes verificar:** identifica de dónde sale cada dato, cuáles son los supuestos de la consulta o función y qué ocurriría ante una entrada inesperada. El ejemplo es una base para experimentar; no sustituye pruebas de integración con la infraestructura usada.

## 3. Laboratorio práctico

Redacta 30 descripciones ficticias de libros con entidades anotadas. Separa 20 para desarrollar reglas y 10 para evaluar. Define cuándo una extracción puede ser aceptada y cuándo debe revisarse.

**Evidencias a guardar:** fichero fuente, casos de entrada, resultado esperado, resultado obtenido y explicación de discrepancias. Usa únicamente identidades y datos inventados.

## 4. Preguntas de autoevaluación

1. ¿Qué problema resuelve esta tecnología y cuál no?
2. ¿Cómo sabes que la salida es correcta y no solo plausible?
3. ¿Qué errores o datos incompletos afectarían al resultado?
4. ¿Qué alternativa más sencilla usarías y por qué?
5. ¿Cómo documentarías el método para que otra persona lo reproduzca?

## 5. Criterios de entrega

- [ ] El ejemplo ejecuta en un entorno controlado, o queda documentada la dependencia que lo impide.
- [ ] Las hipótesis están separadas de los hechos comprobados.
- [ ] Hay pruebas al menos de un caso correcto y un caso límite.
- [ ] No se publican secretos ni información privada.
- [ ] Las fuentes externas se citan y se identifica la versión usada.

## Referencias

- [spaCy documentation](https://spacy.io/usage)
- [scikit-learn classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
