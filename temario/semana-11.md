# Semana 11 — Ontologías desde cero: entiende las ideas antes de aprender las siglas

![Diferencias entre RDF, SKOS, OWL y SHACL](../assets/capas-semanticas.svg)

**Bloque semántico.** Antes: [Semana 03](semana-03.md). Después: [Semana 12](semana-12.md). Tiempo: 8–12 horas. **Objetivo:** poder explicar una ontología, distinguir clases de conceptos y probar RDF mediante Python sin asumir conocimientos previos de web semántica.

## 1. El problema real: dos sistemas que no se entienden

Nuestra biblioteca ficticia tiene un libro con una autora y un tema. Un sistema denomina a la autora «escritor» y otro «creator». ¿Significa lo mismo? ¿Cómo se especifica la relación? No basta con tener tablas o un grafo conectado: necesitamos definiciones y acuerdos sobre el significado.

Una **ontología** es una especificación formal de los tipos de entidades, relaciones y afirmaciones válidas sobre un dominio. *Dominio* significa el tema que modelamos —la biblioteca—, no una dirección de internet.

En el caso de biblioteca queremos describir que existen entidades de tipo **Libro** y **Autor**, que se pueden relacionar con la propiedad **escritoPor**, y que un LibroDigital es un tipo especial de Libro.

## 2. Seis conceptos sin jerga

| Palabra | Explicación sencilla | Ejemplo |
|---|---|---|
| Clase | Categoría de entidades | Libro |
| Individuo | Entidad concreta | libro001 |
| Propiedad | Característica o relación | titulo, escritoPor |
| Axioma | Afirmación lógica declarada | LibroDigital es subclase de Libro |
| Inferencia | Conclusión derivada según reglas | libro001 es Libro si es LibroDigital |
| Dominio | Universo temático que describimos | Biblioteca |

No confundas una **clase OWL** con una clase Python. La analogía de clase/objeto es útil para imaginar categorías e individuos, pero OWL no ejecuta métodos ni se comporta como un ORM.

## 3. Glosario, taxonomía, tesauro y ontología no son lo mismo

Un **glosario** define palabras. Un **vocabulario controlado** fija denominaciones aceptadas. Una **taxonomía** agrupa categorías jerárquicamente. Un **tesauro** añade relaciones como etiquetas preferidas, variantes y asociaciones entre conceptos. Una **ontología formal** expresa clases, propiedades y axiomas con semántica lógica.

Ejemplo: «Ciencia» → «Teoría de grafos» puede ser una jerarquía temática. No significa necesariamente que todos los individuos de una clase Grafos sean individuos de una clase Ciencia.

**Decisión práctica:** si solo necesitas clasificar libros con temas y sinónimos, SKOS puede bastar. Si necesitas inferencias a partir de axiomas, examina OWL. Si necesitas comprobar registros obligatorios, estudia SHACL.

## 4. RDF: los ladrillos con los que expresamos afirmaciones

**RDF** son siglas de *Resource Description Framework*: modelo de descripción de recursos. Utiliza afirmaciones de tres partes, llamadas **triples**:

- **Sujeto:** de qué hablamos.
- **Predicado:** qué afirmamos sobre ello.
- **Objeto:** recurso o valor asociado.

Por ejemplo: libro001 — tiene título — El mapa de los grafos.

En el formato textual **Turtle** se escribe así:

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
ex:libro001 dcterms:title "El mapa de los grafos"@es .
```

Lee cada fragmento:

1. `@prefix` define una abreviatura para identificadores largos.
2. `ex:libro001` identifica al libro.
3. `dcterms:title` es una propiedad estandarizada de Dublin Core.
4. `"El mapa de los grafos"@es` es texto etiquetado como español.
5. El punto `.` termina la afirmación.

Una **IRI**, de *Internationalized Resource Identifier*, es un identificador global. No significa que cada IRI abra una web real. `example.org` se utiliza aquí únicamente para ejemplos ficticios.

## 5. RDFS: clases y subclases

**RDFS** significa *RDF Schema*. Añade un vocabulario para clases, subclases, propiedades, dominios y rangos.

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:LibroDigital rdfs:subClassOf ex:Libro .
ex:libro001 rdf:type ex:LibroDigital .
```

Declara explícitamente que LibroDigital es una subclase de Libro y que libro001 pertenece a LibroDigital. **Una consecuencia lógica** es que libro001 pertenece a Libro.

**No supongas que un archivo Turtle calcula esa inferencia por sí mismo.** Necesitas una herramienta y configuración de razonamiento que aplique la semántica adecuada.

### Por qué el dominio y el rango no son restricciones SQL

Si una propiedad tiene `rdfs:domain ex:Libro`, usar esa propiedad con un sujeto permite deducir que ese sujeto es Libro bajo RDFS. No significa necesariamente que el sistema rechace cualquier dato sin un `rdf:type` explícito. Es **inferencia de tipos**, no una clave foránea.

## 6. OWL: hablar de axiomas más expresivos

**OWL** significa *Web Ontology Language*. OWL 2 es un lenguaje estandarizado para expresar axiomas como equivalencias, disjunción de clases, propiedades inversas y restricciones lógicas.

Ejemplo: si `escritoPor` y `escribio` son propiedades inversas, al afirmar «libro001 escritoPor autor001» un razonador compatible puede deducir «autor001 escribio libro001».

No necesitas memorizar toda OWL hoy. El primer objetivo es distinguir **lo declarado** de **lo inferido**.

## 7. Mundo abierto: la ausencia de un dato no demuestra lo contrario

**OWA**, *Open World Assumption* o **suposición de mundo abierto**, significa que no conocer una afirmación no implica que sea falsa.

Si un libro no tiene autor declarado:

- sabemos que falta información en **nuestro grafo**;
- **no** sabemos que ese libro carece de autor;
- una restricción existencial OWL no equivale a un «campo requerido» como lo entenderías en un formulario.

Este cambio de mentalidad es fundamental para ontologías y para no malinterpretar los resultados de un razonador.

## 8. SHACL: la comprobación de datos

**SHACL** significa *Shapes Constraint Language*, lenguaje para expresar condiciones que debe cumplir un grafo RDF. ¿Queremos exigir que cada libro tenga al menos un título? SHACL sirve para expresarlo y obtener un informe.

```turtle
@prefix ex: <https://example.org/biblioteca/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

ex:LibroShape a sh:NodeShape ;
  sh:targetClass ex:Libro ;
  sh:property [ sh:path ex:titulo ; sh:minCount 1 ] .
```

Aquí `sh:targetClass` selecciona las entidades objetivo de tipo Libro y `sh:minCount 1` exige al menos una propiedad `titulo`. **OWL describe axiomas; SHACL comprueba condiciones de calidad.** No son herramientas intercambiables.

## 9. SKOS y Dublin Core: metadatos frente a ontologías

**SKOS**, *Simple Knowledge Organization System*, define cómo representar conceptos de vocabularios y tesauros. «Teoría de grafos» puede ser un concepto SKOS con una etiqueta preferida y otra alternativa.

**DCMI Terms**, de *Dublin Core Metadata Initiative*, proporciona propiedades como título, creador, identificador o fecha. Sirven para describir recursos de forma interoperable.

Puedes combinar **SKOS para temas**, **DCMI para fichas bibliográficas**, **SHACL para validar** y **OWL para inferencias** cuando realmente sean necesarias.

## 10. Primer laboratorio que puedes ejecutar con Python

Instala las dependencias desde la raíz del repositorio:

```bash
python -m pip install -r laboratorios/requirements.txt
```

Ejecuta:

```python
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

ex = Namespace("https://example.org/biblioteca/")
g = Graph()

g.add((ex.LibroDigital, RDFS.subClassOf, ex.Libro))
g.add((ex.libro001, RDF.type, ex.LibroDigital))
g.add((ex.libro001, ex.titulo, Literal("El mapa de los grafos", lang="es")))

print("Triples guardados:", len(g))
print("¿Se guardó explícitamente rdf:type Libro?",
      (ex.libro001, RDF.type, ex.Libro) in g)
```

**Resultado esperado:**

```text
Triples guardados: 3
¿Se guardó explícitamente rdf:type Libro? False
```

¿Por qué `False` si sabemos que LibroDigital es subclase de Libro? **Porque no hemos ejecutado razonamiento:** RDFLib contiene los tres triples explícitos que añadiste; esa consulta directa no añade automáticamente las consecuencias RDFS.

Después practica [RDF y validación SHACL en Python](../laboratorios/02-ontologias.md).

## 11. Ejercicios para comprobar que entiendes

1. ¿Qué diferencia hay entre la clase Libro y el individuo libro001?
2. En `ex:libro001 dcterms:title "Título"@es`, identifica sujeto, predicado y objeto.
3. ¿Por qué «Grafos» como concepto SKOS no equivale necesariamente a una clase OWL?
4. Agrega en Python un segundo libro y verifica cuántos triples has declarado.
5. ¿Por qué no concluyes que un libro sin autor declarado no tiene autor?
6. ¿Qué utilizarías para exigir un título: OWL o SHACL? Justifica.
7. ¿Cuándo elegirías usar solo SKOS, sin diseñar una ontología OWL compleja?

### Soluciones comentadas

**1.** La clase describe una categoría; el individuo identifica un recurso concreto. No son dos formas de llamar a la misma cosa.

**2.** Sujeto: libro001; predicado: dcterms:title; objeto: un literal de texto en español.

**3.** Un concepto SKOS clasifica materias; una clase OWL describe un conjunto formal de individuos. Las jerarquías de conceptos y de clases no comparten la misma semántica.

**5.** La información ausente en un sistema no demuestra falsedad bajo el supuesto de mundo abierto.

**6.** SHACL permite comprobar `sh:minCount 1` para un objetivo determinado. OWL no debe confundirse con esa validación de completitud.

**7.** Un catálogo de materias con nombres preferidos, alternativas y jerarquías puede no necesitar los axiomas expresivos de OWL.

## 12. ¿Estás preparado para continuar?

Antes de la siguiente unidad debes poder explicar sin mirar: **ontología, clase, individuo, propiedad, triple RDF, IRI, RDFS, OWL, OWA, SKOS, SHACL y DCMI Terms**. Si una sigla no te dice nada, vuelve al ejemplo de biblioteca y formula una oración concreta con ella.

**Siguiente:** [Semana 12 — construir un vocabulario SKOS y consultarlo con SPARQL](semana-12.md).

## Fuentes normativas

- [RDF 1.1 Primer — W3C](https://www.w3.org/TR/rdf11-primer/)
- [RDFS — W3C](https://www.w3.org/TR/rdf-schema/)
- [OWL 2 Primer — W3C](https://www.w3.org/TR/owl2-primer/)
- [SKOS Primer — W3C](https://www.w3.org/TR/skos-primer/)
- [SHACL — W3C](https://www.w3.org/TR/shacl/)
- [DCMI Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)

**Estado editorial:** explicaciones basadas en estándares oficiales, con ejemplos y ejercicios. Pendiente revisión integral de ejecución y evaluación formativa con alumnos.
