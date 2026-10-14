# Semana 10 — Comparación Neo4j vs ArcadeDB sin marketing

**Objetivo:** tomar decisiones con requisitos, datos y pruebas. No existe un «ganador» universal.

## Antes de comparar: qué significa «mejor»

Tu objetivo no es ganar una discusión sobre bases de datos, sino **elegir la herramienta que resuelva un problema concreto**.

Imagina dos vehículos: una bicicleta y una camioneta. ¿Cuál es mejor? Sin conocer la carga, el recorrido y el presupuesto, no existe una respuesta responsable. Con Neo4j y ArcadeDB ocurre algo parecido.

**Benchmark** es una prueba de rendimiento con un procedimiento y unas condiciones documentadas. Las palabras importantes son:

| Concepto | Explicación con lenguaje claro |
|---|---|
| Latencia | Tiempo que pasa hasta recibir la respuesta de una operación |
| Rendimiento o throughput | Cantidad de operaciones atendidas durante un intervalo |
| Concurrencia | Cantidad de operaciones que suceden o se solicitan simultáneamente |
| Caché | Datos guardados temporalmente para acelerar accesos repetidos |
| Índice | Estructura de búsqueda que evita revisar indiscriminadamente todos los registros |
| Mediana | Valor central de una serie de mediciones ordenadas |
| Percentil 95 (p95) | Valor por debajo del cual se sitúa aproximadamente el 95 % de las mediciones |
| Coste total | Recursos, administración, licencias, mantenimiento y desarrollo |

**Dos consultas no son comparables si devuelven cosas diferentes.** Antes de medir rapidez, verifica que ambas recuperan exactamente los mismos libros y relaciones, o explica las diferencias de semántica.

### Ejemplo con números inventados, solo para aprender a medir

Supón que cinco ejecuciones de una consulta tardan 7, 9, 8, 10 y 41 milisegundos. Ordenadas: 7, 8, 9, 10, 41. La **mediana es 9 ms**. No debes proclamar «la consulta siempre tarda 9 ms»: una ejecución tardó 41.

No confundas este ejemplo aritmético con una medición de Neo4j o ArcadeDB: **son números ficticios**.

### Cómo empezar una comparativa sin instalar nada nuevo

1. Define la pregunta de biblioteca, por ejemplo «libros de una autora».
2. Especifica el resultado correcto en identificadores, **antes de medir**.
3. Documenta la consulta Cypher y su equivalente en ArcadeDB.
4. Anota diferencias de sintaxis, dirección, duplicados y tipo de relación.
5. Solo después crea un entorno comparable y mide varias veces.

---

## Práctica previa: comprueba equivalencia antes de medir

Un error común es comparar la velocidad de dos consultas que **no responden exactamente lo mismo**. En este laboratorio podrás examinarlo con datos ficticios, sin motores instalados.

Ejecuta:

```bash
python laboratorios/comparar_motores.py
python -m pytest laboratorios/tests/test_comparar_motores.py -q
```

El programa muestra un ejemplo donde dos motores simulan devolver el mismo ISBN y título. **No ejecuta Neo4j ni ArcadeDB.**

### Cómo se comprueban resultados

```python
from laboratorios.comparar_motores import comparar_resultados

filas_neo4j = [
    {"isbn": "ISBN-001", "titulo": "El mapa de los grafos"},
]
filas_arcadedb = [
    {"isbn": "ISBN-001", "titulo": "El mapa de los grafos"},
]

print(comparar_resultados(filas_neo4j, filas_arcadedb))
```

**Esperado:** `True`. La función compara los pares ISBN-título y utiliza contadores para **no ocultar duplicados**. Si una consulta devuelve un libro dos veces y otra una vez, el resultado pasa a ser `False`.

### Cómo se calculan métricas sin inventar benchmarks

```python
from laboratorios.comparar_motores import resumen_tiempos

print(resumen_tiempos([7, 9, 8, 10, 41]))
```

**Esperado:** `{'n': 5, 'mediana_ms': 9, 'p95_ms': 41}`.

- `n` es el número de mediciones.
- **Mediana:** valor central de los tiempos ordenados.
- **p95:** percentil 95 según el método de rango más próximo, declarado en la implementación.

Los números **son inventados para aprender estadística**, no son resultados observados de motores de bases de datos. Una comparativa profesional también necesita dataset, versiones, hardware, red, índices y varias ejecuciones reales.

**Prueba negativa obligatoria:** añade un ISBN repetido a solo uno de los conjuntos. Aunque los títulos parezcan iguales, la comparación debe devolver `False`.

---

## 1. Define un benchmark justo

Con el mismo conjunto **ficticio** de libros, autores y temas ejecuta:

1. Buscar libro por identificador.
2. Recuperar sus autores.
3. Listar libros asociados a un tema.
4. Recorrer dos saltos `Autor → Libro → Tema`.
5. Cargar 1.000 registros sintéticos.
6. Repetir la carga y contar duplicados.

**Controla:** hardware/plan, índices, tamaño de datos, latencia de red, concurrencia y caché. No compares AuraDB remoto con un ArcadeDB local sin aclarar que el resultado incluye la red.

## 2. Matriz de evaluación

| Criterio | Qué debes documentar |
|---|---|
| Lenguajes | Consultas necesarias y compatibilidad demostrada |
| Python | API/driver, transacciones, mantenimiento |
| Operación | Copias, actualizaciones, usuarios, observabilidad |
| Coste | Recursos, trabajo operativo y límites de plan |
| Semántica | RDF, SKOS, OWL y SHACL: requisitos frente a soporte comprobado |
| Seguridad | Aislamiento, cifrado, permisos y auditoría |

## 3. Cómo redactar el informe

Para cada afirmación incluye **prueba o enlace oficial**. Distingue:

- Hecho documentado.
- Observación experimental.
- Hipótesis que aún no se ha validado.

Ejemplo correcto: «Con 3.000 libros sintéticos y una consulta parametrizada, el tiempo mediano de 30 ejecuciones fue X en la configuración Y». Ejemplo incorrecto: «El motor A es siempre más rápido».

## 4. Ejercicios

1. Prepara tablas con resultados y parámetros de consulta.
2. Decide si añadir PostgreSQL aporta valor o complejidad innecesaria.
3. Evalúa si la semántica del catálogo requiere una representación RDF separada.
4. Explica la migración, el lock-in y el coste de mantener dos drivers.

## Entregable

Un informe de 2–4 páginas con matriz de decisión, scripts, contexto de ejecución y riesgos.

## Fuentes

- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [ArcadeDB Documentation](https://docs.arcadedb.com/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)


## 5. Ejercicio práctico completo: plantilla de decisión

Rellena esta tabla para dos motores reales de tu laboratorio. **No pongas cifras inventadas** donde todavía no has realizado mediciones.

| Factor | Motor A | Motor B | Cómo lo comprobaré |
|---|---|---|---|
| Resultado correcto para ISBN-001 | Pendiente | Pendiente | Comparar ISBN y título |
| Resultado correcto de Autor→Libro→Tema | Pendiente | Pendiente | Comparar conjuntos de registros |
| Mediana de latencia tras repeticiones | No medida | No medida | Script reproducible y varias ejecuciones |
| Seguridad de conexiones | Pendiente | Pendiente | Revisar autenticación y TLS según despliegue |
| Gestión de claves y duplicados | Pendiente | Pendiente | Constraint o índice único y prueba negativa |
| Recuperación de errores | Pendiente | Pendiente | Probar fallos controlados |
| Coste de mantenimiento | Pendiente | Pendiente | Documentar horas, parches y licencias |

### Soluciones razonadas a los ejercicios

**1.** Para repetir de verdad un benchmark necesitas guardar scripts, parámetros, dataset, versiones, hardware/plan, número de repeticiones y condiciones de red. Una tabla con «el motor X ganó» no demuestra nada por sí sola.

**2.** PostgreSQL puede ser adecuado para transacciones y datos relacionales. No lo añadas sin una razón: tener dos motores crea problemas de sincronización, copias, permisos y observabilidad.

**3.** Si necesitas intercambio interoperable mediante RDF, vocabularios SKOS y semántica OWL, evalúa una plataforma RDF. Eso no convierte automáticamente cualquier grafo de propiedades en un triple store.

**4.** Mantener dos drivers y motores incrementa superficie de mantenimiento. Una migración debe probar equivalencia de resultados, política de IDs, consultas y operaciones; no basta con traducir cadenas de texto.

### Qué debes demostrar para continuar

Describe tres diferencias entre un **dato probado**, una **suposición** y una **medición reproducible**. Explica por qué no es justo comparar un servicio remoto con un motor local sin registrar la latencia de red.

**Siguiente:** [semana 11, qué es una ontología](semana-11.md).
