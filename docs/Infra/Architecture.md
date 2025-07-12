# Diagrama de Arquitectura

```mermaid
flowchart LR
  subgraph Infraestructura
    localstack[(LocalStack)]
    postgres[(PostgreSQL)]
    mongo[(MongoDB)]
    rabbitmq[(RabbitMQ)]
  end

  subgraph Servicios
    vps[Video Parser]
    pas[Pattern Analyzer]
    ses[Suggestion Engine]
    ds[Dashboard]
  end

  vps -->|Cargas video / S3| localstack
  vps -->|Publica eventos| rabbitmq
  rabbitmq -->|Consume| pas
  pas -->|Guarda patrones| postgres
  pas -->|Guarda eventos| mongo
  pas -->|Publica análisis| rabbitmq
  rabbitmq -->|Consume| ses
  ses -->|Carga patrones| postgres
  ses -->|Envía sugerencias| rabbitmq
  rabbitmq -->|Consume| ds
  ds -->|Lee datos| postgres & mongo

Cuando tu sitio de docs renderice Markdown puedes activar el plugin de Mermaid para verlo inline.

---

## 3. Opción imagen estática

1. Abre [mermaid.live](https://mermaid.live/) y pega únicamente el bloque dentro de ```mermaid …```.  
2. Ajusta tamaños o colores y haz clic en **Export** → **PNG** (o **SVG**).  
3. Guarda el archivo como `docs/Infra/architecture.png`.  
4. En `docs/Infra/Architecture.md` escribe:

   ```markdown
   # Diagrama de Arquitectura

   ![Arquitectura del sistema](architecture.png)
