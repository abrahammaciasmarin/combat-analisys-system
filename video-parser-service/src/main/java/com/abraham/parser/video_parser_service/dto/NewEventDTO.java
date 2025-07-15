package com.abraham.parser.video_parser_service.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class NewEventDTO {
    private String sample_id;
    private String boss_in_turn;
}
