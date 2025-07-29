package com.abraham.video_parser_service_query.repository;

import com.abraham.video_parser_service_query.entity.CombatEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.stream.Stream;

@Repository
public interface CombatEventRepository extends MongoRepository<CombatEvent, String> {


    @Query("{ 'sample_id': ?0, 'boss': ?1, 'game': ?2 }")
    Stream<CombatEvent> findBySampleIdAndBossAndGame(String sampleID, String boss, String game );
}
