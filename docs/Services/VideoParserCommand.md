**Aplicación del patrón CQRS al sistema**

| Componente | Responsabilidad | Tipo de operación | Ventajas |
|:----------------:|:----------------:|:----------------:|:----------------:|
| Video Parser Service Command | Procesa el video y almacena los frames en MongoDB (db-combat-events)   | Command | Desacoplado del acceso a datos<br>- Puede optimizarse para escritura masiva |
| Video Parser Service Query   | Expone endpoint para consultar frames por sample_id, game, boss | Query | Optimizado con Streaming chunk para consultas que retornan gran cantidad de documentos |
