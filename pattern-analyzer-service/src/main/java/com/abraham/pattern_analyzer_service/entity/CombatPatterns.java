package com.abraham.pattern_analyzer_service.entity;

import lombok.*;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Builder
@Document(collection = "combat_patterns")
public class CombatPatterns {

    private String sample_id;
    private String boss_in_turn;
    private String pattern_id;
    private List<String>sequence;
    private String strategyTag;
    private String threatLevel;
    private Integer startFrame;
    private Integer endFrame;
    private String phase;
    private Integer occurrences;
    private String schema_version;
}
