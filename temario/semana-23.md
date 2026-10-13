# Semana 23 — Pruebas, rendimiento y seguridad del prototipo

**Caso:** biblioteca digital ficticia · **Dedicación sugerida:** 8–10 horas.

## Objetivos de la unidad

- Entender las decisiones técnicas, sus límites y sus costes.
- Reproducir el ejemplo sin datos ni credenciales reales.
- Aplicar el tema al proyecto público de biblioteca y justificar resultados.
- Crear pruebas y documentación antes de declarar la funcionalidad terminada.

## 1. Fundamentos

La fiabilidad se comprueba en varias capas: tests unitarios para reglas, integración para consultas reales, pruebas de datos para consistencia y pruebas funcionales para endpoints. Examina los planes de ejecución con EXPLAIN y PROFILE antes de optimizar. No uses información sensible, ni credenciales embebidas. Para un proyecto con dos bases, incorpora reconciliación y detección de desfases.

## 2. Ejemplo comentado

```cypher
MATCH (l:Libro {isbn:$isbn})
RETURN l.titulo AS titulo;

// En Neo4j Browser, examina el plan:
// EXPLAIN MATCH (l:Libro {isbn:$isbn}) RETURN l.titulo
```

**Qué debes verificar:** identifica de dónde sale cada dato, cuáles son los supuestos de la consulta o función y qué ocurriría ante una entrada inesperada. El ejemplo es una base para experimentar; no sustituye pruebas de integración con la infraestructura usada.

## 3. Laboratorio práctico

Diseña una matriz con al menos 15 pruebas: 5 de dominio, 5 de consultas y 5 de entrada/API. Mide los tiempos con datos reproducibles, registra el plan y comprueba qué índice se usa.

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

- [Neo4j query tuning](https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/query-tuning/)
- [pytest](https://docs.pytest.org/)
