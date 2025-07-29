package com.abraham.video_parser_service_query.entity;

import lombok.*;

import java.util.List;

@NoArgsConstructor
@AllArgsConstructor
@Setter
@Getter
@ToString
public class Detections {

    /*
    *
    * object: str
    confidence: float
    bbox: List[int]
    action: str
    duration: float
    phase: str
    player_action: bool
    *
    * */

    private float confidence;
    private List<Integer> bbox;
    private String action;
    private float duration;
    private String phase;
    private boolean playerAction;
}
