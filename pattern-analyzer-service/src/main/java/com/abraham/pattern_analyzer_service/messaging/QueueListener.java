package com.abraham.pattern_analyzer_service.messaging;


import com.abraham.pattern_analyzer_service.client.VideoParserServiceClient;
import com.abraham.pattern_analyzer_service.dto.CombatSampleReady;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import lombok.extern.log4j.Log4j2;
import reactor.core.publisher.Flux;

@Log4j2
@Component
public class QueueListener {

    @Autowired
    private ObjectMapper objectMapper;

    private final VideoParserServiceClient videoParserServiceClient;

    public QueueListener(VideoParserServiceClient videoParserServiceClient) {
        this.videoParserServiceClient = videoParserServiceClient;
    }

    //This listener is waiting for the event from Video-Parser-Service witch sampleId, boss, game
    @RabbitListener(queues = "combat-events-queue")
    public void handleSampleReady(String messageJson) {
        log.info("Message Received: {}", messageJson);
        try {
            log.info("Converting message received into CombatSampleReady Pojo");
            CombatSampleReady combatSampleReady = objectMapper.readValue(messageJson, CombatSampleReady.class);
            Flux<JsonNode> jsonNodeFlux = videoParserServiceClient.getDocumentStream(combatSampleReady);
            //Here is subscribed with (doOnNext, doOnError, subscribe) to process each JsonNode, as it arrives
            jsonNodeFlux
                    .doOnNext(jsonNode -> {
                        log.info("Received Streaming: {}", jsonNode.toPrettyString());
                    })
                    .doOnError(error ->{
                        log.error("Error Processing JSON!!");
                    })
                    .doOnComplete(()->{
                        log.info("JSON Completed!!");
                    })
                    .subscribe();

        } catch (JsonProcessingException e) {
            log.error(e.getMessage());
            throw new RuntimeException(e);
        }
    }
}
