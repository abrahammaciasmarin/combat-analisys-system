# ADR 0001: SNS + SQS vs RabbitMQ

## Context  
We need a queuing system for asynchronous communication.

## Options Considered  
- Amazon SNS + SQS  
- RabbitMQ

## Desision
Use **RabbitMQ** on-premises/prototype for simplicity and flexibility.
Evaluate migrating to SNS + SQS on AWS production if workload increases.

## Consecuences  
- + Full control of the broker
- – Own maintenance and no AWS auto-scaling


## Contexto  
Necesitamos un sistema de colas para comunicación asíncrona

## Opciones consideradas  
- Amazon SNS + SQS  
- RabbitMQ

## Decisión  
Usar **RabbitMQ** en local/prototipo por simplicidad y flexibilidad.  
Evaluar migración a SNS+SQS en AWS producción si la carga crece.

## Consecuencias  
- + Control total del broker  
- – Mantenimiento propio y sin escalado automático de AWS  
