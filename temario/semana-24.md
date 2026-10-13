# Semana 24 — Entrega final: aplicación demostrable y criterio técnico

> **Estado pedagógico: unidad introductoria, no equivalente a formación experta.** Este tema requiere todavía una lección desarrollada desde sus prerrequisitos, implementación reproducible de extremo a extremo, ejercicios con respuestas razonadas y evaluación con casos negativos. Lee esta página como orientación, no como certificado de dominio.

**Antes de continuar:** asegúrate de entender la terminología del [glosario](glosario-desde-cero.md) y de haber completado los bloques de modelado, Cypher, Python y calidad de datos. Si una sigla o una función aparecen sin explicación suficiente en este borrador, no se consideran conocimientos que ya debas poseer.


**Caso:** biblioteca digital ficticia · **Dedicación sugerida:** 8–10 horas.

## Objetivos de la unidad

- Entender las decisiones técnicas, sus límites y sus costes.
- Reproducir el ejemplo sin datos ni credenciales reales.
- Aplicar el tema al proyecto público de biblioteca y justificar resultados.
- Crear pruebas y documentación antes de declarar la funcionalidad terminada.

## 1. Fundamentos

El cierre del itinerario no consiste en acumular tecnologías. Demuestra un conjunto pequeño de funcionalidades implementadas y correctamente justificadas: crear y encontrar libros, relacionarlos con temas y autores, rastrear procedencia y validar un subconjunto RDF cuando corresponda. Explica por qué elegiste el motor, qué problemas resuelve y qué queda fuera de alcance. La evaluación debe ser reproducible por otra persona.

## 2. Ejemplo comentado

```text
biblioteca-final/
  README.md
  docs/decisiones.md
  docs/arquitectura.svg
  src/
  scripts/
  tests/
  ejemplos/
  .env.example
```

**Qué debes verificar:** identifica de dónde sale cada dato, cuáles son los supuestos de la consulta o función y qué ocurriría ante una entrada inesperada. El ejemplo es una base para experimentar; no sustituye pruebas de integración con la infraestructura usada.

## 3. Laboratorio práctico

Entrega README con instalación, datos ficticios, arquitectura, tres consultas Cypher, ejemplo RDF/SHACL y diez tests. Prepara una demo de 8 minutos y un apartado «Limitaciones conocidas».

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

- [Neo4j GraphAcademy](https://graphacademy.neo4j.com/)
- [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)
- [SHACL](https://www.w3.org/TR/shacl/)
