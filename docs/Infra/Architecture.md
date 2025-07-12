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

  vps --> rabbitmq
  rabbitmq --> pas
  pas --> postgres & mongo
  pas --> rabbitmq
  rabbitmq --> ses
  ses --> postgres
  ses --> rabbitmq
  rabbitmq --> ds
  ds --> postgres & mongo

Ese triple backtick de cierre (` ``` `) es obligatorio.

---

## 🛠️ Si ya lo corregiste y sigue fallando…

- Verifica que tu editor de Markdown (VSCode, Obsidian, etc.) soporte Mermaid.  
- Si estás en GitHub, recuerda que Markdown por defecto **no renderiza Mermaid** a menos que uses extensiones (como en GitHub Pages con MkDocs o Docusaurus).

Alternativas:

- Exportar el diagrama desde [mermaid.live](https://mermaid.live/) como imagen (`PNG` o `SVG`)  
- Guardar en `docs/Infra/architecture.png`  
- Y enlazarlo desde `Architecture.md` así:

```markdown
![Diagrama del sistema](architecture.png)
