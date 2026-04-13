package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api/network/fc/ports")
public class FCPortController {

    @GetMapping
    public ResponseEntity<Map<String, Object>> getFCPorts() {
        List<Map<String, Object>> records = new ArrayList<>();

        // Port 1 (online, with node and fabric info)
        Map<String, Object> port1 = new HashMap<>();
        port1.put("uuid", "port-uuid-001");
        port1.put("name", "0a");
        port1.put("wwpn", "50:0a:09:84:00:1a:01:02");

        Map<String, Object> node = new HashMap<>();
        node.put("name", "node-01");
        node.put("uuid", "node-uuid-001");
        port1.put("node", node);

        port1.put("port_type", "target");
        port1.put("state", "online");
        port1.put("speed", "16Gb");
        port1.put("enabled", true);

        Map<String, Object> fabric = new HashMap<>();
        fabric.put("name", "fabric-A");
        port1.put("fabric", fabric);

        records.add(port1);

        // Port 2 (offline, minimal info)
        Map<String, Object> port2 = new HashMap<>();
        port2.put("uuid", "port-uuid-002");
        port2.put("name", "0b");
        port2.put("wwpn", "50:0a:09:84:00:1a:01:03");
        port2.put("state", "offline");
        port2.put("speed", "8Gb");

        records.add(port2);

        Map<String, Object> response = new HashMap<>();
        response.put("records", records);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/{portUuid}/metrics")
    public ResponseEntity<Map<String, Object>> getPortMetrics(@PathVariable("portUuid") String portUuid) {
        Map<String, Object> throughput = new HashMap<>();
        throughput.put("received", 300000000);
        throughput.put("sent", 280000000);

        Map<String, Object> errors = new HashMap<>();
        errors.put("rx", 0);
        errors.put("tx", 2);

        Map<String, Object> metrics = new HashMap<>();
        metrics.put("throughput", throughput);
        metrics.put("errors", errors);
        metrics.put("utilization_percent", 65.0);
        metrics.put("timestamp", "2025-07-16T13:00:00Z");

        Map<String, Object> response = new HashMap<>();
        response.put("metrics", metrics);

        return ResponseEntity.ok(response);
    }
}
