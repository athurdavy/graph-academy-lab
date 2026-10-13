# Laboratorios verificables — biblioteca ficticia

Estos materiales complementan el campus público. Para **leerlos en formato web** abre [Laboratorios en la academia](https://athurdavy.github.io/graph-academy-lab/laboratorios.html); los archivos aquí sirven para ejecutar código.

## Rutas de estudio

| Laboratorio | Tecnología | Requiere servicio externo | Verificación |
|---|---|---|---|
| [01 — Modelado](01-modelado.md) | Python + NetworkX | No | pytest |
| [02 — Ontologías](02-ontologias.md) | RDFLib + SHACL | No | pytest + validación |
| [03 — Cypher](03-neo4j.md) | Neo4j AuraDB, Cypher, Python | Sí, instancia de prueba | Recuentos y consultas |
| [04 — Arquitectura](04-arquitectura.md) | Python, repositorios e interfaces | No | pytest |

## Instalación de los laboratorios locales

En un clon del repositorio, con Python 3.11 o superior:

\`\`\`bash
python -m venv .venv
# macOS y Linux:
source .venv/bin/activate
# PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r laboratorios/requirements.txt
python -m pytest laboratorios/tests -q
\`\`\`

**Resultado esperado:** tests correctos en un entorno con dependencias instaladas. No se necesitan contraseñas para estos tests.

Para el laboratorio 03 es necesaria una instancia Neo4j de pruebas; las contraseñas **nunca** se guardan en el repositorio. Todos los datos son ficticios.

## Calidad y límites

- El pipeline CI ejecuta únicamente tests locales y no utiliza cuentas Aura.
- La ausencia de errores en tests sintéticos no equivale a validación de rendimiento o compatibilidad con todas las versiones de los motores.
- Al modificar los ejemplos, crea un test que primero falle y luego comprueba que tu corrección lo hace pasar.
