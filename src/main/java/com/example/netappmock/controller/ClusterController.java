package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api/cluster")
public class ClusterController {

    @GetMapping
    public ResponseEntity<?> getCluster() {
        Map<String, Object> response = new LinkedHashMap<>();

        response.put("name", "cluster-01");
        response.put("uuid", "3a1f9f10-1234-11eb-9a70-005056bb6e4b");
        response.put("contact", "admin@example.com");
        response.put("location", "Data Center A");

        List<Map<String, Object>> nodes = new ArrayList<>();
        Map<String, Object> node1 = new HashMap<>();
        node1.put("name", "node1");
        node1.put("uuid", "d4e3a710-1234-11eb-9a70-005056bb6e4b");

        Map<String, Object> node2 = new HashMap<>();
        node2.put("name", "node2");
        node2.put("uuid", "d4e3a711-1234-11eb-9a70-005056bb6e4b");

        nodes.add(node1);
        nodes.add(node2);
        response.put("nodes", nodes);

        List<Map<String, Object>> interfaces = new ArrayList<>();
        Map<String, Object> iface = new HashMap<>();
        iface.put("ip", "10.0.0.100");
        iface.put("port", 443);
        interfaces.add(iface);

        response.put("management_interfaces", interfaces);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/version")
    public ResponseEntity<?> getClusterVersion() {
        Map<String, Object> version = new LinkedHashMap<>();
        version.put("full", "NetApp Release 9.12.1P5");
        version.put("generation", "9");
        version.put("major", "12");
        version.put("minor", "1");
        version.put("build", "P5");

        Map<String, Object> response = new LinkedHashMap<>();
        response.put("version", version);
        response.put("build_date", "2024-01-15T12:34:56Z");

        return ResponseEntity.ok(response);
    }

    @GetMapping("/licensing/licenses")
    public ResponseEntity<?> getLicenses() {
        List<Map<String, Object>> licenses = new ArrayList<>();

        Map<String, Object> baseLicense = new HashMap<>();
        baseLicense.put("package", "Base");
        baseLicense.put("serial_number", "1-80-000011");
        baseLicense.put("installed", true);
        baseLicense.put("scope", "cluster");
        baseLicense.put("expiration_date", null);
        baseLicense.put("features", List.of("NFS", "CIFS", "iSCSI"));
        baseLicense.put("firmware_version", "9.12.1P5");

        Map<String, Object> snapMirror = new HashMap<>();
        snapMirror.put("package", "SnapMirror");
        snapMirror.put("serial_number", "1-80-000012");
        snapMirror.put("installed", true);
        snapMirror.put("scope", "cluster");
        snapMirror.put("expiration_date", "2026-01-01");

        licenses.add(baseLicense);
        licenses.add(snapMirror);

        Map<String, Object> response = new LinkedHashMap<>();
        response.put("licenses", licenses);

        return ResponseEntity.ok(response);
    }
}
