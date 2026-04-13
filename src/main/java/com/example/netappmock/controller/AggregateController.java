package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/storage/aggregates")
class AggregateController {

    @GetMapping
    public ResponseEntity<?> getAggregates() {
        Map<String, Object> response = Map.of("records", List.of(
                Map.of(
                        "uuid", "agg-uuid-001",
                        "name", "aggr1_node1",
                        "node", Map.of("name", "node-01", "uuid", "node-uuid-001"),
                        "block_storage", Map.of("primary", Map.of("size", 1099511627776L, "used", 439804651110L)),
                        "type", "hybrid",
                        "state", "online",
                        "comment", "Root aggregate for node-01"
                ),
                Map.of(
                        "uuid", "agg-uuid-002",
                        "name", "aggr2_node2",
                        "node", Map.of("name", "node-02"),
                        "type", "ssd",
                        "state", "online"
                )
        ));
        return ResponseEntity.ok(response);
    }
}