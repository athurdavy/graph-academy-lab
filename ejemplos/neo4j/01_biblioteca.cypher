// Datos completamente ficticios para la formación pública.
// Ejecuta las instrucciones en un entorno de laboratorio.
CREATE CONSTRAINT libro_isbn IF NOT EXISTS FOR (l:Libro) REQUIRE l.isbn IS UNIQUE;
CREATE CONSTRAINT autor_id IF NOT EXISTS FOR (a:Autor) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT tema_codigo IF NOT EXISTS FOR (t:Tema) REQUIRE t.codigo IS UNIQUE;
CREATE CONSTRAINT lector_id IF NOT EXISTS FOR (l:Lector) REQUIRE l.id IS UNIQUE;

UNWIND [
  {isbn:'ISBN-001', titulo:'El mapa de los grafos', anio:2022},
  {isbn:'ISBN-002', titulo:'Rutas de conocimiento', anio:2024},
  {isbn:'ISBN-003', titulo:'Historias del océano', anio:2019}
] AS fila
MERGE (l:Libro {isbn:fila.isbn})
SET l.titulo=fila.titulo, l.anio=fila.anio;

UNWIND [{id:'A-001',nombre:'Marina Soler'},{id:'A-002',nombre:'Diego Ríos'}] AS fila
MERGE (a:Autor {id:fila.id}) SET a.nombre=fila.nombre;

UNWIND [{codigo:'GRAFOS',nombre:'Grafos'},{codigo:'CIENCIA',nombre:'Ciencia'},{codigo:'NATURALEZA',nombre:'Naturaleza'}] AS fila
MERGE (t:Tema {codigo:fila.codigo}) SET t.nombre=fila.nombre;

MERGE (p:Lector {id:'L-001'}) SET p.alias='lector_demo';

MATCH (a:Autor {id:'A-001'}), (l:Libro {isbn:'ISBN-001'})
MERGE (a)-[:ESCRIBIO]->(l);
MATCH (a:Autor {id:'A-001'}), (l:Libro {isbn:'ISBN-002'})
MERGE (a)-[:ESCRIBIO]->(l);
MATCH (a:Autor {id:'A-002'}), (l:Libro {isbn:'ISBN-003'})
MERGE (a)-[:ESCRIBIO]->(l);

MATCH (l:Libro {isbn:'ISBN-001'}), (t:Tema {codigo:'GRAFOS'})
MERGE (l)-[:TRATA_SOBRE]->(t);
MATCH (l:Libro {isbn:'ISBN-002'}), (t:Tema {codigo:'GRAFOS'})
MERGE (l)-[:TRATA_SOBRE]->(t);
MATCH (l:Libro {isbn:'ISBN-002'}), (t:Tema {codigo:'CIENCIA'})
MERGE (l)-[:TRATA_SOBRE]->(t);
MATCH (l:Libro {isbn:'ISBN-003'}), (t:Tema {codigo:'NATURALEZA'})
MERGE (l)-[:TRATA_SOBRE]->(t);

MATCH (p:Lector {id:'L-001'}), (l:Libro {isbn:'ISBN-001'})
MERGE (p)-[:LEYO]->(l);
