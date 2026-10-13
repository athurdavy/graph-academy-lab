# Semana 21 — GraphRAG: recuperación trazable, no respuestas mágicas

> **Estado pedagógico: unidad introductoria, no equivalente a formación experta.** Este tema requiere todavía una lección desarrollada desde sus prerrequisitos, implementación reproducible de extremo a extremo, ejercicios con respuestas razonadas y evaluación con casos negativos. Lee esta página como orientación, no como certificado de dominio.

**Antes de continuar:** asegúrate de entender la terminología del [glosario](glosario-desde-cero.md) y de haber completado los bloques de modelado, Cypher, Python y calidad de datos. Si una sigla o una función aparecen sin explicación suficiente en este borrador, no se consideran conocimientos que ya debas poseer.


**Caso:** biblioteca digital ficticia · **Dedicación sugerida:** 8–10 horas.

## Objetivos de la unidad

- Entender las decisiones técnicas, sus límites y sus costes.
- Reproducir el ejemplo sin datos ni credenciales reales.
- Aplicar el tema al proyecto público de biblioteca y justificar resultados.
- Crear pruebas y documentación antes de declarar la funcionalidad terminada.

## 1. Fundamentos

GraphRAG describe enfoques para enriquecer la recuperación de contexto con estructuras de grafo. No hay una única arquitectura. En la biblioteca, una pregunta «¿qué libros sobre grafos escribió Marina?» puede traducirse en una consulta Cypher parametrizada y ofrecer un contexto respaldado por IDs de libros. La respuesta del modelo debe citar esos datos y admitir que no se encontró evidencia. No permitas que el lenguaje natural se convierta sin revisión en Cypher con privilegios de escritura.

## 2. Ejemplo comentado

```cypher
MATCH (a:Autor {id:$autor_id})-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo:$tema})
RETURN l.isbn AS fuente, l.titulo AS titulo
ORDER BY titulo
```

**Qué debes verificar:** identifica de dónde sale cada dato, cuáles son los supuestos de la consulta o función y qué ocurriría ante una entrada inesperada. El ejemplo es una base para experimentar; no sustituye pruebas de integración con la infraestructura usada.

## 3. Laboratorio práctico

Diseña 15 preguntas, con cinco que no puedan responderse desde el dataset. Evalúa precisión factual, citas a ISBN y porcentaje de abstención correcta. Compara el grafo con recuperación textual y documenta costes.

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

- [Neo4j GraphRAG Python](https://neo4j.com/docs/neo4j-graphrag-python/current/)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
