# Semana 08 — ArcadeDB: arquitectura multimodelo

![Biblioteca ficticia](../assets/biblioteca-grafo.svg)

**Objetivo:** comprender por qué un sistema multimodelo no es «Neo4j con otro nombre» y comparar opciones de despliegue.

## 1. Modelo unificado de ArcadeDB

ArcadeDB dispone de estructuras orientadas a documento, grafo y otros patrones de acceso, con SQL extendido, Cypher y Gremlin, entre otras interfaces. Según su documentación, varios lenguajes acceden a los mismos registros subyacentes.

**No confundas** soportar Cypher con garantizar compatibilidad total de sintaxis, planes o funciones con cada versión de Neo4j. Para migrar consultas prepara pruebas de compatibilidad.

## 2. Escenario de biblioteca digital

Modelo candidato:

| Tipo de vértice | Identificador | Atributos |
|---|---|---|
| Libro | isbn | titulo, anio |
| Autor | id | nombre |
| Tema | codigo | nombre |

Tipos de arista: \`ESCRIBIO\` y \`TRATA_SOBRE\`. Mantén la dirección y los nombres documentados para comparar con Neo4j.

## 3. Laboratorio de desarrollo

Usa una instancia **local de pruebas** siguiendo las instrucciones oficiales de instalación de ArcadeDB. No conectes ejemplos a un servidor público ni uses una contraseña trivial en entornos expuestos.

En un entorno con base \`biblioteca\` creada, explora:

\`\`\`sql
CREATE VERTEX TYPE Libro;
CREATE VERTEX TYPE Autor;
CREATE EDGE TYPE ESCRIBIO;
\`\`\`

Después inserta vértices ficticios:

\`\`\`sql
CREATE VERTEX Libro SET isbn = 'ISBN-001', titulo = 'El mapa de los grafos';
CREATE VERTEX Autor SET id = 'A-001', nombre = 'Marina Soler';
\`\`\`

Para crear la relación en este modelo:

\`\`\`sql
CREATE EDGE ESCRIBIO
FROM (SELECT FROM Autor WHERE id = 'A-001')
TO (SELECT FROM Libro WHERE isbn = 'ISBN-001');
\`\`\`

Comprueba en la documentación de **la versión instalada** la sintaxis de creación de tipos, los índices y las APIs. Usa una base limpia al repetir el ejercicio de carga si no has incorporado lógica idempotente.

## 4. Decisiones y límites

- Una base multimodelo no evita diseñar relaciones y cardinalidades.
- No supone automáticamente interoperabilidad RDF ni razonamiento OWL.
- La seguridad incluye red, autenticación, permisos y ciclo de vida del servidor.
- Las diferencias entre motores deben medirse con la misma carga, cardinalidad y consultas.

## 5. Ejercicios

1. Diseña las consultas que debe soportar la biblioteca antes de decidir el motor.
2. Describe ventajas y costes de desplegar ArcadeDB local frente a AuraDB gestionado.
3. Explica por qué ejecutar una consulta Cypher no prueba equivalencia completa de motores.
4. Identifica los puntos de prueba: creación de tipos, índices, transacciones y conexiones Python.

## Documentación oficial

- [ArcadeDB: arquitectura multimodelo](https://docs.arcadedb.com/arcadedb/concepts/multi-model)
- [ArcadeDB: documentación](https://docs.arcadedb.com/)
