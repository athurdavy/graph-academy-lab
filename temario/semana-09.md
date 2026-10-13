# Semana 09 — Consultas y API de ArcadeDB con Python

**Objetivo:** ejecutar una consulta real con ArcadeDB utilizando su API HTTP y comprender la diferencia entre leer y escribir.

## Antes de programar: ¿qué es una API HTTP?

En la semana 08 creaste un libro en una base local. Ahora quieres **pedir ese libro desde un programa Python**.

- **Cliente:** tu programa Python, que solicita información.
- **Servidor:** ArcadeDB, que responde.
- **API:** reglas y direcciones que hacen posible solicitar operaciones.
- **HTTP** (*Hypertext Transfer Protocol*): protocolo por el que se envían peticiones y respuestas.
- **URL:** dirección que identifica el destino de una petición.
- **JSON** (*JavaScript Object Notation*): formato de datos estructurados que puede transportar una petición.

**Analogía:** tu programa es quien hace el pedido, el servidor es la cocina, la API es la carta que indica qué puedes pedir y con qué información.

| Símbolo o concepto | Qué significa |
|---|---|
| `POST` | Método HTTP que envía información al servidor |
| `localhost` | Este mismo ordenador, no un servidor público |
| `200` | Petición atendida correctamente en el caso habitual |
| `401` | No se acreditó correctamente la identidad |
| `403` | No se permite esa operación con los permisos actuales |
| `timeout` | Se acabó el tiempo de espera |
| `requests` | Biblioteca Python para enviar peticiones HTTP |

Antes del programa completo, lee este diccionario Python:

```python
peticion = {
    "language": "sql",
    "command": "SELECT FROM Libro",
}
```

Los dos puntos después de `"language"` y `"command"` son **la sintaxis de un diccionario Python**: separan clave y valor. **No** tienen el significado de `:Libro` en Cypher ni de `ex:Libro` en Turtle.

Nuestro recorrido será: configurar credenciales locales → componer URL → enviar JSON → comprobar errores HTTP → leer datos devueltos. **No publiques credenciales** y ejecuta la práctica contra una instancia ficticia de pruebas.

---

## 1. Consultas con SQL y grafos

ArcadeDB extiende SQL con recorridos de relaciones. Para listar los libros cargados:

```sql
SELECT FROM Libro;
```

La documentación oficial explica que el acceso puede hacerse por API HTTP/JSON, por controladores nativos y por protocolos compatibles. La elección del protocolo afecta a despliegue, autenticación y herramientas.

## 2. Cliente Python HTTP

La API oficial expone `POST /api/v1/query/{database}` para consultas de lectura. Esta práctica solo debe apuntar a tu instancia **local**:

```python
import os
import requests
from requests.auth import HTTPBasicAuth

url = os.getenv("ARCADEDB_URL", "http://localhost:2480")
db = os.getenv("ARCADEDB_DATABASE", "biblioteca")
user = os.environ["ARCADEDB_USER"]
password = os.environ["ARCADEDB_PASSWORD"]

response = requests.post(
    f"{url}/api/v1/query/{db}",
    auth=HTTPBasicAuth(user, password),
    json={"language": "sql", "command": "SELECT FROM Libro"},
    timeout=10,
)
response.raise_for_status()
print(response.json())
```

No guardes contraseñas en el repositorio. Para producción usa transporte protegido y la política de autenticación apropiada.

## 3. Driver oficial

ArcadeDB documenta `arcadedb-driver` para Python, generado desde OpenAPI. Si lo usas, fija una versión, documenta la API y comprueba cambios del cliente. Los ejemplos de los tutoriales pueden reflejar una versión concreta del servidor.

## 4. Comparación con Neo4j

| Necesidad | Neo4j | ArcadeDB |
|---|---|---|
| Leer patrones | Cypher | SQL extendido, Cypher según soporte |
| Python | Driver oficial Neo4j | Driver HTTP y API, otros protocolos |
| Despliegue | AuraDB o autogestionado | Despliegue según edición y arquitectura |
| Ontologías RDF | Requiere diseño adicional | Requiere comprobar capacidades concretas |

Estas categorías no bastan para afirmar cuál es «más rápido»: haz pruebas repetibles.

## 5. Ejercicios

1. Ejecuta una consulta con credenciales leídas de variables de entorno.
2. Gestiona error 401/403, timeout y base no existente, distinguiéndolos.
3. Registra duración y volumen de resultados con datos ficticios.
4. Crea una interfaz Python `CatalogoRepository` e implementa dos adaptadores de lectura.

## Referencias oficiales

- [ArcadeDB Python Quickstart](https://docs.arcadedb.com/arcadedb/tutorials/python-quickstart)
- [ArcadeDB Python HTTP Driver](https://docs.arcadedb.com/arcadedb/how-to/connectivity/drivers/python-http)
- [ArcadeDB HTTP API](https://docs.arcadedb.com/arcadedb/reference/http-api/http)


## 6. Soluciones razonadas

**Ejercicio 1.** Lee usuario y contraseña desde variables de entorno. El programa no debe almacenarlos como literales en el repositorio. Un fichero de configuración real con secretos debe quedar fuera de Git.

**Ejercicio 2.** Un error 401 señala problemas de autenticación; 403 indica falta de autorización; un timeout indica que no se recibió la respuesta a tiempo. No transformes estos errores en una lista vacía, porque eso ocultaría una incidencia técnica.

**Ejercicio 3.** Para medir rendimiento registra la versión del motor, número de registros, latencia de red, repeticiones, configuración y tamaño de respuesta. Una única petición no demuestra qué motor es mejor.

**Ejercicio 4.** Define un contrato para consultar libros que no conozca HTTP. Implementa dos adaptadores: memoria para tests unitarios y HTTP para integración. Así separas la lógica de negocio del mecanismo de conexión.

### Prueba antes de continuar

Explica con tus propias palabras qué significan API, HTTP, JSON, URL, POST y código 401. Describe por qué una respuesta sin libros no es igual que un error de conexión. Si puedes hacerlo sin buscar definiciones, pasa a [semana 10](semana-10.md).
