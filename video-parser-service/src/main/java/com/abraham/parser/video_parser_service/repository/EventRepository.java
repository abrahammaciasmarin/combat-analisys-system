package com.abraham.parser.video_parser_service.repository;

import com.abraham.parser.video_parser_service.enity.Event;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EventRepository extends MongoRepository<Event, ObjectId> {
}
