# Laboratorio de ontologías y validación

Ejemplos ficticios y públicos.

- `temas.ttl`: vocabulario SKOS.
- `biblioteca.ttl`: individuos y clases.
- `shapes.ttl`: requisitos SHACL.
- `validar.py`: script que valida los archivos anteriores.

Desde la raíz del repositorio:

```bash
python -m pip install -r ejemplos/ontologias/requirements.txt
python ejemplos/ontologias/validar.py
```

Para practicar el fallo, elimina `ex:titulo` de un libro y vuelve a ejecutar.

Documentación: https://www.w3.org/TR/shacl/ y https://www.w3.org/TR/owl2-primer/.
