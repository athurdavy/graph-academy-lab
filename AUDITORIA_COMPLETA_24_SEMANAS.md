# Auditoría de aprendizaje de las 24 semanas — octubre de 2026

**Objetivo:** una persona que sabe programar (Python/SQL), pero parte de cero en grafos y ontologías, debe comprender lo que estudia y demostrar que puede construir algo nuevo sin copiar.

**Esta auditoría NO es una certificación de calidad:** se basa en lectura del repositorio, revisión de código y referencias. Salvo indicación expresa, no demuestra que los ejemplos se hayan ejecutado contra Neo4j AuraDB, ArcadeDB, Protégé, GraphDB y servicios externos. La longitud del texto tampoco prueba resultados pedagógicos. Las lecciones necesitan evaluación con estudiantes reales.

## Criterios que debe cumplir una clase cerrada

| Criterio | Evidencia necesaria |
|---|---|
| Comprensión inicial | Parte de un problema cotidiano; ninguna sigla sin explicar |
| Progresión | Introduce una decisión cada vez, sin utilizar conceptos aún no enseñados |
| Vocabulario | Define cada símbolo, identificador, relación y abreviatura en contexto |
| Exactitud | Código, nombres, archivos y salidas coherentes con el repositorio |
| Laboratorio | Instrucciones de instalación, entrada y salida esperada |
| Comprobación | Casos correctos, negativos, errores frecuentes y explicación |
| Autonomía | Problema nuevo, rúbrica, soluciones razonadas y entrega reproducible |
| Validación | Tests unitarios, integración según motor y resultados verificables |

**Regla editorial:** una unidad puede ser útil, incluso extensa, sin estar todavía «cerrada».

## Revisión individual de las 24 semanas

| Semana | Lo que ya enseña | Riesgo / trabajo todavía necesario | Estado |
|---|---|---|---|
| 01 | Nodos, relaciones, identidad y primer Python; reorganizada para empezar sin sintaxis | Prueba de comprensión con alumnos; revisar fragmentos complejos de modelado | Desarrollo sustancial; sin validación pedagógica externa |
| 02 | Caminos, BFS, DFS, Dijkstra, código y tests | Verificar resultados de todos los ejemplos; ejercicios adicionales de grafos dirigidos | Desarrollo sustancial; integración pendiente |
| 03 | Propiedades vs triples RDF, IRIs, Turtle y RDFLib | Probar serializaciones y consultas; separar estrictamente nociones nuevas de adelantos | Desarrollo sustancial; integración pendiente |
| 04 | Cypher inicial, nodos, restricciones y carga de biblioteca | Probar todas las consultas en AuraDB; limpiar escenarios con duplicados antes de crear constraints | Desarrollo sustancial; integración pendiente |
| 05 | MATCH, WITH, OPTIONAL MATCH, agregación | Faltan soluciones completas de todos los retos y casos de consulta con datos imprevistos | Desarrollo sustancial pero evaluación incompleta |
| 06 | MERGE, UNWIND, LOAD CSV, integridad y referencias | Validar importación real en AuraDB, fallos de red y datos CSV inválidos | Desarrollo sustancial; integración pendiente |
| 07 | Python Driver, parámetros, transacciones y arquitectura | Tests del driver simulado no sustituyen tests de integración y recuperación tras errores | Desarrollo sustancial; integración pendiente |
| 08 | ArcadeDB, conceptos multimodelo y SQL inicial | Validar contra servidor ArcadeDB concreto y repetir sin duplicación | Desarrollo intermedio; integración pendiente |
| 09 | HTTP, JSON, peticiones desde Python y consultas ArcadeDB | Completar suite de pruebas HTTP y respuestas inesperadas; verificar endpoints por versión | Intermedia; tests de integración pendientes |
| 10 | Comparación de motores y criterios de benchmark | Ejecutar una comparación reproducible, con volumen y métricas reales | Parcial; metodología sin campaña de mediciones |
| 11 | Ontologías, RDF/RDFS, OWL, SKOS, SHACL, Python | Trabajo adicional de modelado autónomo y selección de vocabularios | Desarrollo sustancial; evaluación incompleta |
| 12 | Vocabularios SKOS, SPARQL, filtros, caminos y RDFLib | Ampliar consultas avanzadas y validar resultados en GraphDB | Desarrollo sustancial; integración pendiente |
| 13 | OWL, inferencias, mundo abierto, inversas y perfiles | Razonador real, inconsistencias y sesiones Protégé verificadas | Desarrollo sustancial; práctica con motor pendiente |
| 14 | SHACL, shapes, validación positiva y negativa | Añadir informes detallados, reglas avanzadas y configuración GraphDB | Desarrollo sustancial; integración pendiente |
| 15 | Calidad de datos, Cypher y RDF | Definir esquema de incidentes, reporte medible y aceptación de cambios | Intermedia; proyecto evaluado incompleto |
| 16 | Identidad, procedencia y PROV-O | Modelar revisiones de afirmaciones, versionado de vocabularios y reconciliación | Intermedia; proyecto evaluado incompleto |
| 17 | Arquitectura, repositorios, fuente de verdad, ORM/OGM | Construir API integrada, probar sincronización SQL/Neo4j y observabilidad | Intermedia; integración pendiente |
| 18 | KG, afirmaciones con fuente, identidad y NetworkX; reescrita | Tests del laboratorio y reconciliación sobre registros nuevos | Desarrollo sustancial nuevo; integración pendiente |
| 19 | NLP, NER, enlace de entidades, precisión y recall; reescrita | Ensayar modelos y datasets reales, anotar resultados y errores | Desarrollo sustancial nuevo; evaluación de modelo pendiente |
| 20 | Conceptos de embeddings y recuperación | Modelo ejecutable y tests de recuperación, comparación con búsqueda léxica | **Introductoria, no cerrada** |
| 21 | GraphRAG y trazabilidad | Flujo completo con evaluación de citas, no-respuestas y alucinaciones | **Introductoria, no cerrada** |
| 22 | Integración API e importaciones | Aplicación completa ejecutable con contratos y casos de fallo | **Introductoria, no cerrada** |
| 23 | Pruebas, seguridad y rendimiento | Suite completa, métricas y plan de despliegue seguro | **Introductoria, no cerrada** |
| 24 | Entrega final, criterios y defensa | Proyecto construido, rúbrica aplicada y demostración verificable | **Introductoria, no cerrada** |

## Especializaciones y materiales transversales

| Área | Material actual | Qué falta para dominio autónomo |
|---|---|---|
| Protégé/OWL | Taller con pestañas, clases y razonamiento | Sesiones reproducibles, ejercicios inéditos y verificación con razonador real |
| GraphDB | Importación RDF, consultas, inferencias, exportación | Práctica de repositorios con configuración y métricas real, errores y recuperación |
| Certificaciones Neo4j | Cuestionarios de repaso y examen práctico interno | Cobertura oficial versionada, mayor banco inédito de preguntas y simulacros exigentes |
| ArcadeDB | Semanas 08–10 | Operación validada, tests de API y comparación reproducible |
| RDF/DCMI | RDFLib y exportaciones | Publicación, estabilidad de IRIs, versión y conversiones entre formatos verificadas |
| Arquitectura SQL + grafo | Teoría de repositorios y consistencia | Prueba de integración con cambios que fallan a mitad del flujo |
| GraphRAG / GDS / IA | Esquemas avanzados, ejemplos parciales | Material de extremo a extremo, métricas y evaluación con casos negativos |
| Java y Jena/RDF4J | Planificado | Lecciones ejecutables y pruebas; no presentar como impartido |

## Defectos transversales observados

1. **Orden inicial:** enseñar símbolos de Cypher antes de comprender nodos confundía al principiante; se ha adelantado el problema y retrasado la sintaxis en semana 01.
2. **Código sin validación de motor:** muchas salidas están indicadas como esperadas, pero aún requieren integración real.
3. **Cobertura de exámenes:** unos pocos cuestionarios no bastan para evaluar preparación oficial.
4. **Laboratorio continuo insuficiente:** hace falta acumular entregables y evolucionar el mismo catálogo de forma verificable.
5. **Avanzado esquemático:** todavía es necesario convertir 20–24 en clases completas con laboratorios, no aumentar la longitud artificialmente.
6. **Datos y textos contradictorios:** se corrigió la explicación inicial de semana 14 porque las dos fichas iniciales sí incluyen títulos; el error se introduce después para el test negativo.
7. **Especializaciones no equivalen a certificación:** disponer de una guía de Protégé/GraphDB no valida competencia operativa.

## Prioridad ejecutable de mejora

1. **Cerrar fundamentos 01–07:** probar y corregir código, ejercicios completos, práctica inédita y pruebas de integración en AuraDB.
2. **Cerrar ontologías 11–14 y talleres:** proyectos de RDF desde CSV, SKOS, OWL con razonador y SHACL en GraphDB.
3. **Cerrar ArcadeDB y arquitectura 08–10 / 15–17:** tests versionados y arquitectura híbrida reproducible.
4. **Construir 20–24 desde cero:** búsqueda semántica, GraphRAG, aplicación, seguridad y defensa.
5. **Evaluar alumnos:** comparar resultados antes y después, examinar autonomía sin ayudas, corregir contenidos donde fallen.

## Criterio final

**No declarar «experto» al alumno por completar 24 páginas**. El mínimo es una evaluación donde reciba datos y requisitos nuevos y pueda construir, probar, explicar y defender la solución. Documentar también los límites del sistema es parte del resultado.

_Actualizada el 14 de octubre de 2026. Datos de ejemplo siempre ficticios; jamás publicar información interna en repositorio público._
