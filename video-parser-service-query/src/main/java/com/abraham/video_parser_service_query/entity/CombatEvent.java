package com.abraham.video_parser_service_query.entity;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.CompoundIndexes;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;

@Builder
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@ToString
@Document(collection = "combat_events")
@CompoundIndexes({
        @CompoundIndex(name = "sample_game_boss_idx", def = "{'sample_id': 1, 'game': 1, 'boss': 1}")
})
public class CombatEvent {

    /*
    * timestamp: str
    sample_id: str
    boss: str
    game: str
    source: str
    frame_id: int
    * */

        @Id
        private String id;
        private String timestamp;
        @Field("sample_id")
        private String sampleId;
        private String boss;
        private String game;
        private String source;
        @Field("frame_id")
        private Integer frameId;
        private List<Detections> detections;
}
