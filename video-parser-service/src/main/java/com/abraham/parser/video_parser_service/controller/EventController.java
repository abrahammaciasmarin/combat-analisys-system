package com.abraham.parser.video_parser_service.controller;


import com.abraham.parser.video_parser_service.dto.EventDTO;
import com.abraham.parser.video_parser_service.exceptions.AlreadyExistsException;
import com.abraham.parser.video_parser_service.exceptions.NotFoundException;
import com.abraham.parser.video_parser_service.service.impl.EventServiceImpl;
import lombok.extern.log4j.Log4j2;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.w3c.dom.events.Event;

@Log4j2
@RestController
@RequestMapping("/api/events")
public class EventController {

    private final EventServiceImpl eventServiceImpl;

    @Autowired
    public EventController(EventServiceImpl eventServiceImpl) {
        this.eventServiceImpl = eventServiceImpl;
    }

    @PostMapping("/save")
    public ResponseEntity<EventDTO> save(@RequestBody EventDTO eventDTO) throws AlreadyExistsException {
        eventServiceImpl.save(eventDTO);
        return new ResponseEntity<>(eventDTO, HttpStatus.OK);
    }

    @GetMapping("/get-event/{id}")
    public ResponseEntity<EventDTO> getEvent(@PathVariable ObjectId id) throws NotFoundException {
        return new ResponseEntity<>(this.eventServiceImpl.getById(id), HttpStatus.OK);
    }

}
