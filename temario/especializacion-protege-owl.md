# Taller guiado 01 — Protégé Desktop y ontologías OWL desde cero

![RDF, SKOS, OWL y SHACL: diferentes funciones](../assets/capas-semanticas.svg)

**Para alumnos que saben programar pero no conocen Protégé.** Antes estudia [ontologías desde cero](semana-11.md) y [OWL](semana-13.md). Después continúa con [GraphDB](especializacion-graphdb.md). Dedicación: dos sesiones de 2 horas y práctica adicional.

**Meta observable:** abrir una ontología, distinguir clases, propiedades e individuos, añadir datos, obtener inferencias con un razonador, exportar RDF y verificar que no has confundido validación e inferencia.

## 1. Qué es Protégé, y qué no es

Protégé es un **editor de ontologías** para modelar clases, propiedades y axiomas, especialmente en **OWL (Web Ontology Language)**. Una ontología formal define conceptos y permite derivar consecuencias lógicas. Protégé **no es** una base de datos de producción como Neo4j ni un repositorio RDF como GraphDB.

| Herramienta | Su principal papel |
|---|---|
| Protégé | Diseñar una ontología y revisar sus axiomas |
| RDFLib | Leer y escribir RDF desde Python |
| GraphDB | Guardar y consultar RDF a través de SPARQL |
| Neo4j | Trabajar con grafos de propiedades y Cypher |

No necesitas programar en Java para usar Protégé, aunque la aplicación Desktop funciona sobre tecnología Java. Java será opcional en el itinerario de integración con Jena/RDF4J.

## 2. El escenario que vamos a modelar

Trabajaremos con una biblioteca ficticia y este archivo descargable del repositorio:

`ejemplos/ontologias/ontologia-biblioteca.ttl`

Contiene tres **clases**: Libro, LibroDigital y Autor; dos **propiedades de objeto**: escritoPor y escribio; una **propiedad de datos**: titulo; y tres **individuos**: libro001, libro002 y autor001.

La afirmación «LibroDigital es subclase de Libro» no equivale a «libro001 es una clase». Lo primero define inclusión entre categorías; libro001 es una **entidad concreta**.

## 3. Instalar y abrir el proyecto

1. Entra en la [página oficial de Protégé](https://protege.stanford.edu/software/) y descarga Desktop para tu sistema.
2. Consulta su [Getting Started oficial](https://protegeproject.github.io/protege/getting-started/) para instalación y versiones.
3. Descarga o clona Graph Academy Lab y abre **File → Open** con `ejemplos/ontologias/ontologia-biblioteca.ttl`.
4. Ve a la vista de clases (`Classes`). Debes encontrar LibroDigital debajo de Libro.
5. Abre la vista de propiedades y después la de individuos. Reconoce las diferencias entre las tres.

**Resultado esperado:** podrás identificar esta estructura lógica:

```text
owl:Thing
├── Autor
└── Libro
    └── LibroDigital
```

`owl:Thing` es la clase universal de individuos. No es el nombre de un registro.

Si ves IRIs completas en vez de nombres amigables, inspecciona las etiquetas `rdfs:label`. La etiqueta visual no cambia la identidad de la entidad.

## 4. Entender cada pestaña antes de editar

### Clases: Classes

Una **clase** expresa una categoría, como Libro. Una **subclase** expresa inclusión: todos los LibroDigital son Libro. Esto no equivale a una taxonomía de materias SKOS.

### Propiedades de objeto: Object Properties

Conectan un individuo con otro recurso. Ejemplo:

```turtle
ex:libro001 ex:escritoPor ex:autor001 .
```

Aquí el sujeto es un libro y el objeto es un autor. `rdfs:domain` y `rdfs:range` permiten determinadas inferencias de tipos; **no son** automáticamente validaciones de claves foráneas como en SQL.

### Propiedades de datos: Data Properties

Conectan el individuo con un **literal**, como una cadena:

```turtle
ex:libro001 ex:titulo "El mapa de los grafos" .
```

**Comprueba:** identifica en Protégé cuál de las dos propiedades conecta dos recursos y cuál enlaza un literal.

## 5. Primer ejercicio en la interfaz: crear libro003

1. Selecciona la clase LibroDigital.
2. En la vista de **Individuals**, añade un individuo llamado `libro003`.
3. Comprueba su IRI: queremos que represente `https://example.org/biblioteca/libro003`.
4. Declara su tipo LibroDigital.
5. Añade la propiedad de datos `titulo` con valor de texto «Atlas de conocimiento».
6. Añade la propiedad de objeto `escritoPor` apuntando a `autor001`.
7. Guarda una **copia nueva**, sin destruir el ejemplo inicial.

**Resultado esperado:** un individuo que tiene un título literal y una relación a un recurso Autor. Si en vez de eso creaste una clase llamada libro003, repite el ejercicio: son conceptos diferentes.

Las denominaciones exactas de botones pueden variar según la versión de Protégé; utiliza la documentación oficial de esa versión.

## 6. Inferencia: ¿por qué un LibroDigital es Libro?

En la ontología existen los hechos declarados:

```turtle
ex:LibroDigital rdfs:subClassOf ex:Libro .
ex:libro001 a ex:LibroDigital .
```

Por tanto, con semántica RDFS/OWL adecuada, `libro001 a ex:Libro` es una **consecuencia lógica** aunque ese triple no esté declarado en el archivo.

### Experimenta con un razonador

1. Inspecciona los tipos **declarados** de libro001.
2. En el menú **Reasoner**, elige un razonador disponible y compatible (por ejemplo HermiT si se incluye en tu instalación).
3. Ejecuta la clasificación según las opciones de esa versión.
4. Inspecciona los tipos **inferidos** de libro001. Deberías poder comprobar su pertenencia a Libro.
5. Anota herramienta, versión y resultado. Si no tienes razonador, anota la dependencia en vez de inventar el resultado.

**Importante:** un razonador extrae consecuencias lógicas de axiomas. No comprueba si las afirmaciones de una biblioteca son verdaderas en el mundo real.

### Contrasta con Python sin razonador

```bash
python -m pip install -r laboratorios/requirements.txt
python laboratorios/practica_owl_rdf.py
python -m pytest laboratorios/tests/test_practica_owl_rdf.py -q
```

El programa inspecciona si el triple `libro001 rdf:type Libro` está **materializado**. Devuelve `False` porque RDFLib, en ese ejemplo, no ejecuta razonamiento. Esto **no contradice** la consecuencia lógica.

## 7. Propiedades inversas: dos direcciones semánticas

La ontología declara que `escritoPor` y `escribio` son propiedades inversas.

Si escribimos:

```turtle
ex:libro001 ex:escritoPor ex:autor001 .
```

Un razonador adecuado puede deducir:

```turtle
ex:autor001 ex:escribio ex:libro001 .
```

No hemos «dado la vuelta a una flecha» como al escribir una consulta Cypher: hemos declarado un axioma que relaciona el significado lógico de dos propiedades RDF.

## 8. Mundo abierto y clases disjuntas

**OWA** (*Open World Assumption*, suposición de mundo abierto) significa que si el título o el autor no están declarados no concluimos automáticamente que no existen.

Por eso OWL **no equivale** a la regla de un formulario «este campo es obligatorio». La validación de ese requisito pertenece a [SHACL](semana-14.md).

Como ejercicio opcional, declara dos clases **disjuntas** (sin individuos compartidos) y asigna deliberadamente el mismo individuo a ambas. Un razonador compatible puede detectar inconsistencia.

**No declares LibroDigital y LibroFisico disjuntas por costumbre:** primero decide si cada recurso representa una obra, una edición o una manifestación física/digital.

## 9. Exportar y verificar

1. Guarda una copia con **Save As** o la función de exportación correspondiente, eligiendo Turtle u otro formato RDF soportado.
2. Cierra y vuelve a abrir el archivo.
3. Verifica que las **IRIs** de Libro y libro001 no hayan cambiado.
4. Verifica que se conservan `rdfs:subClassOf`, `owl:inverseOf` y los individuos.
5. Repite la prueba del razonador.

**Guardar una ontología y exportar axiomas inferidos son operaciones distintas.** Protégé documenta herramientas específicas para exportación de axiomas inferidos. No presumas que guardar la ontología materializa todo lo inferido.

## 10. Ejercicios y soluciones

**Básico:** ¿qué diferencia hay entre Libro, LibroDigital y libro001? Localiza una propiedad de objeto y una de datos.

**Intermedio:** añade libro003, vuelve a abrirlo y documenta una inferencia comprobada.

**Avanzado:** plantea dos clases disjuntas con una justificación de dominio. Explica por qué `owl:sameAs` es peligroso si dos recursos solo tienen títulos parecidos. Exporta y compara la estructura.

### Soluciones razonadas

- **Clase frente a individuo:** Libro es una categoría; LibroDigital es una categoría más concreta; libro001 representa una entidad del catálogo.
- **Propiedades:** escritoPor conecta dos individuos; titulo conecta un individuo y un literal.
- **Inferencia:** si libro001 es LibroDigital y toda instancia de LibroDigital es Libro, la pertenencia a Libro se sigue lógicamente.
- **owl:sameAs:** afirma identidad; los títulos similares no demuestran identidad.

## 11. Evaluación de salida

Entrega una ontología editada, una tabla de axiomas declarados e inferencias comprobadas, el archivo exportado reabierto, la versión de Protégé y un razonador identificado. Acompaña la entrega de una explicación de por qué la validación de títulos exige otras herramientas.

**Siguiente clase:** [GraphDB: almacenar y consultar ese mismo RDF](especializacion-graphdb.md).

**Fuentes oficiales:** [Protégé Desktop](https://protege.stanford.edu/software/), [Getting Started](https://protegeproject.github.io/protege/getting-started/), [exportar inferencias](https://protegeproject.github.io/protege/menus/), [OWL 2 Primer W3C](https://www.w3.org/TR/owl2-primer/).

**Estado:** explicación y archivos reproducibles publicados. Las operaciones en la interfaz deben contrastarse en una instalación real de Protégé; no se ha registrado todavía esa ejecución supervisada.
