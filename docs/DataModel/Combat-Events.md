🗃️ Modelo de Persistencia en MongoDB
🛠️ Diseño de Persistencia en DB-events

📂 Estructura de Colecciones

Colección principal: combat-events

```json
{
  "_id": {
    "$oid": "688110c097ef8c3cfa749b2a"
  },
  "timestamp": "2025-07-23T16:41:36.053194",
  "sample_id": "01",
  "game": "Sekiro",
  "boss": "Ishin",
  "source": "YOLO",
  "frame_id": 30,
  "detections": [
    {
      "action": "ishin_running",
      "confidence": 0.9094690680503845,
      "bbox": [
        612,
        733,
        1081,
        1049
      ],
      "phase": "02",
      "player_action": false
    }
  ]
}
```
🗂️ Índices sugeridos

sample_id

game

boss

source

action

phase

player_action


Descripción de propiedades:

timestamp: Marca de tiempo en formato ISO 8601 que indica cuándo se generó el evento.

sample_id: Numero de video muestra de donde se extrajo el frame.

game: Nombre del juego en el que ocurre el evento.

boss: Nombre del jefe activo durante el evento.

source: Origen del evento, en este caso, el sistema YOLO.

frame_id: Identificador único del frame analizado.

detections: Lista de acciones detectadss en el frame.

  action: Nombre de la accion detectada.
  
  confidence: Nivel de confianza de la detección (valor entre 0 y 1).
  
  bbox: Coordenadas y tamaño del cuadro delimitador del objeto detectado (x1, y1, x2, y2).
  
  phase: Fase del combate en la que ocurre la acción.
  
  player_action: Indica si la acción fue realizada por el jugador (true/false).
