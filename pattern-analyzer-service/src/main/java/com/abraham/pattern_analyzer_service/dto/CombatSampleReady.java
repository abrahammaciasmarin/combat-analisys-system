package com.abraham.pattern_analyzer_service.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Builder
@Getter
@Setter
@ToString
public class CombatSampleReady {

    @JsonProperty("sample_id")
    private String sampleId;
    @JsonProperty("boss")
    private String boss;
    @JsonProperty("game")
    private String game;
    @JsonProperty("total_frames")
    private String totalFrames;

}

