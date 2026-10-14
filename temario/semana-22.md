# Semana 22 — De consultas sueltas a una API: construir un servicio Python

**Antes:** [semana 07, driver Neo4j](semana-07.md), [semana 17, arquitectura](semana-17.md), [semana 21, recuperación](semana-21.md). **Después:** [semana 23, pruebas y seguridad](semana-23.md).

**Objetivo:** comprender por qué una aplicación necesita separar entrada, reglas y acceso a datos; construir una pequeña API desde cero; diferenciar casos de éxito, ausencia y error sin ocultar fallos.

## 1. El problema real antes de instalar nada

Hasta ahora has ejecutado consultas en una consola o un script Python. Pero una aplicación externa quiere preguntar:

> «¿Qué libros de nuestra biblioteca ficticia tratan sobre Grafos?»

No puede depender de que alguien abra Neo4j Browser y copie el resultado manualmente. Necesitamos un **servicio** que reciba solicitudes y devuelva resultados de forma predecible.

### Cinco palabras que debes entender

| Palabra | Explicación | En nuestro ejemplo |
|---|---|---|
| Cliente | Programa que solicita información | Navegador o aplicación |
| Servidor | Programa que recibe y procesa solicitudes | API de biblioteca |
| API | Interfaz programable con operaciones documentadas | Consultar libros por tema |
| HTTP | Protocolo de solicitudes y respuestas web | GET /libros?tema=GRAFOS |
| JSON | Formato textual de objetos y listas | Lista de libros con isbn y título |
| Endpoint | Dirección y operación concreta de la API | GET /libros |
| Código de estado | Número que describe el resultado HTTP | 200, 400, 500 |

**Importante:** el valor HTTP 200 significa que la solicitud se procesó correctamente según el contrato; no prueba que los datos devueltos sean verdaderos.

## 2. El flujo que vamos a construir

```text
Cliente web
  → GET /libros?tema=GRAFOS
  → Validación de entrada
  → Servicio de biblioteca
  → Repositorio de datos
  → Lista de libros
  → Respuesta JSON
```

Primero probaremos un repositorio **en memoria**. Así aprenderás qué responsabilidades tiene cada capa sin confundir errores de código con fallos de Neo4j o de la red.

## 3. Instalar FastAPI y un servidor de desarrollo

**FastAPI** es un framework de Python para construir APIs web. **Uvicorn** es un servidor de aplicaciones que puede ejecutar una aplicación FastAPI.

En un entorno virtual de pruebas:

```bash
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
python -m pip install fastapi uvicorn pytest httpx
```

Si estás en Windows, activa el entorno mediante el comando apropiado para PowerShell o tu terminal. Para este primer ejemplo no necesitas conectar credenciales de Neo4j.

## 4. Tu primera API completa, sin base de datos

Guarda este archivo como `app_biblioteca.py` en tu equipo:

```python
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Biblioteca de prácticas")

CATALOGO = [
    {"isbn": "ISBN-001", "titulo": "El mapa de los grafos", "tema": "GRAFOS"},
    {"isbn": "ISBN-002", "titulo": "Rutas de conocimiento", "tema": "GRAFOS"},
    {"isbn": "ISBN-003", "titulo": "Historias del océano", "tema": "NATURALEZA"},
]

def buscar_por_tema(tema: str) -> list[dict]:
    return [libro for libro in CATALOGO if libro["tema"] == tema]

@app.get("/libros")
def listar_libros(tema: str = Query(min_length=1)):
    resultados = buscar_por_tema(tema)
    return {"tema": tema, "libros": resultados}
```

Ejecuta:

```bash
uvicorn app_biblioteca:app --reload
```

Abre en tu navegador: `http://127.0.0.1:8000/libros?tema=GRAFOS`.

**Resultado esperado:** un objeto JSON con la propiedad `tema` y una lista de dos libros.

### Entiende cada instrucción

1. `FastAPI()` crea la aplicación web.
2. `CATALOGO` es una lista ficticia local; no conecta a ningún motor externo.
3. `buscar_por_tema` separa la consulta lógica de la capa HTTP.
4. `@app.get("/libros")` registra la ruta GET.
5. `Query(min_length=1)` indica que el parámetro debe estar presente y contener al menos un carácter.
6. `return` crea la respuesta que FastAPI serializa como JSON.

No has construido una «plataforma profesional» en 20 líneas: has construido **una primera API comprensible y comprobable**.

## 5. Ausencia de resultados no es fallo del servidor

Prueba `http://127.0.0.1:8000/libros?tema=DESCONOCIDO`.

**Esperado:** una respuesta válida con lista vacía:

```json
{"tema": "DESCONOCIDO", "libros": []}
```

El servicio ha podido procesar la solicitud. No existe una coincidencia en el catálogo.

Ahora prueba quitar el parámetro `tema`. FastAPI debe producir una respuesta de **error de validación** según su configuración. Eso es diferente de una lista vacía.

En una API real documenta qué errores representan problemas del cliente y cuáles fallos internos o indisponibilidad de datos.

## 6. ¿Cómo sustituir memoria por Neo4j?

En la [semana 07](semana-07.md) aprendiste a buscar libros con el driver oficial:

```python
def buscar_libros_por_tema(driver, codigo: str, database: str):
    records, _, _ = driver.execute_query(
        """
        MATCH (l:Libro)-[:TRATA_SOBRE]->(t:Tema {codigo:$codigo})
        RETURN l.isbn AS isbn, l.titulo AS titulo
        ORDER BY titulo
        """,
        codigo=codigo,
        database_=database,
    )
    return [record.data() for record in records]
```

Puedes crear un adaptador que implemente un contrato de búsqueda común. Así la ruta web **no necesita saber Cypher**, y tus tests pueden utilizar memoria o dobles de prueba.

Pero **no** debes abrir un driver por cada petición, guardar contraseñas en el código ni asumir que un fallo de Neo4j equivale a «no hay libros».

## 7. Primer test automático de la API

Crea `test_app_biblioteca.py` en la misma carpeta:

```python
from fastapi.testclient import TestClient
from app_biblioteca import app

cliente = TestClient(app)

def test_libros_de_grafos():
    respuesta = cliente.get("/libros", params={"tema": "GRAFOS"})
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert len(datos["libros"]) == 2
    assert {x["isbn"] for x in datos["libros"]} == {"ISBN-001", "ISBN-002"}

def test_tema_desconocido():
    respuesta = cliente.get("/libros", params={"tema": "DESCONOCIDO"})
    assert respuesta.status_code == 200
    assert respuesta.json()["libros"] == []

def test_falta_tema():
    respuesta = cliente.get("/libros")
    assert respuesta.status_code == 422
```

Ejecuta `python -m pytest -q` desde la carpeta donde guardaste ambos archivos.

**Qué evalúan las pruebas:** éxito con dos registros, lista vacía válida y error de entrada. **Qué NO evalúan:** red, autenticación, transacciones o consultas reales de Neo4j.

## 8. Errores que cometería un principiante (y cómo detectarlos)

| Error | Consecuencia | Corrección |
|---|---|---|
| Concatenar entrada del usuario dentro de Cypher | Consultas inseguras o mal formadas | Parámetros ``$codigo`` |
| Abrir driver en cada solicitud | Recursos mal gestionados | Ciclo de vida por aplicación |
| `except Exception: return []` | Ocultar problemas de red | Manejar errores explícitos |
| Entregar toda la base a cualquier usuario | Riesgo de divulgación | Autenticación y permisos |
| Probar solo el camino feliz | Fallos no detectados | Pruebas negativas |
| Exponer la API de desarrollo públicamente | Configuración insegura | Revisar despliegue y seguridad antes de publicar |

## 9. Ejercicios con soluciones orientativas

1. Añade un filtro opcional por año y especifica qué ocurre si no se envía.
2. Crea el endpoint `GET /libros/{isbn}` y devuelve 404 cuando el libro no exista.
3. Refactoriza el catálogo de memoria a una clase repositorio.
4. Escribe tests para éxito, ausencia, entrada inválida y error simulado del repositorio.
5. Propón qué información de errores deberías registrar sin incluir credenciales.

### Solución orientativa al ejercicio 2

```python
@app.get("/libros/{isbn}")
def obtener_libro(isbn: str):
    for libro in CATALOGO:
        if libro["isbn"] == isbn:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")
```

**Explicación:** la URL identifica un libro concreto; 404 es adecuado cuando el recurso solicitado no está disponible según el contrato. Una consulta por tema que devuelve cero coincidencias puede, en cambio, responder 200 con una lista vacía.

## 10. Examen de salida

Recibes un catálogo nuevo con cinco libros y debes desarrollar una API que responda tres preguntas, valide parámetros, devuelva datos estructurados y pase pruebas con un caso negativo. Después justifica cómo reemplazarías el repositorio de memoria por Neo4j sin reescribir la lógica HTTP.

**Siguiente:** [semana 23 — pruebas, rendimiento y seguridad](semana-23.md).

## Fuentes oficiales

- [FastAPI: primer tutorial](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [FastAPI: parámetros de consulta](https://fastapi.tiangolo.com/tutorial/query-params/)
- [FastAPI: testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)

**Estado:** API y tests propuestos para ejecución local; integración real con Neo4j y despliegue seguro todavía pendientes, no declarar producción validada.
