package com.abraham.parser.video_parser_service.service.impl;

import com.abraham.parser.video_parser_service.dto.EventDTO;
import com.abraham.parser.video_parser_service.dto.NewEventDTO;
import com.abraham.parser.video_parser_service.enity.Detections;
import com.abraham.parser.video_parser_service.enity.Event;
import com.abraham.parser.video_parser_service.event.EventPublisher;
import com.abraham.parser.video_parser_service.exceptions.AlreadyExistsException;
import com.abraham.parser.video_parser_service.exceptions.NotFoundException;
import com.abraham.parser.video_parser_service.repository.EventRepository;
import com.abraham.parser.video_parser_service.service.EventService;
import lombok.extern.log4j.Log4j2;
import org.bson.types.ObjectId;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


@Log4j2
@Service
public class EventServiceImpl implements EventService {

    private final EventRepository eventRepository;
    private final EventPublisher eventPublisher;

    @Autowired
    public EventServiceImpl(EventRepository eventRepository, EventPublisher eventPublisher) {
        this.eventRepository = eventRepository;
        this.eventPublisher = eventPublisher;
    }

    @Override
    public Event save(EventDTO eventDTO) throws AlreadyExistsException {
        log.info("Saving new event in data base: {}", eventDTO.toString());
        Event event = Event.builder()
                .id(eventDTO.getId())
                .detections(eventDTO.getDetections())
                .boss_in_turn(eventDTO.getBoss_in_turn())
                .frame_id(eventDTO.getFrame_id())
                .sample_id(eventDTO.getSample_id())
                .source(eventDTO.getSource())
                .timestamp(eventDTO.getTimestamp())
                .build();
        NewEventDTO newEventDTO = NewEventDTO.builder()
                .boss_in_turn(event.getBoss_in_turn())
                .sample_id(event.getSample_id())
                .build();
        eventPublisher.publishNewEventMessage(newEventDTO);
        return eventRepository.save(event);
    }

    @Override
    public EventDTO getById(ObjectId id) throws NotFoundException {
        log.info("Getting event from data base with objectId : {}", id.toString());
        Event event = eventRepository.findById(id).orElseThrow(() -> new NotFoundException("The event does not exists!!"));
        EventDTO eventDTO = new EventDTO();
        BeanUtils.copyProperties(event, eventDTO);
        return eventDTO;
    }
}
