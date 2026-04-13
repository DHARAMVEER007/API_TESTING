package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api/cluster/nodes")
class NodeController {
    @GetMapping
    public ResponseEntity<?> getNodes() {
        Map<String, Object> response = Map.of("records", List.of(
                Map.of(
                        "uuid", "a1b2c3d4-5678-90ab-cdef-1234567890ab",
                        "name", "node-01",
                        "state", "healthy",
                        "model", "FAS2750",
                        "serial_number", "123456789",
                        "ha", Map.of("partner", "node-02", "state", "connected"),
                        "version", Map.of("full", "NetApp Release 9.12.1P5")
                ),
                Map.of(
                        "uuid", "b2c3d4e5-6789-01ab-cdef-2345678901bc",
                        "name", "node-02",
                        "state", "healthy",
                        "model", "FAS2750",
                        "serial_number", "987654321"
                )
        ));
        return ResponseEntity.ok(response);
    }
}
