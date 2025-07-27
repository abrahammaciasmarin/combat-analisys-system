**Aplicación del patrón CQRS al sistema**

| Componente | Responsabilidad | Tipo de operación | Ventajas |
|:----------------:|:----------------:|:----------------:|:----------------:|
| Video Parser Service Command | Procesa el video y almacena los frames en MongoDB (db-combat-events)   | Command | Desacoplado del acceso a datos<br>- Puede optimizarse para escritura masiva |
| Video Parser Service Query   | Expone endpoint para consultar frames por sample_id, game, boss | Query | Optimizado con Streaming chunk para consultas que retornan gran cantidad de documentos |

**Importancia del CPU en el Video Parser Service Query**

El CPU es crítico en el Video Parser Service Query, especialmente para manejar consultas de alto volumen y filtros complejos sobre miles de frames por video.

**Razones técnicas**

* __Deserialización_de_documentos__: MongoDB devuelve BSON, que debe transformarse a objetos JSON. Esto requiere ciclos del CPU, sobre todo si los documentos son grandes o tienen arrays anidados como detections.

* __Aplicación_de_filtros_lógicos__: Consultas por phase, action, confidence, o incluso subagregaciones tipo $group, $sort, $project demandan procesamiento intensivo en el servicio.


**Optimizaciones posibles para mitigar la carga del CPU**

| Estrategia | Beneficio | Recomendación |
|:----------------:|:----------------:|:----------------:|
| **Índices en MongoDB** | Reduce el volumen de documentos escaneados | Indexar por sample_id, game, boss |
| **Proyecciones específicas** | Solo se consulta lo necesario | Evita consultar el array completo de detections si no se usa |
| **Workers en paralelo** | Escala el CPU horizontalmente | El servicio puede correr con múltiples threads/instancias | 

**Streaming con chunked response**

El streaming con chunked response es una técnica que permite enviar datos en partes (cunks) mientras se procesan, en lugar de esperar a que toda la consulta termine. Esto es especialmente útil para manejar grandes volúmenes de datos como los miles de documentos generados por analizar el video.

**Ventajas del streaming**

* Reducción de latencia: Los datos comienzan a enviarse tan pronto como están disponibles, mejorando la experiencia del usuario.

* Tolerancia a fallos: Si la conexión se interrumpe, el cliente puede reanudar desde el último chunk recibido.

**Implementación técnica**

1. Configuración del microservicio receptor: Asegúrarse de que el Pattern Analyzer Service soporte respuestas chunked.

2. División de datos en chunks: Dividir los documentos en bloques manejables (por ejemplo, 100 documentos por chunk).

3. Manejo de errores: Implementar lógica para reintentar o reanudar la transmisión en caso de fallos.

**Nota importante**

En este caso, no se enviarán los frames por streaming para ser renderizados, sino que serán documentos de MongoDB con las acciones detectadas por YOLO en los frames. Esto asegura que el cliente reciba información procesada y estructurada, optimizando el uso de recursos y la experiencia del usuario.

**Uso del streaming en el Pattern Analyzer Service**

El streaming será utilizado por el Pattern Analyzer Service para trabajar con los datos en busca de patrones. Este servicio los procesará internamente para identificar patrones recurrentes y generar insights tácticos. Esto evita time outs debido a la naturaleza de la respuestas del Video Parser Query. 
La manera en que el Pattern Analyzer Service sabra que inofrmacion pedir, sera atra vez de un evento publicado en una cola de RabbitMQ, en el cual se le informara que un video acaba de ser procesado y la informacion extraida esta lista para ser analizada.

Este evento contendrá almenos el sample_id, game y boss del video que acaba de ser procesado. Podría incluir también metadatos útiles como la duración del video, el número total de frames procesados, o un timestamp de finalización.

Cuando pattern-analyzer recibe el evento, solicita el stream de datos al video-parser-query con el sample_id, game y boss obtenidos del evento de la cola, el pattern-analyzer ahora sabe exactamente qué video necesita analizar.
