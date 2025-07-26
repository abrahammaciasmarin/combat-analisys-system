package com.abraham.pattern_analyzer_service.messaging;


import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

import lombok.extern.log4j.Log4j2;
@Log4j2
@Component
public class QueueListener {

    @RabbitListener(queues = "event.queue")
    public void handleSampleReady(String messageJson) {
        log.info("Message Received: {}", messageJson);
        // Aquí puedes deserializar el JSON y lanzar el análisis por sample_id
    }
}
