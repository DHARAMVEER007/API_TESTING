package com.example.netappmock.controller;


import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api/protocols/san/iscsi")
public class ISCSIExportController {

    @GetMapping("/luns")
    public ResponseEntity<Map<String, Object>> getLUNs() {
        Map<String, Object> lun = new HashMap<>();
        lun.put("uuid", "lun-uuid-001");
        lun.put("name", "/vol1/lun1");

        Map<String, Object> svm = new HashMap<>();
        svm.put("name", "svm1");
        lun.put("svm", svm);

        Map<String, Object> volume = new HashMap<>();
        volume.put("name", "vol_data_01");
        lun.put("volume", volume);

        lun.put("size", 214748364800L);
        lun.put("enabled", true);
        lun.put("mapped", true);
        lun.put("os_type", "windows");
        lun.put("space_reserved", false);

        List<Map<String, Object>> records = new ArrayList<>();
        records.add(lun);

        Map<String, Object> response = new HashMap<>();
        response.put("records", records);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/initiators")
    public ResponseEntity<Map<String, Object>> getInitiators() {
        Map<String, Object> initiator = new HashMap<>();
        initiator.put("name", "iqn.1991-05.com.microsoft:client1");

        Map<String, Object> igroup = new HashMap<>();
        igroup.put("name", "windows_servers");
        initiator.put("igroup", igroup);

        Map<String, Object> svm = new HashMap<>();
        svm.put("name", "svm1");
        initiator.put("svm", svm);

        initiator.put("alias", "WinClient01");
        initiator.put("os_type", "windows");

        List<Map<String, Object>> records = new ArrayList<>();
        records.add(initiator);

        Map<String, Object> response = new HashMap<>();
        response.put("records", records);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/targets")
    public ResponseEntity<Map<String, Object>> getTargets() {
        Map<String, Object> target = new HashMap<>();
        target.put("name", "iqn.1992-08.com.netapp:sn.123456789.lun1");

        Map<String, Object> address = new HashMap<>();
        address.put("ip", "10.10.10.100");
        address.put("port", 3260);
        target.put("address", address);

        Map<String, Object> svm = new HashMap<>();
        svm.put("name", "svm1");
        target.put("svm", svm);

        target.put("enabled", true);

        Map<String, Object> lif = new HashMap<>();
        lif.put("name", "lif_iscsi_1");
        target.put("lif", lif);

        List<Map<String, Object>> records = new ArrayList<>();
        records.add(target);

        Map<String, Object> response = new HashMap<>();
        response.put("records", records);

        return ResponseEntity.ok(response);
    }
}
