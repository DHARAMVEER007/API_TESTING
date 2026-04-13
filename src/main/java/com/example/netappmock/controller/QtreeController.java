package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

import static java.util.Map.entry;

@RestController
@RequestMapping("/api/storage/qtrees")
public class QtreeController {

    @GetMapping
    public ResponseEntity<Map<String, Object>> getQtrees() {
        Map<String, Object> qtree1 = Map.ofEntries(
                entry("uuid", "qtree-uuid-001"),
                entry("name", "qtree_docs"),
                entry("volume", Map.of("name", "vol_data_01", "uuid", "vol-uuid-001")),
                entry("path", "/vol_data_01/qtree_docs"),
                entry("svm", Map.of("name", "svm1")),
                entry("security_style", "unix"),
                entry("export_policy", Map.of("name", "default")),
                entry("oplocks", "enabled"),
                entry("status", "online")
        );

        Map<String, Object> qtree2 = Map.ofEntries(
                entry("uuid", "qtree-uuid-002"),
                entry("name", "qtree_logs"),
                entry("volume", Map.of("name", "vol_logs_01", "uuid", "vol-uuid-002")),
                entry("path", "/vol_logs_01/qtree_logs"),
                entry("svm", Map.of("name", "svm1")),
                entry("security_style", "ntfs"),
                entry("export_policy", Map.of("name", "logs_policy")),
                entry("oplocks", "disabled"),
                entry("status", "online")
        );

        Map<String, Object> qtree3 = Map.ofEntries(
                entry("uuid", "qtree-uuid-003"),
                entry("name", "qtree_backup"),
                entry("volume", Map.of("name", "vol_backup_01", "uuid", "vol-uuid-003")),
                entry("path", "/vol_backup_01/qtree_backup"),
                entry("svm", Map.of("name", "svm2")),
                entry("security_style", "mixed"),
                entry("export_policy", Map.of("name", "backup_policy")),
                entry("oplocks", "enabled"),
                entry("status", "online")
        );

        Map<String, Object> response = Map.of("records", List.of(qtree1, qtree2, qtree3));
        return ResponseEntity.ok(response);
    }
}