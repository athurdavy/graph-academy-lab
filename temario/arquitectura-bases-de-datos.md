# Arquitectura: Neo4j, PostgreSQL, ORM/OGM y RDF

![Arquitectura de la biblioteca de prácticas](../assets/arquitectura-biblioteca.svg)

**Caso público ficticio:** biblioteca digital. Este documento responde a las decisiones que aparecen al construir una aplicación de verdad.

## 1. ¿Neo4j permite varias bases de datos?

**Sí, en ediciones y planes compatibles.** Según la documentación actual de Neo4j Aura, **AuraDB Business Critical** y **AuraDB Virtual Dedicated Cloud** permiten varias bases de datos de usuario dentro de una instancia cuando se activa esta capacidad al crearla. No se puede activar después en una instancia existente. Las bases nuevas se gestionan desde Aura Console o Aura API, **no** mediante comandos Cypher de administración en Aura. Las bases de una misma instancia comparten recursos de computación y memoria.

**No presupongas que AuraDB Free o Professional permiten esta característica.** Tampoco confundas una **instancia** (infraestructura de servicio), una **base de datos** (espacio de datos) y un **grafo lógico** (modelo de nodos y relaciones dentro de una base).

Fuente oficial: [Neo4j Aura: múltiples bases de datos](https://neo4j.com/docs/aura/managing-instances/multiple-databases/).

## 2. Tres arquitecturas válidas

### Opción A — Solo Neo4j

\`API Python → Neo4j\`

**Cuándo elegirla:** consultas centradas en patrones y recorridos; poco valor adicional al introducir otra base.

**Carencia que debes aceptar:** Neo4j no se convierte automáticamente en un almacén RDF con inferencia OWL completa por guardar nodos etiquetados como conceptos. Hay que diseñar explícitamente interoperabilidad y validación.

### Opción B — PostgreSQL + Neo4j

\`API Python → PostgreSQL (catálogo transaccional)\` y \`API Python → Neo4j (relaciones y exploración)\`

**Ventajas:** integridad relacional madura y patrones de recorrido expresivos.

**Costes:** dos sistemas, duplicación parcial, sincronización, observabilidad y fallos intermedios.

**Importante:** una transacción de PostgreSQL no es automáticamente atómica con otra de Neo4j. Define una fuente de verdad y usa mecanismos como outbox transaccional, reintentos idempotentes y reconciliación para mantener proyecciones coherentes.

### Opción C — RDF + aplicación

\`API Python → RDFLib / almacén RDF → SPARQL y SHACL\`

**Cuándo elegirla:** interoperabilidad RDF y semántica formal son requisitos centrales.

**No presupongas** que GraphDB, Fuseki, Blazegraph, RDFLib y Neo4j implementan exactamente las mismas capacidades ni el mismo nivel de inferencia.

## 3. ¿ORM, OGM o driver directo?

| Tecnología | Papel principal | Límite |
|---|---|---|
| SQLAlchemy ORM | Objetos Python ↔ modelo relacional | No es ORM nativo de Neo4j |
| Neo4j Python Driver | Cypher, sesiones, transacciones | No es ORM |
| neomodel | OGM de Python para Neo4j | Abstracción adicional y dependencia de compatibilidad |
| RDFLib | Modelo RDF, Turtle, SPARQL local | No equivale a razonamiento OWL completo |

**Recomendación formativa:** empieza con el driver oficial, Cypher explícito y pruebas. Adopta OGM cuando conozcas las consultas y una abstracción aporte más de lo que oculta.

Fuentes: [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/), [Neo4j Driver](https://neo4j.com/docs/python-manual/current/), [neomodel](https://neomodel.readthedocs.io/), [RDFLib](https://rdflib.readthedocs.io/).

## 4. Cómo organizar un proyecto mantenible

\`\`\`text
biblioteca/
├── pyproject.toml
├── .env.example
├── src/biblioteca/
│   ├── domain/               # Entidades y reglas sin detalles de BBDD
│   ├── services/             # Casos de uso: registrar lectura, buscar libro
│   ├── repositories/         # Interfaces y adaptadores de persistencia
│   │   ├── neo4j_libros.py
│   │   └── postgres_libros.py
│   ├── api/                  # Endpoints web
│   └── config.py
├── ontologias/
│   ├── biblioteca.ttl
│   └── shapes.ttl
├── scripts/
│   └── importar.py
└── tests/
    ├── unit/
    └── integration/
\`\`\`

No crees directorios «por arquitectura» si todavía no tienen responsabilidad real: este es un esquema al que puedes evolucionar.

## 5. Un patrón de repositorio sencillo

\`\`\`python
class LibroRepository:
    def __init__(self, driver, database: str = "neo4j"):
        self.driver = driver
        self.database = database

    def buscar_por_isbn(self, isbn: str):
        rows, _, _ = self.driver.execute_query(
            """
            MATCH (l:Libro {isbn:$isbn})
            RETURN l.isbn AS isbn, l.titulo AS titulo
            """,
            isbn=isbn,
            database_=self.database,
        )
        return rows[0].data() if rows else None
\`\`\`

En Neo4j es recomendable especificar \`database_\` explícitamente, incluso con una sola base, para evitar un viaje extra al servidor para determinar la base predeterminada.

Fuente: [Neo4j Driver: query configuration](https://neo4j.com/docs/python-manual/current/query-simple/).

## 6. Buenas decisiones y antipatrones

- **Antipatrón:** mezclar rutas HTTP, lógica de negocio y Cypher concatenado en el mismo archivo.
- **Antipatrón:** suponer transacciones distribuidas automáticas entre Neo4j y SQL.
- **Antipatrón:** conectar a producción desde notebooks de prueba con permisos de escritura.
- **Antipatrón:** escoger OGM para evitar aprender Cypher.
- **Buena práctica:** consultas parametrizadas, restricciones, migraciones versionadas, logs sin secretos, pruebas de integración, índices medidos mediante EXPLAIN/PROFILE.
- **Buena práctica:** distinguir datos operativos, vocabularios RDF y proyecciones de consulta.

## 7. Ejercicios de diseño

1. Diseña una solución solo Neo4j y argumenta por qué no necesitas PostgreSQL.
2. Diseña una solución híbrida. Decide cuál guarda el registro canónico de cada libro.
3. Imagina que SQL confirma una actualización y Neo4j no: describe compensación/reintento.
4. Modela el flujo API → Servicio → Repositorio → Driver con clases Python.
5. ¿Qué diferencia hay entre guardar varios subgrafos etiquetados y tener varias bases aisladas?

## Referencias

- [Neo4j Aura: múltiples bases de datos](https://neo4j.com/docs/aura/managing-instances/multiple-databases/)
- [Driver Python oficial](https://neo4j.com/docs/python-manual/current/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [SHACL W3C](https://www.w3.org/TR/shacl/)
