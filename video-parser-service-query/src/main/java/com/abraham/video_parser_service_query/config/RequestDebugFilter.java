package com.abraham.video_parser_service_query.config;

// En el proyecto video-parser-service-query
// Crea esta clase: src/main/java/com/yourcompany/videoparserservice/config/RequestDebugFilter.java
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Enumeration;
import java.util.Map;

@Component
public class RequestDebugFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger(RequestDebugFilter.class);

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {

        log.info("--- Incoming Request Debug Filter ---");
        log.info("Request URL: {}", request.getRequestURL());
        log.info("Query String: {}", request.getQueryString()); // Esto mostrará los %20 si el contenedor NO los decodifica

        log.info("Headers:");
        Enumeration<String> headerNames = request.getHeaderNames();
        while (headerNames.hasMoreElements()) {
            String headerName = headerNames.nextElement();
            log.info("  {}: {}", headerName, request.getHeader(headerName));
        }

        log.info("Parameters (from request.getParameter()):");
        Map<String, String[]> params = request.getParameterMap();
        params.forEach((name, values) -> {
            for (String value : values) {
                log.info("  {}: {}", name, value); // ¡Esto DEBERÍA mostrar los valores decodificados!
            }
        });
        log.info("--- End Incoming Request Debug Filter ---");

        filterChain.doFilter(request, response);
    }
}
