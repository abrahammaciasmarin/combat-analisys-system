🗃️ Modelo de Persistencia en MongoDB

✅ Opción 1: Persistencia “tal cual”

Ventajas:

Simplicidad de implementación.

El microservicio recibe el JSON y lo inserta directamente.

Muy útil para auditoría o debugging visual.

Limitaciones:

Consultas complejas pueden requerir agregaciones complicadas.

Difícil de versionar o extender si la estructura cambia con el tiempo.

⚙️ Opción 2: Persistencia enriquecida

Transformaciones sugeridas:

Separar campos clave en colecciones relacionadas (por ejemplo, una colección para boss_in_turn, otra para game).

Indexar campos críticos como timestamp, phase, player_action.

Añadir metadatos internos: versión del esquema, tiempo de procesamiento, ID de nodo.

Ventajas:

Mejora el rendimiento en queries complejas.

Facilita visualizaciones por fases, enemigos, juegos, etc.

Puedes hacer análisis predictivo más fácilmente con los datos bien categorizados.

🛠️ Diseño de Persistencia en DB-events

📂 Estructura de Colecciones

Colección principal: events

{
  "_id": "unique_event_id",
  "timestamp": "2025-07-14T13:30:45Z",
  "source": "YOLO",
  "frame_id": 1550,
  "detections": [
    {
      "object": "spear",
      "confidence": 0.91,
      "bbox": [300, 140, 360, 200],
      "action": "thrust",
      "duration": 0.5,
      "phase": "attack",
      "game": "Combat Arena",
      "player_action": true,
      "boss_in_turn": "Dragon King"
    }
  ]
}

Colección secundaria: metadata

{
  "_id": "unique_metadata_id",
  "event_id": "unique_event_id",
  "schema_version": "1.0",
  "processing_time_ms": 15,
  "node_id": "parser_node_01"
}

🗂️ Índices sugeridos

timestamp

source

object

phase

game

player_action

boss_in_turn

Descripción de propiedades:

timestamp: Marca de tiempo en formato ISO 8601 que indica cuándo se generó el evento.

source: Origen del evento, en este caso, el sistema YOLO.

frame_id: Identificador único del cuadro analizado.

detections: Lista de objetos detectados en el cuadro.

object: Nombre del objeto detectado.

confidence: Nivel de confianza de la detección (valor entre 0 y 1).

bbox: Coordenadas del cuadro delimitador del objeto detectado (x1, y1, x2, y2).

action: Acción asociada al objeto detectado.

duration: Duración estimada de la acción en segundos.

phase: Fase del combate en la que ocurre la acción.

game: Nombre del juego en el que ocurre el evento.

player_action: Indica si la acción fue realizada por el jugador (true/false).

boss_in_turn: Nombre del jefe activo durante el evento.

🔄 Estrategias de Versionado

Versionado por esquema: Cada evento incluye un campo schema_version para identificar la versión del esquema.

Migración incremental: Scripts automáticos para actualizar eventos antiguos al nuevo esquema.

🚨 Manejo de Errores

Validación previa: Uso de JSON Schema para validar la estructura antes de insertar.

Logs detallados: Registro de errores en una colección separada error_logs.

Reintentos automáticos: Reprocesamiento de eventos malformados hasta 3 veces antes de descartarlos.