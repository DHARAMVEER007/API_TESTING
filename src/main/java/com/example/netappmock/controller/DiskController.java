package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api/storage/disks")
public class DiskController {

    @GetMapping
    public ResponseEntity<Map<String, Object>> getDisks() {
        Map<String, Object> disk = new HashMap<>();
        disk.put("uuid", "disk-uuid-001");
        disk.put("name", "0a.00.0");
        disk.put("serial_number", "X477_12345678");
        disk.put("type", "SSD");
        disk.put("model", "X477_S1648A9");
        disk.put("vendor", "NetApp");
        disk.put("size", 1649267441664L); // 1.6 TB
        disk.put("rpm", 10000);
        disk.put("state", "present");

        Map<String, Object> location = new HashMap<>();
        location.put("shelf", 1);
        location.put("bay", 0);
        disk.put("location", location);

        Map<String, Object> node = new HashMap<>();
        node.put("name", "node-01");
        disk.put("node", node);

        List<Map<String, Object>> records = new ArrayList<>();
        records.add(disk);

        Map<String, Object> response = new HashMap<>();
        response.put("records", records);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/{diskUuid}/metrics")
    public ResponseEntity<Map<String, Object>> getDiskMetrics(@PathVariable("diskUuid") String diskUuid) {
        Map<String, Object> iops = new HashMap<>();
        iops.put("read", 120);
        iops.put("write", 95);

        Map<String, Object> latency = new HashMap<>();
        latency.put("read", 0.7);
        latency.put("write", 1.0);

        Map<String, Object> errors = new HashMap<>();
        errors.put("media", 0);
        errors.put("other", 1);

        Map<String, Object> metrics = new HashMap<>();
        metrics.put("utilization_percent", 74.3);
        metrics.put("iops", iops);
        metrics.put("latency", latency);
        metrics.put("temperature_celsius", 38);
        metrics.put("errors", errors);
        metrics.put("timestamp", "2025-07-16T14:00:00Z");

        Map<String, Object> response = new HashMap<>();
        response.put("metrics", metrics);

        return ResponseEntity.ok(response);
    }
}
