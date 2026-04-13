package com.example.netappmock.controller;



import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api/protocols/san/fc")
public class FCExportController {

    @GetMapping("/luns")
    public ResponseEntity<Map<String, Object>> getFCLUNs() {
        Map<String, Object> lun = new HashMap<>();
        lun.put("uuid", "lun-uuid-002");
        lun.put("name", "/vol2/lun2");

        Map<String, Object> svm = new HashMap<>();
        svm.put("name", "svm2");
        lun.put("svm", svm);

        Map<String, Object> volume = new HashMap<>();
        volume.put("name", "vol2");
        lun.put("volume", volume);

        lun.put("size", 429496729600L); // 400 GB
        lun.put("enabled", true);
        lun.put("mapped", true);
        lun.put("os_type", "linux");
        lun.put("space_reserved", true);

        List<Map<String, Object>> records = new ArrayList<>();
        records.add(lun);

        Map<String, Object> response = new HashMap<>();
        response.put("records", records);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/initiators")
    public ResponseEntity<Map<String, Object>> getFCInitiators() {
        Map<String, Object> initiator = new HashMap<>();
        initiator.put("name", "20:00:00:25:b5:00:00:01");

        Map<String, Object> igroup = new HashMap<>();
        igroup.put("name", "linux_servers");
        initiator.put("igroup", igroup);

        Map<String, Object> svm = new HashMap<>();
        svm.put("name", "svm2");
        initiator.put("svm", svm);

        initiator.put("alias", "LinuxHost01");
        initiator.put("os_type", "linux");

        List<Map<String, Object>> records = new ArrayList<>();
        records.add(initiator);

        Map<String, Object> response = new HashMap<>();
        response.put("records", records);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/targets")
    public ResponseEntity<Map<String, Object>> getFCTargets() {
        Map<String, Object> target = new HashMap<>();
        target.put("name", "50:0a:09:84:00:1a:01:02");

        Map<String, Object> svm = new HashMap<>();
        svm.put("name", "svm2");
        target.put("svm", svm);

        Map<String, Object> lif = new HashMap<>();
        lif.put("name", "fc_lif_1");
        target.put("lif", lif);

        target.put("enabled", true);

        Map<String, Object> node = new HashMap<>();
        node.put("name", "node-02");
        target.put("node", node);

        List<Map<String, Object>> records = new ArrayList<>();
        records.add(target);

        Map<String, Object> response = new HashMap<>();
        response.put("records", records);

        return ResponseEntity.ok(response);
    }
}
