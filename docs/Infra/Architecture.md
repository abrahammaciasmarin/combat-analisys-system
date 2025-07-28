# Architecture Diagram

This diagram represents the complete flow of the Combat Analysis system, from uploading the video until the visualization of suggested tactics.

![Architecture Diagram](Combat_Analysis_System_Architecture.png)

## 🧭 Main Components

- **Application Tier**: It contains all the microservices that process, analyze and suggest.
- **Messaging Layer**: RabbitMQ 3 queues: `combat-events-queue`, `pattern-analysis-queue` y `tactical-tips-queue`.
- **Data Layer**: MongoDB by context (`events`, `patterns`, `suggestions`).
- **Frontend**: A dashboard that consumes the endpoint `/suggestions` y respond to events in real time.

Each microservice establishes communication through queues, favoring synchronous communication, scalability and modularity.



# Diagrama de Arquitectura

Este diagrama representa el flujo completo del sistema Combat Analysis, desde la carga de video hasta la visualización de tácticas sugeridas.

![Diagrama de Arquitectura](Combat_Analysis_System_Architecture.png)

## 🧭 Componentes Principales

- **Application Tier**: contiene los microservicios que procesan, analizan y recomiendan.
- **Messaging Layer**: RabbitMQ con tres colas: `combat-events-queue`, `pattern-analysis-queue` y `tactical-tips-queue`.
- **Data Layer**: MongoDB segmentados por contexto (`events`, `patterns`, `suggestions`).
- **Frontend**: Un dashboard que consume el endpoint `/suggestions` y responde a eventos en tiempo real.

Cada microservicio se comunica mediante colas, favoreciendo la asincronía, la escalabilidad y la modularidad.

