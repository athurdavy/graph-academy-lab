# Semana 09 — Consultas y API de ArcadeDB con Python

**Objetivo:** ejecutar una consulta real con ArcadeDB utilizando su API HTTP y comprender la diferencia entre leer y escribir.

## 1. Consultas con SQL y grafos

ArcadeDB extiende SQL con recorridos de relaciones. Para listar los libros cargados:

\`\`\`sql
SELECT FROM Libro;
\`\`\`

La documentación oficial explica que el acceso puede hacerse por API HTTP/JSON, por controladores nativos y por protocolos compatibles. La elección del protocolo afecta a despliegue, autenticación y herramientas.

## 2. Cliente Python HTTP

La API oficial expone \`POST /api/v1/query/{database}\` para consultas de lectura. Esta práctica solo debe apuntar a tu instancia **local**:

\`\`\`python
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
\`\`\`

No guardes contraseñas en el repositorio. Para producción usa transporte protegido y la política de autenticación apropiada.

## 3. Driver oficial

ArcadeDB documenta \`arcadedb-driver\` para Python, generado desde OpenAPI. Si lo usas, fija una versión, documenta la API y comprueba cambios del cliente. Los ejemplos de los tutoriales pueden reflejar una versión concreta del servidor.

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
4. Crea una interfaz Python \`CatalogoRepository\` e implementa dos adaptadores de lectura.

## Referencias oficiales

- [ArcadeDB Python Quickstart](https://docs.arcadedb.com/arcadedb/tutorials/python-quickstart)
- [ArcadeDB Python HTTP Driver](https://docs.arcadedb.com/arcadedb/how-to/connectivity/drivers/python-http)
- [ArcadeDB HTTP API](https://docs.arcadedb.com/arcadedb/reference/http-api/http)
