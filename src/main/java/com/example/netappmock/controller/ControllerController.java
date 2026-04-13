package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

import static java.util.Map.entry;

@RestController
@RequestMapping("/api/storage/controllers")
public class ControllerController {

    @GetMapping
    public ResponseEntity<Map<String, Object>> getControllers() {
        Map<String, Object> controller1 = Map.ofEntries(
                entry("uuid", "ctrl-uuid-001"),
                entry("name", "node-01"),
                entry("model", "FAS2750"),
                entry("vendor", "NetApp"),
                entry("serial_number", "SN1234567890"),
                entry("os_version", "NetApp Release 9.12.1P5"),
                entry("location", "Rack 3, DC1"),
                entry("ha", Map.of("partner", "node-02", "state", "connected")),
                entry("cpu", Map.of("cores", 12, "model", "Intel Xeon E5-2630")),
                entry("memory", Map.of("size", "128GB")),
                entry("state", "online")
        );

        Map<String, Object> response = Map.of("records", List.of(controller1));
        return ResponseEntity.ok(response);
    }
}
