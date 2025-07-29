package com.abraham.video_parser_service_query.controller;


import com.abraham.video_parser_service_query.entity.CombatEvent;
import com.abraham.video_parser_service_query.service.CombatEventService;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.ServletOutputStream;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.log4j.Log4j2;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.stream.Stream;

@Log4j2
@RequestMapping ("/api")
@RestController
public class CombatEventsStreamingController {

    private final MongoTemplate mongoTemplate;
    private final ObjectMapper objectMapper;

    private final CombatEventService combatEventService;

    public CombatEventsStreamingController(MongoTemplate mongoTemplate, ObjectMapper objectMapper, CombatEventService combatEventService) {
        this.mongoTemplate = mongoTemplate;
        this.objectMapper = objectMapper;
        this.combatEventService = combatEventService;
    }

    //This controller receives the request from pattern-analyzer-service
    @GetMapping(value = "/documents", produces = MediaType.APPLICATION_NDJSON_VALUE)
    public void streamDocuments(
            @RequestParam("sampleId") String sampleId,
            @RequestParam("boss") String boss,
            @RequestParam("game") String game,
            HttpServletResponse response) throws IOException {


        // --- KEY STEP: Decode manually the parameters if contains %20 ---
        String decodedBoss = URLDecoder.decode(boss, StandardCharsets.UTF_8);
        String decodedGame = URLDecoder.decode(game, StandardCharsets.UTF_8);
        String decodedSampleId = URLDecoder.decode(sampleId, StandardCharsets.UTF_8);

        log.info("Request received, retreiving actions with params: {} {} {}", sampleId, boss, game);
        response.setContentType(MediaType.APPLICATION_NDJSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        response.setHeader("Transfer-Encoding", "chunked");

        //Combat Event service use the decoded parameters to query the database and returns Stream<CombatEvent>
        try (ServletOutputStream outputStream = response.getOutputStream();
             JsonGenerator jsonGenerator = objectMapper.getFactory().createGenerator(outputStream)) {

            Stream<CombatEvent> combatEventStream = combatEventService.getDocumentsBySampleId(decodedSampleId, decodedBoss, decodedGame);
            //for each combat event, it serialize to JSON and it's written to the HttpServletResponse.getOutputStream() adding a \n after each object to achieve with ndjson
            combatEventStream.forEach(doc -> {
                log.info(doc.toString());
                try {
                    jsonGenerator.writeObject(doc);
                    jsonGenerator.writeRaw('\n');
                    jsonGenerator.flush();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
        }
    }
}
