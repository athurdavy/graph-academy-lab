# Semana 17 — Arquitectura desde cero: separar lo que hace la aplicación de dónde guarda los datos

![Esquema de arquitectura para una biblioteca ficticia](../assets/arquitectura-biblioteca.svg)

**Antes:** [semana 07 — Neo4j desde Python](semana-07.md), [semana 15 — calidad](semana-15.md) y [semana 16 — procedencia](semana-16.md). **Después:** [semana 18](semana-18.md). Tiempo orientativo: 8–12 horas.

**Objetivo:** construir un caso de uso Python que funcione sin base de datos, entender por qué los repositorios permiten cambiar el almacenamiento y detectar qué problemas permanecen al combinar PostgreSQL, Neo4j y RDF.

## 1. El problema cotidiano: ¿dónde pongo esta función?

Tu aplicación de biblioteca tiene una operación:

> «Dame el libro con ISBN-001».

Hoy lo guardas en memoria, mañana en Neo4j y después quizá necesites mantener los registros maestros en PostgreSQL. ¿Tendrás que reescribir toda la aplicación cada vez?

**No, si has separado las responsabilidades.** Esa separación es una decisión de **arquitectura**: qué parte se encarga de cada trabajo, y por qué.

Dibújalo en palabras:

```text
Una persona pide un ISBN
       |
       v
CASO DE USO «ConsultarLibro»
       |
       v
REPOSITORIO: contrato de búsqueda
       |
       +--> memoria para aprender y probar
       +--> Neo4j para integración de grafos
       +--> PostgreSQL para almacenamiento relacional
```

Las flechas muestran **dependencias lógicas**, no una instalación concreta. No necesitas utilizar tres motores a la vez.

## 2. Cinco palabras que debes conocer

| Término | Definición sencilla | En nuestra biblioteca |
|---|---|---|
| Dominio | Entidades y reglas del problema | Libro e ISBN |
| Caso de uso | Acción de la aplicación para lograr algo | Consultar un libro |
| Repositorio | Contrato de acceso a entidades sin mostrar detalles de almacenamiento | Buscar por ISBN |
| Adaptador | Implementación concreta de ese contrato | Memoria o Neo4j |
| Driver | Librería que conecta con un motor externo | Neo4j Python Driver |
| Dependencia | Objeto o servicio que otra parte necesita | ConsultarLibro necesita repositorio |

**ORM** (*Object-Relational Mapper*) facilita ciertas interacciones entre objetos Python y bases relacionales. **OGM** (*Object-Graph Mapper*) cumple una función análoga con ciertos modelos de grafos. **Ninguno reemplaza la comprensión de las consultas y del modelo.**

## 3. Primero un ejemplo que puedas ejecutar sin credenciales

Nuestro repositorio incluye [servicios.py](../laboratorios/servicios.py). Léelo antes de este fragmento:

```python
from laboratorios.servicios import (
    Libro, RepositorioMemoria, ConsultarLibro,
)

libros = [
    Libro("ISBN-001", "El mapa de los grafos"),
    Libro("ISBN-002", "Rutas de conocimiento"),
]

repositorio = RepositorioMemoria(libros)
caso = ConsultarLibro(repositorio)

print(caso.ejecutar("ISBN-001"))
print(caso.ejecutar("ISBN-999"))
```

**Resultado esperado:**

```text
Libro(isbn='ISBN-001', titulo='El mapa de los grafos')
None
```

### ¿Por qué funciona sin base de datos?

- `Libro` es un tipo Python que expresa los datos básicos del dominio.
- `RepositorioMemoria` utiliza un diccionario y entiende cómo buscar.
- `ConsultarLibro` solo conoce la operación de búsqueda, no SQL ni Cypher.
- `ejecutar` valida la entrada; ante un identificador vacío, lanza `ValueError`.
- `None` representa ausencia de entidad. **No es** un error de red.

## 4. ¿Qué es un contrato en Python?

Python permite usar **Protocol**, una forma de describir qué métodos debe proporcionar un objeto.

```python
from typing import Protocol

class LibroRepository(Protocol):
    def buscar(self, isbn: str) -> Libro | None:
        ...
```

No hace falta heredar obligatoriamente de `LibroRepository` para que un objeto cumpla su forma estructural: si implementa un método compatible `buscar`, puede encajar en ese contrato para comprobaciones estáticas y diseño.

**Diferencia importante:** las anotaciones de tipos de Python no crean automáticamente una validación de datos en tiempo de ejecución. Para comprobar entradas reales necesitas código de validación y tests.

## 5. Pruebas unitarias: aprende sin depender de AuraDB

Ejecuta desde la raíz:

```bash
python -m pip install -r laboratorios/requirements.txt
python -m pytest laboratorios/tests/test_servicios.py -q
```

Estas pruebas verifican:

1. Se encuentra un ISBN conocido.
2. Un ISBN inexistente devuelve `None`.
3. Un identificador vacío se rechaza.
4. Los espacios de los extremos se eliminan antes de buscar.

**No verifican** un servidor Neo4j: eso requiere pruebas de integración.

### Experimento de aprendizaje

Cambia el resultado de un repositorio de memoria para que devuelva un libro diferente. ¿Debe cambiar la lógica de la clase `ConsultarLibro`? No, siempre que el adaptador siga cumpliendo su contrato y entregue el tipo de dato esperado.

## 6. Añadir el adaptador de Neo4j sin acoplar el servicio

En una aplicación real podrías escribir:

```python
class RepositorioNeo4j:
    def __init__(self, driver, database="neo4j"):
        self.driver = driver
        self.database = database

    def buscar(self, isbn: str):
        records, _, _ = self.driver.execute_query(
            """
            MATCH (l:Libro {isbn:$isbn})
            RETURN l.isbn AS isbn, l.titulo AS titulo
            """,
            isbn=isbn,
            database_=self.database,
        )
        if not records:
            return None
        return Libro(
            isbn=records[0]["isbn"],
            titulo=records[0]["titulo"],
        )
```

**Léelo en orden:**

- El adaptador recibe un driver ya configurado: **no abre una conexión en cada búsqueda**.
- `execute_query` ejecuta una consulta Cypher parametrizada.
- Si no hay filas devuelve `None`, como el repositorio de memoria.
- Si hay resultado construye un objeto `Libro` del dominio.
- Si el driver lanza un error de red, no lo convertimos silenciosamente en `None`.

El ejemplo presupone que `Libro` está importado desde el dominio. Para ejecutarlo de extremo a extremo necesitas el driver instalado, un dataset Neo4j cargado y pruebas de integración.

## 7. ¿Y dónde entra PostgreSQL?

**PostgreSQL** es un motor de base de datos relacional. Puedes almacenar allí fichas bibliográficas que actúen como **fuente de verdad**: sistema que gobierna qué datos son oficiales en un contexto específico.

Neo4j podría contener una **proyección** de relaciones para consultas conectadas. *Proyección* significa una representación derivada del origen, no un segundo registro maestro independiente.

```text
PostgreSQL: libro oficial
    |
    v
Cambio registrado / evento
    |
    v
Proceso de sincronización
    |
    v
Neo4j: relaciones consultables
```

**Peligro:** una transacción SQL y una transacción Neo4j no forman automáticamente una transacción ACID conjunta. Si falla la sincronización debes registrar el cambio pendiente y poder reintentarlo sin crear duplicados.

## 8. Cómo sincronizar sin prometer magia

Un enfoque habitual es el **outbox transaccional**: registrar el cambio y un evento pendiente dentro de la misma transacción del sistema principal, y publicarlo después a un consumidor.

Pero el outbox no resuelve todo: el consumidor puede recibir un evento más de una vez, perder conexión o procesarlo fuera de orden. Necesitas:

- un ID estable para el evento;
- escritura idempotente en destino;
- reintentos con política;
- métricas de fallos;
- reconciliación entre origen y destino.

**Ejemplo:** «ISBN-001 tiene nuevo tema» debe poder aplicarse dos veces sin duplicar arbitrariamente la misma relación.

## 9. ¿Cuándo NO añadir dos bases de datos?

Si tu aplicación se resuelve bien con SQL y unas cuantas consultas sencillas, **agregar Neo4j solo por utilizar grafos introduce mantenimiento innecesario**.

Antes de decidir, pregunta:

- ¿Qué consultas reales son difíciles en el motor actual?
- ¿Qué volumen y latencia necesitamos?
- ¿Qué cuesta mantener backups, usuarios y monitorización de dos sistemas?
- ¿Cómo evitamos resultados desactualizados?
- ¿Qué herramientas y habilidades tiene el equipo?

Una comparación seria mide resultados; no presenta una preferencia tecnológica como verdad universal.

## 10. Ejercicios graduados

1. Ejecuta `ConsultarLibro` con repositorio en memoria y explica por qué devuelve `None` para un ISBN desconocido.
2. Modifica el repositorio para que encuentre libros por título. ¿Debería cambiar el contrato?
3. Escribe un test para ISBN vacío.
4. Implementa un repositorio de lectura sobre una lista de diccionarios con el mismo contrato.
5. Diseña una prueba de contrato que ejecutarías tanto contra memoria como contra Neo4j.
6. Describe qué ocurre si PostgreSQL confirma un cambio y Neo4j está temporalmente caído.
7. Propón cómo recuperarías esa inconsistencia sin reescribir manualmente los datos.

### Soluciones razonadas

**1.** La consulta no halló una entidad; `None` es una respuesta de dominio. No implica que el repositorio haya fallado.

**3.** Debes esperar `ValueError` y verificar que el repositorio no se invocó con una clave vacía.

**5.** Prueba casos de ISBN conocido, inexistente y formato de resultados idéntico en ambos adaptadores. Añade pruebas de error de red exclusivas de integración.

**6.** Debes identificar el cambio confirmado, conservar una tarea pendiente y reintentar la sincronización. No supongas una transacción distribuida automática.

## 11. Prueba de autonomía

Recibe un nuevo dataset ficticio. Escribe dos adaptadores con el mismo contrato, un caso de uso que no conozca el motor y tests para éxito, ausencia y error. Justifica si necesitas Neo4j, SQL, ambos o ninguno.

**Siguiente:** [semana 18 — qué convierte datos conectados en un grafo de conocimiento](semana-18.md).

## Fuentes oficiales

- [Python typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Neo4j transactions](https://neo4j.com/docs/python-manual/current/transactions/)

**Estado:** laboratorio en memoria y pruebas disponibles; integración Neo4j/PostgreSQL y reconciliación real todavía pendientes.
