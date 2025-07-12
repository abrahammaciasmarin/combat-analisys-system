# ADR 0001: SNS + SQS vs RabbitMQ

## Contexto  
Necesitamos un sistema de colas para comunicación asíncrona en local y producción.

## Opciones consideradas  
- Amazon SNS + SQS  
- RabbitMQ

## Decisión  
Usar **RabbitMQ** en local/prototipo por simplicidad y flexibilidad.  
Evaluar migración a SNS+SQS en AWS producción si la carga crece.

## Consecuencias  
- + Control total del broker  
- – Mantenimiento propio y sin escalado automático de AWS  
