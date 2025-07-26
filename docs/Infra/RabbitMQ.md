# Configuración de Colas – RabbitMQ

En esta arquitectura, RabbitMQ orquesta la mensajería entre los microservicios mediante colas bien definidas. Cada servicio publica o consume mensajes según su responsabilidad.

---

## 🎯 Flujo de mensajes y nombres de colas

| Cola                     | Publica               | Consume              | Tipo de mensaje           |
|--------------------------|-----------------------|----------------------|---------------------------|
| `combat-events-queue`    | `video-parser`        | `pattern-analyzer`   | Eventos brutos del video |
| `pattern-analysis-queue` | `pattern-analyzer`    | `suggestion-engine`  | Patrones detectados      |
| `tactical-tips-queue`    | `suggestion-engine`   | `dashboard`          | Sugerencias de combate   |

---

## 🔧 Detalles técnicos

- Los mensajes se serializan como `JSON`.  
- Cada cola es duradera (`durable: true`) para evitar pérdida en reinicios.  
- Se usa `ack=true` para asegurar que los consumidores procesan correctamente.

---

## 🧪 Ejemplo de mensaje en `combat-events-queue`

```json
{
  "sample_id": "sample_07",
  "game": "Sekiro",
  "boss_in_turn": "Isshin",
  "total_frames": 1533,
  "timestamp": "2025-07-22T18:30:00Z"
}
