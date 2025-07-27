**Aplicación del patrón CQRS al sistema**

| Componente | Responsabilidad | Tipo de operación | Ventajas |
|:----------------:|:----------------:|:----------------:|:----------------:|
| Video Parser Service Command | Procesa el video y almacena los frames en MongoDB (db-combat-events)   | Command | Desacoplado del acceso a datos<br>- Puede optimizarse para escritura masiva |
| Video Parser Service Query   | Expone endpoint para consultar frames por sample_id, game, boss | Query | Optimizado con Streaming chunk para consultas que retornan gran cantidad de documentos |


**Optimización del Video Parser Service Command con GPU**

El Video Parser Service command , está diseñado para trabajar con GPU. Esto se debe a que utiliza el modelo YOLOv8l para procesar los videos, lo que hace que el análisis sea significativamente más rápido en comparación con el uso de CPU.

**Ventajas de usar GPU en el Video Parser Service Command**

* Mayor velocidad de procesamiento: Las GPUs están optimizadas para operaciones paralelas, lo que acelera el análisis de video.

* Eficiencia en tareas intensivas: El modelo YOLO aprovecha la arquitectura de las GPUs para manejar grandes volúmenes de datos de manera eficiente.

* Reducción de latencia: Al procesar los videos en tiempo real, las GPUs minimizan la latencia, mejorando la experiencia del usuario.

Con esta optimización, el Video Processing Service puede manejar análisis de video en tiempo real de manera más efectiva, lo que es crucial para sistemas que dependen de decisiones rápidas basadas en datos visuales.