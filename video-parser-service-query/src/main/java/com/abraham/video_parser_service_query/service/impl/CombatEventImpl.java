package com.abraham.video_parser_service_query.service.impl;

import com.abraham.video_parser_service_query.entity.CombatEvent;
import com.abraham.video_parser_service_query.repository.CombatEventRepository;
import com.abraham.video_parser_service_query.service.CombatEventService;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Stream;

@Log4j2
@Service
public class CombatEventImpl implements CombatEventService {


    private final CombatEventRepository combatEventRepository;

    public CombatEventImpl(CombatEventRepository combatEventRepository) {
        this.combatEventRepository = combatEventRepository;
    }


    @Override
    public Stream<CombatEvent> getDocumentsBySampleId(String sampleId, String boss, String game) {
        log.info("Getting documents by from game: {}, boss: {}, sample Id: {}", game, boss,sampleId);
        return combatEventRepository.findBySampleIdAndBossAndGame(sampleId, boss, game);
    }
}
