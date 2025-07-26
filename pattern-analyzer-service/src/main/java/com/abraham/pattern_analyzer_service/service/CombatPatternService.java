package com.abraham.pattern_analyzer_service.service;

import com.abraham.pattern_analyzer_service.entity.CombatPatterns;
import com.mongodb.MongoClientException;

public interface CombatPatternService {
    public CombatPatterns save(CombatPatterns pattern) throws MongoClientException;
    public void analyzeEvents(String events);
}
