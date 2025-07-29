package com.abraham.video_parser_service_query.service;

import com.abraham.video_parser_service_query.entity.CombatEvent;


import java.util.List;
import java.util.stream.Stream;

public interface CombatEventService {

    public Stream<CombatEvent> getDocumentsBySampleId(String sampleId, String boss, String game);

}
