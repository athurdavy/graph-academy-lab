# Semana 22 — Integración: API, importación y consultas completas

**Caso:** biblioteca digital ficticia · **Dedicación sugerida:** 8–10 horas.

## Objetivos de la unidad

- Entender las decisiones técnicas, sus límites y sus costes.
- Reproducir el ejemplo sin datos ni credenciales reales.
- Aplicar el tema al proyecto público de biblioteca y justificar resultados.
- Crear pruebas y documentación antes de declarar la funcionalidad terminada.

## 1. Fundamentos

Una aplicación útil incluye entrada de datos, reglas de negocio, persistencia, APIs y pruebas. En el caso de la biblioteca, decide si el catálogo se mantiene solo en Neo4j o también existe una fuente relacional. Evita incorporar una segunda base sin justificarlo. La migración debe poder repetirse y las credenciales nunca entran en el repositorio. Un endpoint público de lectura necesita paginación, manejo de errores y limitaciones de consulta.

## 2. Ejemplo comentado

```python
from typing import Protocol

class Books(Protocol):
    def find_by_topic(self, topic: str, limit: int) -> list[dict]: ...

class Catalog:
    def __init__(self, books: Books): self.books = books
    def search(self, topic: str, limit: int = 20):
        if not topic or limit < 1 or limit > 100:
            raise ValueError('Parámetros inválidos')
        return self.books.find_by_topic(topic, limit)
```

**Qué debes verificar:** identifica de dónde sale cada dato, cuáles son los supuestos de la consulta o función y qué ocurriría ante una entrada inesperada. El ejemplo es una base para experimentar; no sustituye pruebas de integración con la infraestructura usada.

## 3. Laboratorio práctico

Implementa dos endpoints ficticios, GET /libros/{isbn} y GET /temas/{codigo}/libros, con pruebas de límites, ausencia de resultados e identificadores inexistentes.

**Evidencias a guardar:** fichero fuente, casos de entrada, resultado esperado, resultado obtenido y explicación de discrepancias. Usa únicamente identidades y datos inventados.

## 4. Preguntas de autoevaluación

1. ¿Qué problema resuelve esta tecnología y cuál no?
2. ¿Cómo sabes que la salida es correcta y no solo plausible?
3. ¿Qué errores o datos incompletos afectarían al resultado?
4. ¿Qué alternativa más sencilla usarías y por qué?
5. ¿Cómo documentarías el método para que otra persona lo reproduzca?

## 5. Criterios de entrega

- [ ] El ejemplo ejecuta en un entorno controlado, o queda documentada la dependencia que lo impide.
- [ ] Las hipótesis están separadas de los hechos comprobados.
- [ ] Hay pruebas al menos de un caso correcto y un caso límite.
- [ ] No se publican secretos ni información privada.
- [ ] Las fuentes externas se citan y se identifica la versión usada.

## Referencias

- [FastAPI](https://fastapi.tiangolo.com/)
- [Neo4j Driver](https://neo4j.com/docs/python-manual/current/)
