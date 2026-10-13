# Semana 10 — Comparación Neo4j vs ArcadeDB sin marketing

**Objetivo:** tomar decisiones con requisitos, datos y pruebas. No existe un «ganador» universal.

## 1. Define un benchmark justo

Con el mismo conjunto **ficticio** de libros, autores y temas ejecuta:

1. Buscar libro por identificador.
2. Recuperar sus autores.
3. Listar libros asociados a un tema.
4. Recorrer dos saltos \`Autor → Libro → Tema\`.
5. Cargar 1.000 registros sintéticos.
6. Repetir la carga y contar duplicados.

**Controla:** hardware/plan, índices, tamaño de datos, latencia de red, concurrencia y caché. No compares AuraDB remoto con un ArcadeDB local sin aclarar que el resultado incluye la red.

## 2. Matriz de evaluación

| Criterio | Qué debes documentar |
|---|---|
| Lenguajes | Consultas necesarias y compatibilidad demostrada |
| Python | API/driver, transacciones, mantenimiento |
| Operación | Copias, actualizaciones, usuarios, observabilidad |
| Coste | Recursos, trabajo operativo y límites de plan |
| Semántica | RDF, SKOS, OWL y SHACL: requisitos frente a soporte comprobado |
| Seguridad | Aislamiento, cifrado, permisos y auditoría |

## 3. Cómo redactar el informe

Para cada afirmación incluye **prueba o enlace oficial**. Distingue:

- Hecho documentado.
- Observación experimental.
- Hipótesis que aún no se ha validado.

Ejemplo correcto: «Con 3.000 libros sintéticos y una consulta parametrizada, el tiempo mediano de 30 ejecuciones fue X en la configuración Y». Ejemplo incorrecto: «El motor A es siempre más rápido».

## 4. Ejercicios

1. Prepara tablas con resultados y parámetros de consulta.
2. Decide si añadir PostgreSQL aporta valor o complejidad innecesaria.
3. Evalúa si la semántica del catálogo requiere una representación RDF separada.
4. Explica la migración, el lock-in y el coste de mantener dos drivers.

## Entregable

Un informe de 2–4 páginas con matriz de decisión, scripts, contexto de ejecución y riesgos.

## Fuentes

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [ArcadeDB Documentation](https://docs.arcadedb.com/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
