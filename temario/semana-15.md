# Semana 15 — Validación, gobierno del dato y calidad

## Objetivo

Pasar de un grafo que «funciona» a uno cuya calidad pueda medirse y discutirse.

## Antes de la técnica: ¿qué significa que un dato sea de calidad?

Una base puede ejecutar correctamente una consulta y devolver un resultado **incorrecto en la realidad**. Supón que un registro afirma que Marina escribió un libro que en realidad escribió otra persona. Cypher puede encontrar y mostrar esa relación sin errores. **La consulta funciona; el dato es falso.**

Distingue las preguntas:

1. **¿Existe el dato?** Completitud: ¿un Libro tiene ISBN y título?
2. **¿Aparece varias veces?** Unicidad: ¿dos registros comparten indebidamente la misma clave?
3. **¿Las relaciones respetan nuestras reglas?** Consistencia: ¿ESCRIBIO conecta un Autor y un Libro?
4. **¿De dónde salió la afirmación?** Procedencia: ¿fue introducida manualmente o calculada?
5. **¿Cuándo se revisó?** Actualidad: una clasificación antigua puede estar desactualizada.

### Leer el Cypher de control

```cypher
MATCH (l:Libro)
WHERE l.isbn IS NULL
RETURN l.titulo AS titulo;
```

- `MATCH` encuentra nodos con etiqueta Libro.
- `WHERE` introduce la condición.
- `l.isbn` accede al valor de una propiedad del nodo.
- `IS NULL` pregunta si está ausente o tiene valor nulo.
- `RETURN` presenta los títulos.

**Resultado esperado:** en el dataset inicial de Neo4j, **cero filas**, porque los tres libros tienen ISBN. Un resultado vacío aquí indica que no se ha encontrado esa anomalía, **no** que toda la base esté perfecta.

### Ejercicio con una anomalía controlada

En una **base de pruebas**, añade un libro ficticio sin ISBN:

```cypher
CREATE (:Libro {titulo:'Ficha incompleta para practicar'});
```

Repite la consulta. Debe aparecer su título. **No crees un nodo incompleto en una base compartida o productiva.**

### Por qué un título duplicado no demuestra error

Dos libros diferentes podrían tener el mismo título. Si utilizas `count(*)` agrupando por título, identificas **candidatos a revisión**, no entidades que debas fusionar automáticamente. La identidad depende del criterio editorial y de una clave estable.

## Una primera política de datos comprensible

| Incidencia | Detección | Decisión orientativa |
|---|---|---|
| Libro sin ISBN | Consulta de ausencia | Rechazar o enviar a revisión según contrato |
| Dos registros con la misma clave de negocio | Agrupación por clave | Investigar antes de fusionar |
| Clasificación sin fuente | Control de procedencia | Marcarla como pendiente de revisión |
| Título duplicado | Informe de posibles coincidencias | No fusionar sin evidencias |
| Relación con tipo incorrecto | Consulta de extremos y etiquetas | Corregir datos bajo una política auditada |

**Ejercicio:** ¿qué controles pertenecen a una restricción de Neo4j, cuáles a un test Python y cuáles a una forma SHACL para RDF? Justifica cada elección con un caso concreto.


## 1. Dimensiones de calidad

- **Completitud:** registros con datos necesarios.
- **Unicidad:** claves duplicadas.
- **Consistencia:** relaciones y tipos que cumplen reglas.
- **Procedencia:** fuente de cada afirmación.
- **Actualidad:** frecuencia y fecha de verificación.
- **Validez semántica:** definiciones y relaciones justificadas.

Una consulta correcta sobre datos falsos produce una respuesta técnicamente correcta y conceptualmente incorrecta.

## 2. Comprobaciones Cypher

Buscar libros sin ISBN:

```cypher
MATCH (l:Libro)
WHERE l.isbn IS NULL
RETURN l.titulo AS libro;
```

Contar etiquetas duplicadas de ejemplo:

```cypher
MATCH (l:Libro)
WITH l.titulo AS titulo, count(*) AS cantidad
WHERE cantidad > 1
RETURN titulo, cantidad;
```

**Cuidado:** dos libros pueden compartir título sin ser el mismo libro. Esta consulta propone **candidatos a revisión**, no una corrección automática.

## 3. Validación en RDF

En el laboratorio de ontologías, SHACL exige un título y un ISBN de cada `ex:Libro`. Cambia un dato y ejecuta `validar.py`: comprueba que la validación detecta la desviación. Distingue reglas de negocio en la aplicación, restricciones nativas Neo4j y formas SHACL.

## 4. Flujo de revisión

Propuesta → verificación de fuente → revisión editorial → aprobación → publicación → seguimiento. Define quién puede aprobar y revertir decisiones.

## 5. Ejercicios

1. Diseña cinco reglas de calidad para la biblioteca.
2. Clasifica cada una como restricción Neo4j, test Python o shape SHACL.
3. Define qué ocurre si la carga falla a mitad.
4. Documenta quién corrige cada error y cómo queda trazado.

## Fuentes

- [SHACL](https://www.w3.org/TR/shacl/)
- [Neo4j Constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/)

## Soluciones y verificación de la práctica

**Comprensión:** explica con una situación de la biblioteca la diferencia entre una afirmación guardada y un dato confiable. **Aplicación:** cambia un registro ficticio o un adaptador en memoria, predice el resultado y verifica lo observado. **Límite:** un test local correcto no verifica datos del mundo real ni las transacciones de otros motores.

**Criterio para avanzar:** debes poder justificar la decisión técnica y reproducir el ejemplo, no solo repetir los términos. Registra preguntas que no sepas contestar para reforzarlas antes del siguiente bloque.
