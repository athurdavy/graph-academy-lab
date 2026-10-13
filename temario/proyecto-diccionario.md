# Proyecto transversal — Diccionario semántico

## Problema de ejemplo

Una organización usa nombres distintos para el mismo concepto de negocio: «cliente», «customer», «titular». Sus sistemas contienen campos como `crm.customer_id` y `billing.account_holder`. El objetivo es describir conceptos, sus etiquetas y relaciones con activos de datos **sin asumir que todos los términos sean sinónimos**.

## Requisitos iniciales a validar

1. Conceptos con identificador estable, definición y etiquetas por idioma.
2. Responsables, fuente y estado editorial.
3. Relaciones jerárquicas y asociativas justificadas.
4. Mapeos explícitos a tablas/campos.
5. Búsqueda por etiqueta y por relación.
6. Historial de cambios y validación.

## Modelo conceptual candidato

- Concepto
- Etiqueta
- Fuente
- ActivoDeDatos
- Mapeo
- Responsable

Relaciones candidatas: `TIENE_ETIQUETA`, `MAPEA_A`, `RESPONSABLE_DE`, `RELACIONADO_CON`. Son **propuestas**, no requisitos confirmados.

## Iteraciones

- **Semanas 1–3:** modelar el dominio sin depender de una base de datos.
- **Semanas 4–10:** comparar persistencia en Neo4j y ArcadeDB.
- **Semanas 11–17:** evaluar SKOS, RDF, OWL y SHACL según necesidades.
- **Semanas 18–21:** valorar IA solo si aporta valor verificable.
- **Semanas 22–24:** integrar, probar y documentar.

## Criterios de aceptación de ejemplo

- Una consulta recupera un concepto por etiqueta alternativa.
- Cada mapeo tiene procedencia.
- Los identificadores son estables frente a cambios de nombre.
- Los conceptos pendientes de revisión se distinguen de los aprobados.
- Los resultados de búsqueda no confunden coincidencia textual con equivalencia semántica.

## Lecturas

- [SKOS Primer](https://www.w3.org/TR/skos-primer/)
- [SHACL](https://www.w3.org/TR/shacl/)
- [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/)
