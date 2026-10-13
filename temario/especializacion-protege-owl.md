# Especialización práctica: Protégé y OWL 2

**Laboratorio:** biblioteca digital ficticia. **Meta:** crear y comprobar una ontología, no solo memorizar términos.

## ¿Qué es Protégé?

[Protégé Desktop](https://protege.stanford.edu/) es un editor de ontologías empleado para modelar clases, propiedades, individuos y axiomas OWL. No es un ORM y no reemplaza directamente un motor de almacenamiento de datos operacional.

## Tutorial guiado

1. Instala Protégé Desktop utilizando exclusivamente su web oficial.
2. Abre el archivo de ejemplo de la biblioteca (ejemplos/ontologias/biblioteca.ttl).
3. Comprueba las clases Libro y LibroDigital y establece LibroDigital como subclase de Libro.
4. Añade la clase Autor y la propiedad de objeto escritoPor; declara su dominio y rango y **explica que en RDFS esos axiomas pueden inducir tipos**, no rechazar datos.
5. Crea un individuo libro003 de tipo LibroDigital y un individuo autor003 de tipo Autor, conectándolos con escritoPor.
6. En una configuración compatible, ejecuta el razonador disponible y documenta la inferencia de que libro003 pertenece a Libro.
7. Guarda y vuelve a abrir la ontología. Verifica IRIs e importaciones.

## Experimentos conceptuales

**Experimento A — disjunción:** declara LibroDigital y LibroFisico disjuntas y asigna un individuo a ambas. Estudia si el razonador informa de inconsistencia. Documenta qué axioma crea el conflicto.

**Experimento B — mundo abierto:** crea un Libro sin autor. ¿El razonador rechaza el individuo? No lo presupongas: la ausencia de un triple no equivale a negar su existencia.

**Experimento C — validación:** utiliza SHACL para exigir un título de texto. La inferencia OWL y la comprobación SHACL son problemas distintos.

## Entrega evaluable

Ontología exportada en formato RDF/OWL, preguntas de competencia, registro de inferencias verificadas, versión del razonador, cuatro capturas sin información privada y comparación con SHACL.

## Referencias oficiales

- [Protégé Desktop](https://protege.stanford.edu/)
- [OWL 2 Primer — W3C](https://www.w3.org/TR/owl2-primer/)
- [OWL 2 Profiles — W3C](https://www.w3.org/TR/owl2-profiles/)
- [SHACL — W3C](https://www.w3.org/TR/shacl/)
