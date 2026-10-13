# Semana 17 — Arquitectura práctica y decisiones de persistencia

![Arquitectura ficticia de la biblioteca](../assets/arquitectura-biblioteca.svg)

**Lectura central:** [Arquitectura: Neo4j, PostgreSQL, ORM/OGM y RDF](arquitectura-bases-de-datos.md).

## Antes de escribir clases Python: qué es una arquitectura

Una **arquitectura de software** es una forma documentada de repartir responsabilidades. No es simplemente dibujar cajas. En nuestra biblioteca, la función «buscar libros de Grafos» tiene varios trabajos distintos:

1. Recibir la petición (por ejemplo, de una página o API).
2. Comprobar que «GRAFOS» es un código válido y no una entrada vacía.
3. Pedir libros a una capa de acceso a datos.
4. Ejecutar Cypher o SQL en el motor elegido.
5. Devolver un resultado coherente o explicar el error.

### Qué significan estos términos antes del diagrama

| Palabra | Explicación |
|---|---|
| API | Interfaz por la que una aplicación ofrece operaciones a otra |
| Dominio | Entidades y reglas de la biblioteca, independientemente del motor |
| Servicio | Coordina una tarea o caso de uso del dominio |
| Repositorio | Contrato que define cómo solicitar o guardar entidades |
| Adaptador | Implementación concreta del contrato para Neo4j, SQL o memoria |
| Driver | Biblioteca de conexión al motor |
| ORM | *Object-Relational Mapper*: mapea objetos a tablas relacionales |
| OGM | *Object-Graph Mapper*: mapea objetos a estructuras de grafo |
| Fuente de verdad | Sistema que determina qué versión de los datos se considera principal |

### Ejemplo completo en Python, sin servidor

```python
class RepositorioMemoria:
    def __init__(self):
        self.libros = {
            "ISBN-001": {"isbn": "ISBN-001", "titulo": "El mapa de los grafos"}
        }

    def buscar_por_isbn(self, isbn):
        return self.libros.get(isbn)

class BuscarLibro:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def ejecutar(self, isbn):
        if not isbn or not isbn.strip():
            raise ValueError("Debes proporcionar un ISBN")
        return self.repositorio.buscar_por_isbn(isbn)

servicio = BuscarLibro(RepositorioMemoria())
print(servicio.ejecutar("ISBN-001"))
print(servicio.ejecutar("ISBN-NO-EXISTE"))
```

**Esperado:** primero un diccionario con ISBN y título; después `None`. El servicio **no conoce** las consultas Neo4j y, aun así, ejecuta su caso de uso.

**Ejercicio:** implementa otro adaptador con datos en una lista Python. Si tienes que modificar la clase BuscarLibro para hacerlo, revisa la separación de responsabilidades.

### Qué NO resuelve este diseño automáticamente

Separar responsabilidades no garantiza una transacción atómica entre PostgreSQL y Neo4j. Si escribes en dos motores, documenta **dónde está la fuente de verdad**, cómo propagas cambios y cómo detectas o reconcilias desfases.


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

```python
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
```

Ahora implementa un repositorio en memoria para tests y otro con Neo4j. La lógica de `BuscarLibro` no cambia.

## 4. ¿ORM u OGM?

SQLAlchemy ORM modela datos relacionales. neomodel es un OGM para Neo4j. El driver Python oficial consulta directamente con Cypher. Elige después de entender los patrones de acceso. **Ninguno elimina la necesidad de modelar ni de medir consultas.**

## 5. Ejercicios

1. Crea dos adaptadores que cumplan el protocolo.
2. Prueba `BuscarLibro` usando uno falso en memoria.
3. Haz una tabla de responsabilidades SQL/Neo4j/RDF.
4. Define estrategia de reconciliación si hay dos bases.
5. Diseña manejo de secretos y permisos mínimos.

## Fuentes

- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Arquitectura de múltiples BBDD](arquitectura-bases-de-datos.md)

## Soluciones y verificación de la práctica

**Comprensión:** explica con una situación de la biblioteca la diferencia entre una afirmación guardada y un dato confiable. **Aplicación:** cambia un registro ficticio o un adaptador en memoria, predice el resultado y verifica lo observado. **Límite:** un test local correcto no verifica datos del mundo real ni las transacciones de otros motores.

**Criterio para avanzar:** debes poder justificar la decisión técnica y reproducir el ejemplo, no solo repetir los términos. Registra preguntas que no sepas contestar para reforzarlas antes del siguiente bloque.
