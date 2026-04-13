package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

import static java.util.Map.entry;

@RestController
@RequestMapping("/api/protocols")
public class ProtocolController {

    @GetMapping("/cifs/shares")
    public ResponseEntity<Map<String, Object>> getCifsShares() {
        Map<String, Object> share1 = Map.ofEntries(
                entry("name", "share_docs"),
                entry("path", "/vol1/docs"),
                entry("junction_path", "/docs"),
                entry("volume", Map.of("name", "vol_data_01", "uuid", "vol-uuid-001")),
                entry("svm", Map.of("name", "svm1")),
                entry("comment", "Shared documents"),
                entry("offline_files_mode", "manual"),
                entry("symlink", false),
                entry("access_based_enumeration", true)
        );

        Map<String, Object> response = Map.of("records", List.of(share1));
        return ResponseEntity.ok(response);
    }
}
