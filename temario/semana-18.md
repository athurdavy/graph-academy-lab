# Semana 18 — Knowledge Graphs: unir entidades, relaciones y evidencias

**Caso:** biblioteca digital ficticia · **Dedicación sugerida:** 8–10 horas.

## Objetivos de la unidad

- Entender las decisiones técnicas, sus límites y sus costes.
- Reproducir el ejemplo sin datos ni credenciales reales.
- Aplicar el tema al proyecto público de biblioteca y justificar resultados.
- Crear pruebas y documentación antes de declarar la funcionalidad terminada.

## 1. Fundamentos

Un knowledge graph no es simplemente cualquier grafo: necesita un modelo de entidades y relaciones cuyo significado resulte suficientemente explícito para responder preguntas, integrar datos y verificar su procedencia. Para una biblioteca ficticia, los vértices Libro, Autor y Tema y las relaciones ESCRIBIO, TRATA_SOBRE y RECOMENDADO_POR pueden representar conocimientos de diferente fiabilidad. No mezcles observaciones editoriales con hipótesis generadas por algoritmos sin anotar origen y estado.

## 2. Ejemplo comentado

```cypher
MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro)-[:TRATA_SOBRE]->(t:Tema)
RETURN a.nombre AS autor, t.nombre AS tema, count(DISTINCT l) AS libros
ORDER BY libros DESC
```

**Qué debes verificar:** identifica de dónde sale cada dato, cuáles son los supuestos de la consulta o función y qué ocurriría ante una entrada inesperada. El ejemplo es una base para experimentar; no sustituye pruebas de integración con la infraestructura usada.

## 3. Laboratorio práctico

Modela una relación de clasificación propuesta y otra aprobada. Decide si usas una propiedad en una arista o una entidad Clasificacion, teniendo en cuenta auditoría e historial. Crea una consulta que muestre solo clasificaciones aprobadas.

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
- [RDF Primer](https://www.w3.org/TR/rdf11-primer/)
