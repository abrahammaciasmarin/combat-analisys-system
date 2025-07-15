package com.abraham.parser.video_parser_service.event;

import com.abraham.parser.video_parser_service.config.RabbitMqConfig;
import com.abraham.parser.video_parser_service.dto.NewEventDTO;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.log4j.Log4j2;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Log4j2
@Service
public class EventPublisher {


    private final RabbitTemplate rabbitTemplate;
    private final ObjectMapper objectMapper;

    @Autowired
    public EventPublisher(RabbitTemplate rabbitTemplate, ObjectMapper objectMapper) {
        this.rabbitTemplate = rabbitTemplate;
        this.objectMapper = objectMapper;
    }

    public void publishNewEventMessage(NewEventDTO newEventDTO) {
        Map<String, Object> message = new HashMap<>();
        message.put("sample_id", newEventDTO.getSample_id());
        message.put("boss_in_turn", newEventDTO.getBoss_in_turn());
        message.put("trigger", "new_event");
        String jsonMessage = null;
        try {
            jsonMessage = objectMapper.writeValueAsString(message);
            log.info("Sending new event to pattern-analyzer-service: {}",message.toString());
            rabbitTemplate.convertAndSend(
                    RabbitMqConfig.EXCHANGE,
                    RabbitMqConfig.ROUTING_KEY,
                    jsonMessage
            );
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}