package com.abraham.pattern_analyzer_service.client;

import com.abraham.pattern_analyzer_service.dto.CombatSampleReady;
import com.fasterxml.jackson.databind.JsonNode;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriComponentsBuilder;
import reactor.core.publisher.Flux;


@Log4j2
@Component
public class VideoParserServiceClient {

    @Value("${video-parser-service.base-url}")
    private String videoParserBaseUrl;

    @Value("${video-parser-service.query-path}")
    private String queryPath;


    private final WebClient webClient;

    public VideoParserServiceClient(WebClient.Builder webBuilder) {
        this.webClient = webBuilder.build();
    }

    //This method receives the data from the Event
    public Flux<JsonNode> getDocumentStream(CombatSampleReady combatSampleReady){
        log.info("These are my query params: {}", combatSampleReady.toString());

        //Construction of complete URL and codified: example http://localhost:8081/api/documents?sampleId=01&boss=Ancient%20Ape&game=Black%20Myth%20Wukong
        String fullPath = UriComponentsBuilder.fromUriString(videoParserBaseUrl)
                .path(queryPath)
                .queryParam("sampleId",combatSampleReady.getSampleId())
                .queryParam("boss",combatSampleReady.getBoss())
                .queryParam("game",combatSampleReady.getGame()).toUriString();
        log.info("Getting Stream from Video_Parser_Service: {}", fullPath);
        //Do the call to the endpoint
        return webClient.get()
                .uri(fullPath)
                .accept(MediaType.APPLICATION_NDJSON)
                .retrieve()
                .bodyToFlux(JsonNode.class);
    }
}
