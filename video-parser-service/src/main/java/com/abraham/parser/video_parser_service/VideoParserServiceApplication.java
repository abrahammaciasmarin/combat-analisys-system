package com.abraham.parser.video_parser_service;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = "com.abraham.parser.video_parser_service")
public class VideoParserServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(VideoParserServiceApplication.class, args);
	}

}
