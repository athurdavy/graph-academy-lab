"""Cliente educativo ArcadeDB HTTP. No imprime ni guarda contraseñas.

Por defecto no realiza solicitudes: ejecuta los tests unitarios sin servidor.
"""
import os
import requests
from requests.auth import HTTPBasicAuth


def extraer_libros_json(datos):
    """Normaliza la respuesta documentada {result: [...]} de consultas ArcadeDB.

    Rechaza un formato inesperado en vez de ocultar el error devolviendo [].
    """
    if not isinstance(datos, dict) or not isinstance(datos.get("result"), list):
        raise ValueError("Respuesta ArcadeDB inesperada: falta la lista 'result'")
    return datos["result"]


def consultar_libros(session, url, database, username, password):
    """Consulta libros con servidor configurado; recibe session para simular en tests."""
    if not all(isinstance(x, str) and x.strip() for x in
               (url, database, username, password)):
        raise ValueError("Configuración HTTP obligatoria")
    response = session.post(
        f"{url.rstrip('/')}/api/v1/query/{database}",
        auth=HTTPBasicAuth(username, password),
        json={"language": "sql", "command": "SELECT FROM Libro"},
        timeout=10,
    )
    response.raise_for_status()
    return extraer_libros_json(response.json())


def main():
    url = os.getenv("ARCADEDB_URL", "http://localhost:2480")
    database = os.getenv("ARCADEDB_DATABASE", "biblioteca")
    username = os.environ["ARCADEDB_USER"]
    password = os.environ["ARCADEDB_PASSWORD"]
    with requests.Session() as session:
        for libro in consultar_libros(session, url, database, username, password):
            print(libro.get("isbn"), libro.get("titulo"))


if __name__ == "__main__":
    main()
