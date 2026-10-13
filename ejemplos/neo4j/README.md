# Laboratorio Neo4j AuraDB — Biblioteca ficticia

Aprende de forma progresiva en la web: [semana 04](https://athurdavy.github.io/graph-academy-lab/lecciones.html?semana=04), [semana 05](https://athurdavy.github.io/graph-academy-lab/lecciones.html?semana=05), [semana 06](https://athurdavy.github.io/graph-academy-lab/lecciones.html?semana=06) y [semana 07](https://athurdavy.github.io/graph-academy-lab/lecciones.html?semana=07).

## 1. Primero aprende sin credenciales

Desde la raíz del repositorio:

```bash
python -m pip install -r ejemplos/neo4j/requirements.txt
python -m pytest ejemplos/neo4j/tests -q
```

Los tests emplean un driver simulado. Verifican parámetros, valores devueltos, transacciones y errores, **pero no demuestran la conectividad ni el comportamiento real del servidor**.

## 2. Después practica en AuraDB

1. Crea una instancia AuraDB de prueba.
2. Ejecuta las sentencias de `01_biblioteca.cypher` en el editor de consultas.
3. Comprueba que se han creado libros, autores, temas y relaciones.
4. Copia `.env.example` a `.env` **dentro de `ejemplos/neo4j/`** y completa credenciales localmente.
5. Desde la raíz del repositorio ejecuta `python ejemplos/neo4j/app.py`.
6. Consulta `GRAFOS`: deberían aparecer `ISBN-001` y `ISBN-002`.

No publiques `.env`, credenciales, datos internos ni capturas de configuración privada. Todo el dataset es ficticio.

## 3. Cómo continuar

- Lee la teoría en el campus, no en archivos de GitHub.
- Ejecuta los ejemplos por orden.
- Modifica una consulta y predice el resultado antes de ejecutarla.
- Resuelve los ejercicios sin mirar las soluciones.
- Documenta los resultados, errores y condiciones de tu entorno.

**Referencias oficiales:** [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/) y [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/).
