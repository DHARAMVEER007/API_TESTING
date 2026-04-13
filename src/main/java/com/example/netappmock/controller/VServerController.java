package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

import static java.util.Map.entry;

@RestController
@RequestMapping("/api/svm/svms")
public class VServerController {

    @GetMapping
    public ResponseEntity<Map<String, Object>> getVServers() {
        Map<String, Object> vserver1 = Map.ofEntries(
                entry("uuid", "svm-uuid-001"),
                entry("name", "svm1"),
                entry("state", "running"),
                entry("subtype", "default"),
                entry("language", "c.utf_8"),
                entry("max_volumes", 1000),
                entry("allowed_protocols", List.of("nfs", "cifs", "iscsi", "fc"))
        );

        Map<String, Object> vserver2 = Map.ofEntries(
                entry("uuid", "svm-uuid-002"),
                entry("name", "svm2"),
                entry("state", "running"),
                entry("subtype", "default"),
                entry("language", "c.utf_8"),
                entry("max_volumes", 500),
                entry("allowed_protocols", List.of("nfs", "cifs"))
        );

        Map<String, Object> vserver3 = Map.ofEntries(
                entry("uuid", "svm-uuid-003"),
                entry("name", "svm_backup"),
                entry("state", "stopped"),
                entry("subtype", "dp_destination"),
                entry("language", "c.utf_8"),
                entry("max_volumes", 200),
                entry("allowed_protocols", List.of("nfs"))
        );

        Map<String, Object> response = Map.of("records", List.of(vserver1, vserver2, vserver3));
        return ResponseEntity.ok(response);
    }
}