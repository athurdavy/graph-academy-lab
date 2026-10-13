# Semana 20 — Embeddings y recuperación: medir antes de integrar

**Caso:** biblioteca digital ficticia · **Dedicación sugerida:** 8–10 horas.

## Objetivos de la unidad

- Entender las decisiones técnicas, sus límites y sus costes.
- Reproducir el ejemplo sin datos ni credenciales reales.
- Aplicar el tema al proyecto público de biblioteca y justificar resultados.
- Crear pruebas y documentación antes de declarar la funcionalidad terminada.

## 1. Fundamentos

Los embeddings codifican características del texto en vectores y permiten buscar candidatos por similitud. No convierten sinónimos en hechos verificados ni garantizan resultados precisos. La arquitectura puede combinar búsqueda textual, filtros estructurados y vectores; primero establece un conjunto de preguntas con respuestas correctas y métricas como recall@k. Evalúa el coste, la privacidad y el mantenimiento del índice.

## 2. Ejemplo comentado

```python
def recall_at_k(recuperados: list[str], relevantes: set[str], k: int) -> float:
    if not relevantes:
        return 0.0
    return len(set(recuperados[:k]) & relevantes) / len(relevantes)

assert recall_at_k(['ISBN-001', 'ISBN-002'], {'ISBN-001'}, 2) == 1.0
```

**Qué debes verificar:** identifica de dónde sale cada dato, cuáles son los supuestos de la consulta o función y qué ocurriría ante una entrada inesperada. El ejemplo es una base para experimentar; no sustituye pruebas de integración con la infraestructura usada.

## 3. Laboratorio práctico

Prepara diez preguntas sobre temas literarios. Compara coincidencias de texto y resultados semánticos usando el mismo catálogo ficticio. Anota consultas que fallen aunque el coseno de similitud sea alto.

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

- [Neo4j vector indexes](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)
- [Information retrieval evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
