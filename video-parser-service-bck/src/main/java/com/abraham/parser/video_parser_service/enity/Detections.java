package com.abraham.parser.video_parser_service.enity;

import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;

@Data
public class Detections {
    @Field("object")
    private String object;
    @Field("confidence")
    private Double confidence;
    @Field("bbox")
    private List<Integer> bbox;
    @Field("action")
    private String action;
    @Field("duration")
    private Double duration;
    @Field("phase")
    private String phase;
    @Field("game")
    private String game;
    @Field("player_action")
    private Boolean player_action;
}
