# Semana 17 — Arquitectura práctica y decisiones de persistencia

![Arquitectura ficticia de la biblioteca](../assets/arquitectura-biblioteca.svg)

**Lectura central:** [Arquitectura: Neo4j, PostgreSQL, ORM/OGM y RDF](arquitectura-bases-de-datos.md).

## 1. Separación de responsabilidades

- **API:** recibe y valida peticiones.
- **Servicio:** expresa el caso de uso («registrar una lectura»).
- **Repositorio:** encapsula consultas y acceso al motor.
- **Infraestructura:** driver, sesiones, configuración y observabilidad.
- **Dominio:** conceptos y reglas que deberían sobrevivir a un cambio de base.

## 2. Fuente de verdad

Si duplicas datos en PostgreSQL y Neo4j, decide **dónde se escribe** cada entidad y cuál es una **proyección derivada**. Sin esa decisión aparecen actualizaciones contradictorias.

## 3. Ejercicio Python

Define una interfaz mínima:

\`\`\`python
from typing import Protocol

class CatalogoRepository(Protocol):
    def buscar_por_isbn(self, isbn: str) -> dict | None:
        ...

class BuscarLibro:
    def __init__(self, repo: CatalogoRepository):
        self.repo = repo

    def ejecutar(self, isbn: str) -> dict | None:
        if not isbn.strip():
            raise ValueError("ISBN vacío")
        return self.repo.buscar_por_isbn(isbn)
\`\`\`

Ahora implementa un repositorio en memoria para tests y otro con Neo4j. La lógica de \`BuscarLibro\` no cambia.

## 4. ¿ORM u OGM?

SQLAlchemy ORM modela datos relacionales. neomodel es un OGM para Neo4j. El driver Python oficial consulta directamente con Cypher. Elige después de entender los patrones de acceso. **Ninguno elimina la necesidad de modelar ni de medir consultas.**

## 5. Ejercicios

1. Crea dos adaptadores que cumplan el protocolo.
2. Prueba \`BuscarLibro\` usando uno falso en memoria.
3. Haz una tabla de responsabilidades SQL/Neo4j/RDF.
4. Define estrategia de reconciliación si hay dos bases.
5. Diseña manejo de secretos y permisos mínimos.

## Fuentes

- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Arquitectura de múltiples BBDD](arquitectura-bases-de-datos.md)
