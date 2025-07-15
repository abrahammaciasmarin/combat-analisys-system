package com.abraham.parser.video_parser_service.service;

import com.abraham.parser.video_parser_service.dto.EventDTO;
import com.abraham.parser.video_parser_service.enity.Event;
import com.abraham.parser.video_parser_service.exceptions.AlreadyExistsException;
import com.abraham.parser.video_parser_service.exceptions.NotFoundException;
import org.bson.types.ObjectId;

public interface EventService {

    Event save(EventDTO eventDTO) throws AlreadyExistsException;

    EventDTO getById(ObjectId id) throws NotFoundException;

}
