package com.example.netappmock.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

import static java.util.Map.entry;

@RestController
@RequestMapping("/api/network")
public class NetworkController {

    @GetMapping("/ethernet/interfaces")
    public ResponseEntity<Map<String, Object>> getEthernetInterfaces() {
        Map<String, Object> interface1 = Map.ofEntries(
                entry("name", "e0a"),
                entry("node", Map.of("name", "node-01", "uuid", "abcd-1234-efgh-5678")),
                entry("mac", "00:a0:98:12:34:56"),
                entry("speed", "10Gb"),
                entry("status", "up"),
                entry("type", "physical"),
                entry("enabled", true)
        );

        Map<String, Object> interface2 = Map.ofEntries(
                entry("name", "e0b"),
                entry("node", Map.of("name", "node-02")),
                entry("mac", "00:a0:98:12:34:57"),
                entry("speed", "1Gb"),
                entry("status", "down"),
                entry("type", "physical"),
                entry("enabled", false)
        );

        Map<String, Object> response = Map.of("records", List.of(interface1, interface2));
        return ResponseEntity.ok(response);
    }

    @GetMapping("/ip/interfaces")
    public ResponseEntity<Map<String, Object>> getIpInterfaces() {
        Map<String, Object> lif1 = Map.ofEntries(
                entry("ip", Map.of(
                        "address", "192.168.1.100",
                        "netmask", "255.255.255.0"
                )),
                entry("location", Map.of(
                        "port", Map.of("name", "e0a")
                ))
        );

        Map<String, Object> lif2 = Map.ofEntries(
                entry("ip", Map.of(
                        "address", "192.168.1.101",
                        "netmask", "255.255.255.0"
                )),
                entry("location", Map.of(
                        "port", Map.of("name", "e0b")
                ))
        );

        Map<String, Object> response = Map.of("records", List.of(lif1, lif2));
        return ResponseEntity.ok(response);
    }
}
