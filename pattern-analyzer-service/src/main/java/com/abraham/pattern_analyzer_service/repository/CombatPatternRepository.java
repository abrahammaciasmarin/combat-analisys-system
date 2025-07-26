package com.abraham.pattern_analyzer_service.repository;

import com.abraham.pattern_analyzer_service.entity.CombatPatterns;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CombatPatternRepository extends MongoRepository<CombatPatterns, String> {
}
