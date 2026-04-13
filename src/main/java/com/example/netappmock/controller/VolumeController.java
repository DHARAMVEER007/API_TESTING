package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

import static java.util.Map.entry;

@RestController
@RequestMapping("/api/storage/volumes")
public class VolumeController {

    @GetMapping
    public ResponseEntity<Map<String, Object>> getVolumes() {
        Map<String, Object> volume1 = Map.ofEntries(
                entry("uuid", "vol-uuid-001"),
                entry("name", "vol_data_01"),
                entry("svm", Map.of("name", "svm1")),
                entry("aggregate", Map.of("name", "aggr1_node1")),
                entry("type", "rw"),
                entry("style", "flexvol"),
                entry("state", "online"),
                entry("junction_path", "/vol_data_01"),
                entry("size", 536870912000L),
                entry("space_guarantee", "volume"),
                entry("snapshot_policy", Map.of("name", "default"))
        );

        Map<String, Object> volume2 = Map.ofEntries(
                entry("uuid", "vol-uuid-002"),
                entry("name", "vol_logs_01"),
                entry("svm", Map.of("name", "svm2")),
                entry("aggregate", Map.of("name", "aggr2_node2")),
                entry("type", "rw"),
                entry("style", "flexvol"),
                entry("state", "online"),
                entry("junction_path", "/vol_logs_01"),
                entry("size", 214748364800L),
                entry("space_guarantee", "none"),
                entry("snapshot_policy", Map.of("name", "none"))
        );

        Map<String, Object> response = Map.of("records", List.of(volume1, volume2));
        return ResponseEntity.ok(response);
    }

    @GetMapping("/efficiency")
    public ResponseEntity<Map<String, Object>> getStorageEfficiency() {
        Map<String, Object> efficiency1 = Map.ofEntries(
                entry("volume_name", "vol_data_01"),
                entry("volume_uuid", "vol-uuid-001"),
                entry("compression_saved", 107374182400L), // 100 GB
                entry("deduplication_saved", 214748364800L), // 200 GB
                entry("total_space", 536870912000L), // 500 GB
                entry("compression_ratio", 0.8),
                entry("deduplication_ratio", 0.6),
                entry("efficiency_status", "enabled"),
                entry("last_scan_time", "2024-01-15T10:30:00Z"),
                entry("scan_progress", 100)
        );

        Map<String, Object> efficiency2 = Map.ofEntries(
                entry("volume_name", "vol_logs_01"),
                entry("volume_uuid", "vol-uuid-002"),
                entry("compression_saved", 53687091200L), // 50 GB
                entry("deduplication_saved", 107374182400L), // 100 GB
                entry("total_space", 214748364800L), // 200 GB
                entry("compression_ratio", 0.75),
                entry("deduplication_ratio", 0.5),
                entry("efficiency_status", "enabled"),
                entry("last_scan_time", "2024-01-15T11:45:00Z"),
                entry("scan_progress", 100)
        );
        Map<String, Object> response = Map.of("records", List.of(efficiency1, efficiency2));
        return ResponseEntity.ok(response);
    }
}
