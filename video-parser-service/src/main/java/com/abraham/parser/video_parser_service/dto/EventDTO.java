package com.abraham.parser.video_parser_service.dto;

import com.abraham.parser.video_parser_service.enity.Detections;
import com.abraham.parser.video_parser_service.enity.Source;
import lombok.*;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;

@AllArgsConstructor
@NoArgsConstructor
@Data
@ToString
public class EventDTO {
    private ObjectId id;
    private String sample_id;
    private String boss_in_turn;
    private String timestamp;
    private Source source;
    private Long frame_id;
    private List<Detections> detections;

}
