window.EXAM_QUESTIONS={
  "professional": [
    [
      "Cypher",
      "¿Qué cláusula encuentra patrones existentes sin crearlos?",
      [
        "MATCH",
        "CREATE",
        "MERGE",
        "SET"
      ],
      0,
      "MATCH consulta patrones. CREATE siempre crea y MERGE intenta localizar el patrón completo antes de crearlo.",
      "https://neo4j.com/docs/cypher-manual/current/clauses/match/"
    ],
    [
      "Cypher",
      "¿Qué hace OPTIONAL MATCH cuando no se encuentra el patrón opcional?",
      [
        "Descarta siempre toda la fila",
        "Conserva la fila y utiliza null para variables no encontradas",
        "Crea automáticamente el nodo ausente",
        "Inicia una nueva transacción"
      ],
      1,
      "OPTIONAL MATCH se comporta de manera comparable a una unión externa: conserva el contexto anterior aunque falte la coincidencia.",
      "https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/"
    ],
    [
      "Cypher",
      "¿Cuál devuelve solo ISBN y título de los libros escritos por un autor dado?",
      [
        "MATCH (a:Autor {id:$id})-[:ESCRIBIO]->(l:Libro) RETURN l.isbn, l.titulo",
        "MATCH (a:Autor)<-[:ESCRIBIO]-(l:Libro) RETURN l.isbn, l.titulo",
        "CREATE (a:Autor)-[:ESCRIBIO]->(l:Libro) RETURN l",
        "MATCH (l:Libro) DELETE l RETURN l"
      ],
      0,
      "Importan las etiquetas, la dirección de ESCRIBIO y el uso de un parámetro de consulta.",
      "https://neo4j.com/docs/cypher-manual/current/clauses/match/"
    ],
    [
      "Cypher",
      "¿Para qué sirve WITH en una consulta Cypher?",
      [
        "Definir una base de datos nueva",
        "Pasar y transformar variables entre fases de la consulta",
        "Crear índices automáticamente",
        "Activar OWL"
      ],
      1,
      "WITH controla variables en el pipeline, permite agregaciones y filtrar resultados intermedios.",
      "https://neo4j.com/docs/cypher-manual/current/clauses/with/"
    ],
    [
      "Cypher",
      "En MATCH (a:Autor)-[:ESCRIBIO]->(l:Libro), ¿qué evita contar dos veces el mismo libro si aparece más de una vez en las filas?",
      [
        "count(DISTINCT l)",
        "count(a) + count(l)",
        "MERGE l",
        "REMOVE l"
      ],
      0,
      "DISTINCT dentro de una agregación considera valores diferentes, sin modificar los datos almacenados.",
      "https://neo4j.com/docs/cypher-manual/current/functions/aggregating/"
    ],
    [
      "Importing Data",
      "¿Por qué es recomendable establecer claves únicas antes de una carga repetida con MERGE?",
      [
        "Porque MERGE garantiza equivalencia semántica de cualquier cadena",
        "Porque protege frente a registros con la misma clave de negocio",
        "Porque Cypher prohíbe duplicados por defecto",
        "Porque el CSV se convierte en OWL"
      ],
      1,
      "MERGE y las restricciones se apoyan en claves estables; ni uno ni otras garantizan la calidad semántica de los registros.",
      "https://neo4j.com/docs/cypher-manual/current/schema/constraints/"
    ],
    [
      "Schema & Indexes",
      "Una restricción IS UNIQUE sobre l.isbn implica que…",
      [
        "todo Libro debe tener ISBN",
        "no puede haber dos valores presentes idénticos para esa etiqueta y propiedad",
        "todo libro tendrá un autor",
        "no puede existir más de un libro"
      ],
      1,
      "La unicidad no obliga por sí sola a la existencia de la propiedad.",
      "https://neo4j.com/docs/cypher-manual/current/schema/constraints/"
    ],
    [
      "Schema & Indexes",
      "¿Cuál permite inspeccionar el plan sin ejecutar una consulta que escribe datos?",
      [
        "PROFILE",
        "EXPLAIN",
        "UNWIND",
        "DELETE"
      ],
      1,
      "EXPLAIN presenta el plan sin ejecución; PROFILE sí ejecuta la consulta y muestra métricas.",
      "https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/query-tuning/"
    ],
    [
      "Drivers",
      "En el driver Python oficial, ¿cómo se pasa de forma segura el valor de ISBN?",
      [
        "Concatenando el ISBN al texto Cypher",
        "Como parámetro $isbn asociado a un argumento de la consulta",
        "Como nombre de etiqueta creado con el texto del usuario",
        "Guardándolo en el código fuente"
      ],
      1,
      "Las consultas parametrizadas evitan incorporar valores arbitrarios al código de la consulta.",
      "https://neo4j.com/docs/python-manual/current/query-simple/"
    ],
    [
      "Drivers",
      "¿Qué debe tenerse en cuenta con transacciones gestionadas que pueden reintentarse?",
      [
        "Las operaciones externas no idempotentes dentro de la función pueden duplicarse",
        "Se permite guardar la contraseña en GitHub",
        "Las reejecuciones siempre cambian de base",
        "No existen errores de concurrencia"
      ],
      0,
      "Las funciones de transacción pueden reintentarse; evita efectos laterales no idempotentes.",
      "https://neo4j.com/docs/python-manual/current/transactions/"
    ],
    [
      "Data Modeling",
      "Si una relación entre Persona y Proyecto necesita porcentaje de dedicación y fechas, ¿qué es razonable evaluar?",
      [
        "Atributos de relación o una entidad Asignacion",
        "Un único booleano global",
        "Borrar Proyecto",
        "Convertir todo a etiquetas"
      ],
      0,
      "Elige según cardinalidad, historial y consultas: las propiedades de arista o una entidad intermedia pueden modelar la asignación.",
      "https://graphacademy.neo4j.com/courses/modeling-fundamentals/"
    ],
    [
      "Neo4j Fundamentals",
      "¿Qué diferencia esencial hay entre una relación y un nodo de Neo4j?",
      [
        "La relación es dirigida y tipada y conecta nodos",
        "Solo los nodos pueden tener propiedades",
        "Toda relación es simétrica",
        "Los nodos no tienen etiquetas"
      ],
      0,
      "Las relaciones tienen dirección y tipo; ambos elementos pueden almacenar propiedades.",
      "https://graphacademy.neo4j.com/courses/neo4j-fundamentals/"
    ]
  ],
  "gds": [
    [
      "Algorithms",
      "¿Cuál es el objetivo típico de PageRank?",
      [
        "Encontrar comunidades desconectadas",
        "Estimar importancia estructural a partir de enlaces",
        "Validar shapes SHACL",
        "Importar CSV"
      ],
      1,
      "PageRank calcula una medida de importancia basada en la estructura de enlaces; no equivale automáticamente a importancia empresarial.",
      "https://neo4j.com/docs/graph-data-science/current/algorithms/page-rank/"
    ],
    [
      "Algorithms",
      "¿Qué algoritmo es adecuado para encontrar caminos mínimos con pesos no negativos?",
      [
        "Dijkstra",
        "PageRank",
        "Louvain",
        "Triangle Count"
      ],
      0,
      "Dijkstra trabaja con costes de aristas no negativos; selecciona el algoritmo según los supuestos de los datos.",
      "https://neo4j.com/docs/graph-data-science/current/algorithms/dijkstra-source-target/"
    ],
    [
      "Algorithms",
      "¿Qué tipo de pregunta ayuda a responder Weakly Connected Components?",
      [
        "¿Qué vértices pertenecen a componentes conectadas ignorando la dirección?",
        "¿Cuál es la etiqueta preferida SKOS?",
        "¿Qué registros no tienen ISBN?",
        "¿Qué propiedad es funcional en OWL?"
      ],
      0,
      "WCC identifica componentes conectadas tratando las direcciones como no determinantes para la conectividad.",
      "https://neo4j.com/docs/graph-data-science/current/algorithms/wcc/"
    ],
    [
      "Workflows",
      "¿Qué es una proyección GDS?",
      [
        "Una representación en memoria del grafo para algoritmos",
        "Una copia de seguridad de AuraDB",
        "Un archivo OWL obligatorio",
        "Una base PostgreSQL nueva"
      ],
      0,
      "La proyección selecciona estructura y atributos apropiados para ejecutar algoritmos de GDS.",
      "https://neo4j.com/docs/graph-data-science/current/management-ops/graph-creation/"
    ],
    [
      "Workflows",
      "¿Qué modo suele devolver resultados algorítmicos en filas sin persistirlos automáticamente?",
      [
        "stream",
        "write",
        "drop",
        "schema"
      ],
      0,
      "stream expone resultados; write es un modo pensado para persistir resultados según el algoritmo.",
      "https://neo4j.com/docs/graph-data-science/current/algorithms/"
    ],
    [
      "GDS Library",
      "¿Qué debes comprobar antes de ejecutar un algoritmo sobre una relación ponderada?",
      [
        "Que la propiedad de peso existe, es compatible y tiene semántica apropiada",
        "Que todos los valores son cadenas",
        "Que hay ontología OWL",
        "Que la base contiene solo un nodo"
      ],
      0,
      "Un peso puede representar coste, proximidad o distancia. Los algoritmos tienen requisitos concretos sobre los valores.",
      "https://neo4j.com/docs/graph-data-science/current/algorithms/"
    ],
    [
      "Workflows",
      "¿Qué debe hacerse al terminar con una proyección en memoria que ya no se necesita?",
      [
        "Liberarla con la operación de eliminación de la proyección pertinente",
        "Eliminar los nodos originales de la base",
        "Borrar todos los índices",
        "Ejecutar SHACL"
      ],
      0,
      "Las proyecciones consumen recursos; eliminarlas no debe confundirse con borrar datos persistentes.",
      "https://neo4j.com/docs/graph-data-science/current/management-ops/graph-drop/"
    ]
  ],
  "genai": [
    [
      "GraphRAG & Vectors",
      "¿Cuál es una ventaja de recuperar contexto desde un grafo antes de responder con un LLM?",
      [
        "Poder aportar relaciones y fuentes concretas al contexto",
        "Garantizar cero alucinaciones",
        "Eliminar la necesidad de evaluar respuestas",
        "Evitar todos los problemas de privacidad"
      ],
      0,
      "GraphRAG puede aportar evidencia estructurada y trazable, pero no garantiza por sí mismo respuestas correctas.",
      "https://neo4j.com/docs/neo4j-graphrag-python/current/"
    ],
    [
      "Vectors",
      "¿Qué mide normalmente la similitud vectorial?",
      [
        "Proximidad en un espacio de representaciones",
        "Equivalencia lógica OWL",
        "Validez de ISBN",
        "Correctitud factual garantizada"
      ],
      0,
      "Los embeddings son aproximaciones de similitud; no prueban identidad ni verdad.",
      "https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/"
    ],
    [
      "Data Modeling",
      "¿Qué conviene guardar para poder citar correctamente un fragmento recuperado?",
      [
        "Identificador y procedencia del documento o fragmento",
        "Solo el valor del embedding",
        "La contraseña del proveedor de IA",
        "Únicamente el nombre de la etiqueta"
      ],
      0,
      "Para respuestas trazables hacen falta identificadores, fuentes y relaciones de procedencia.",
      "https://neo4j.com/docs/neo4j-graphrag-python/current/"
    ],
    [
      "GraphRAG & Vectors",
      "¿Qué debería hacer una aplicación cuando no encuentra evidencia suficiente?",
      [
        "Reconocer la insuficiencia y abstenerse o pedir precisión",
        "Inventar un nodo plausible",
        "Asegurar que la respuesta es correcta",
        "Desactivar toda validación"
      ],
      0,
      "Los casos sin evidencia deben formar parte de la evaluación de un sistema RAG.",
      "https://neo4j.com/docs/neo4j-graphrag-python/current/"
    ],
    [
      "Cypher",
      "¿Qué riesgo tiene generar y ejecutar sin control Cypher a partir de texto de usuarios?",
      [
        "Consultas erróneas o con efectos no autorizados",
        "La creación automática de ontologías perfectas",
        "La garantía de mejores índices",
        "Que Cypher no admita WHERE"
      ],
      0,
      "Limita permisos, valida patrones y evita otorgar permisos de escritura a flujos que solo necesitan leer.",
      "https://neo4j.com/docs/cypher-manual/current/"
    ],
    [
      "MCP",
      "¿Qué significa MCP en las arquitecturas modernas de herramientas para IA?",
      [
        "Model Context Protocol",
        "Memory Constraint Procedure",
        "Multi Cypher Projection",
        "Metadata Consistency Predicate"
      ],
      0,
      "MCP describe una interfaz/protocolo de conexión de modelos con herramientas y recursos; comprueba su especificación vigente.",
      "https://modelcontextprotocol.io/specification/"
    ],
    [
      "Drivers",
      "¿Cómo debe gestionar secretos una aplicación Python de GraphRAG?",
      [
        "Variables de entorno o gestores de secretos, sin publicarlos",
        "Valores incrustados en el repositorio",
        "Imprimiéndolos en los logs",
        "Guardándolos como etiquetas del grafo"
      ],
      0,
      "Separar configuración y secretos protege la infraestructura.",
      "https://neo4j.com/docs/python-manual/current/connect/"
    ]
  ]
};
