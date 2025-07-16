package com.abraham.parser.video_parser_service.enity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;

@AllArgsConstructor
@NoArgsConstructor
@Data
@Builder
@Document(collection = "events")
public class Event {
    @Id
    private ObjectId id;
    @Field("sample_id")
    private String sample_id;
    @Field("boss_in_turn")
    private String boss_in_turn;
    @Field("timestamp")
    private String timestamp;
    @Field("source")
    private Source source;
    @Field("frame_id")
    private Long frame_id;
    private List<Detections> detections;
}
