package com.abraham.parser.video_parser_service.enity;

public enum Source {

    YOLO("Visual system detection YOLO"),
    OPENCV("Visual process with OpenCV"),
    MANUAL("Event entered manually"),
    OTHER("Not defined fount");

    private final String description;

    Source(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    public static Source fromString(String source) {
        for (Source s : Source.values()) {
            if (s.name().equalsIgnoreCase(source)) {
                return s;
            }
        }
        return Source.OTHER;
    }


}
