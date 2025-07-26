package com.abraham.pattern_analyzer_service.service.impl;

import com.abraham.pattern_analyzer_service.entity.CombatPatterns;
import com.abraham.pattern_analyzer_service.repository.CombatPatternRepository;
import com.abraham.pattern_analyzer_service.service.CombatPatternService;
import com.mongodb.MongoClientException;
import org.springframework.stereotype.Service;

@Service
public class CombatPatternServiceImpl implements CombatPatternService {

    private final CombatPatternRepository combatPatternRepository;

    public CombatPatternServiceImpl(CombatPatternRepository combatPatternRepository) {
        this.combatPatternRepository = combatPatternRepository;
    }

    @Override
    public CombatPatterns save(CombatPatterns pattern) throws MongoClientException {
        return combatPatternRepository.save(pattern);
    }

    @Override
    public void analyzeEvents(String events) {

    }
}
