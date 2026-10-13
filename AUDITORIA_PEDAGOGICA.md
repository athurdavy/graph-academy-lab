# Auditoría pedagógica y criterio de calidad — octubre 2026

## Veredicto desde la perspectiva de un programador que empieza desde cero

**No: el material actual no basta todavía para garantizar la preparación de un experto.** Hay 24 lecciones de profundidad desigual y una ruta extendida de 42 competencias. Las unidades avanzadas de GraphDB, Protégé, OWL, SPARQL, GDS, ORM/OGM y GraphRAG requieren laboratorios integrales y evaluación adicional.

## Problemas identificados

- Existían itinerarios distintos y recursos dispersos sin una entrada única para principiantes.
- Los primeros ejemplos cambiaban de dominio, dificultando seguir un solo caso.
- Las definiciones no siempre se explicaban antes de introducir operaciones sobre ellas.
- Algunos temas complejos tienen una descripción breve que no es una clase completa.
- Las pruebas y las preguntas de práctica no cubren todos los resultados de aprendizaje.
- No hay verificación completa, humana y reproducible de todas las herramientas y versiones.
- Un índice o una lista de estándares no equivale a saber diseñar una ontología.

## Cambios concretos implantados

- Página de orientación desde cero: empezar.html.
- Ruta secuencial y transparente: ruta.html.
- Lecciones iniciales 01, 02 y 03 reescritas con el mismo catálogo ficticio, ejemplos y resultados esperados.
- Semana 04 ampliada con transición de NetworkX a Neo4j.
- Lector con apartados internos, índice de cada unidad, botones de copia y navegación de módulos agrupada.
- Acceso al contenido desde el campus, manteniendo los laboratorios y la extensión de exámenes separados.

## Criterios para dar por terminada una clase

1. Objetivo observable y conocimientos previos explícitos.
2. Explicación desde cero con motivación del problema.
3. Dibujo técnico con significado de relaciones y leyenda.
4. Ejemplo pequeño ejecutable explicado línea por línea.
5. Instrucciones, versiones de dependencia y salida esperada.
6. Experimento donde se cambia un dato y se interpreta el resultado.
7. Tres ejercicios de complejidad progresiva.
8. Soluciones razonadas y explicación de errores comunes.
9. Pruebas unitarias o de integración y al menos un caso negativo.
10. Preguntas de autoevaluación antes de pasar a la siguiente unidad.
11. Referencias primarias y distinción entre norma, práctica e hipótesis.
12. Revisión técnica y editorial antes de marcarla como completa.

## Cobertura pendiente

| Bloque | Estado de calidad | Trabajo importante pendiente |
|---|---|---|
| Fundamentos 1–3 | Reestructurados | Revisión técnica e integración con ejercicios |
| Neo4j / Cypher | Parcial | Lenguaje completo, transacciones, índices, seguridad y GDS |
| ArcadeDB | Parcial | Despliegue y comparativa reproducible |
| RDF / SPARQL | Parcial | Named graphs, SPARQL avanzado y validación |
| SKOS / DCMI | Parcial | Alineación, metadatos y gobernanza |
| OWL / Protégé | Insuficiente para experto | Axiomas, razonadores, perfiles, inferencia y práctica extensa |
| GraphDB | Guía introductoria | Repositorios ejecutados, inferencia y SHACL real |
| ORM / OGM | Parcial | SQLAlchemy y neomodel con código integrador |
| GraphRAG | Introductorio | Pipeline completo y evaluación de respuestas |
| Certificaciones | Banco inicial | Simulacros amplios y práctica oficial equivalente |

**No declarar aprobado, experto ni titulado a alguien solo por recorrer los enlaces.** El programa es independiente y no concede acreditación oficial.