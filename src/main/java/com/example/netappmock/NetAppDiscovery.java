package com.example.netappmock;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpRequest.BodyPublishers;
import java.time.Duration;
import java.util.*;
import com.fasterxml.jackson.databind.*;

public class NetAppDiscovery {

    private static boolean isBlank(String s) {
        return s == null || s.trim().isEmpty();
    }


    private static final String HOST = "localhost";
    private static final int PORT = 1715;
    private static final String USERNAME = "admin";
    private static final String PASSWORD = "netapp123";
    private static final int TIMEOUT = 30;
    private static final String BASE_URL = "http://" + HOST + ":" + PORT + "/api/";
    private static final ObjectMapper mapper = new ObjectMapper();

    private static final HttpClient client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(TIMEOUT))
            .build();

    private static String token;

    public static void main(String[] args) throws Exception {
        System.out.println("NetApp REST API: Starting CMDB discovery for " + HOST);

        token = authenticate();
        if (token == null) {
            System.err.println("Authentication failed.");
            return;
        }
        System.out.println("Authentication successful");

        Map<String, Object> result = new LinkedHashMap<>();

        Map<String, Object> clusterInfo = getClusterInfo();
        String clusterName = clusterInfo.get("description").toString().replace(" NetApp Cluster", "");
        String ipAddress = clusterInfo.get("ip_address").toString();

        result.put("NetApp Storage Server", clusterInfo);
        result.put("NetApp Node", getStorageNodeElement(clusterName, ipAddress));
        result.put("NetApp Cluster", getStorageClusterNodes(clusterName));
        result.put("NetApp Network Interface", getNetworkInterfaces());
        result.put("NetApp Aggregate", getStoragePools()); // corrected
        result.put("NetApp Volume", getStorageVolumes());
        result.put("NetApp LUN", getISCSIExports());
        result.put("NetApp FC LUN", getFCExports()); // optional
        result.put("NetApp Snapshot", getSnapshots()); // needs implementation
        result.put("NetApp VServer", getVServers());   // needs implementation
        result.put("NetApp Qtree", getQtrees());       // needs implementation
        result.put("NetApp Port",getFCPorts());
        result.put("NetApp Disk",getDisks());
        result.put("NetApp Fileshare",getFileShares());
        result.put("NetApp Storage Efficiency", getStorageEfficiency()); // needs implementation


        System.out.println("NetApp REST API: CMDB discovery completed successfully");
        System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(result));
    }

    private static String authenticate() throws Exception {
        String authUrl = BASE_URL + "security/authentication/cluster-tokens";
        Map<String, String> creds = Map.of("username", USERNAME, "password", PASSWORD);
        String json = mapper.writeValueAsString(creds);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(authUrl))
                .header("Content-Type", "application/json")
                .header("Accept", "application/json")
                .POST(BodyPublishers.ofString(json))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() >= 200 && response.statusCode() < 300) {
            return mapper.readTree(response.body()).get("token").asText();
        } else {
            System.err.println("Authentication failed: HTTP " + response.statusCode());
            System.err.println("Response: " + response.body());
            return null;
        }
    }

    private static JsonNode apiCall(String endpoint) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + endpoint))
                .header("Authorization", "Bearer " + token)
                .header("Accept", "application/json")
                .timeout(Duration.ofSeconds(TIMEOUT))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return mapper.readTree(response.body());
    }

    private static Map<String, Object> getClusterInfo() throws Exception {
        JsonNode cluster = apiCall("cluster");
        JsonNode version = apiCall("cluster/version");
        JsonNode license = apiCall("cluster/licensing/licenses");

        JsonNode mgmtInterfaces = cluster.path("management_interfaces");
        String ipAddress = mgmtInterfaces.isArray() && mgmtInterfaces.size() > 0
                ? mgmtInterfaces.get(0).path("ip").asText(null)
                : HOST;

        JsonNode licenses = license.path("licenses");
        String serialNumber = licenses.isArray() && licenses.size() > 0
                ? licenses.get(0).path("serial_number").asText(null)
                : null;
        String firmware = licenses.isArray() && licenses.size() > 0
                ? licenses.get(0).path("firmware_version").asText(null)
                : null;

        if (ipAddress == null || serialNumber == null || firmware == null) {
            throw new RuntimeException("Required cluster fields are missing.");
        }

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("ip_address", ipAddress);
        result.put("cluster_version", version.path("version").path("full").asText());
        result.put("serial_number", serialNumber);
        result.put("firmware_version", firmware);
        result.put("description", cluster.path("name").asText() + " NetApp Cluster");
        result.put("ip_address_range", ipAddress + "/24");
        return result;
    }




    private static List<Map<String, Object>> getStorageNodeElement(String clusterName, String ipAddress) {
        Map<String, Object> node = new LinkedHashMap<>();
        node.put("cluster", clusterName);
        node.put("ip_address_range", ipAddress + "/24");
        return List.of(node);
    }

    private static List<Map<String, Object>> getStorageClusterNodes(String clusterName) throws Exception {
        JsonNode nodes = apiCall("cluster/nodes");
        List<Map<String, Object>> result = new ArrayList<>();

        for (JsonNode node : nodes.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("name", node.path("name").asText());
            entry.put("operational_status", node.path("state").asText());
            entry.put("cluster", clusterName);
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getNetworkInterfaces() throws Exception {
        JsonNode lifs = apiCall("network/ip/interfaces");
        List<Map<String, Object>> result = new ArrayList<>();

        for (JsonNode lif : lifs.path("records")) {
            JsonNode ipNode = lif.path("ip");
            if (!ipNode.has("address")) continue;

            Map<String, Object> nic = new LinkedHashMap<>();
            nic.put("name", ipNode.path("address").asText());
            nic.put("netmask", ipNode.path("netmask").asText(""));
            nic.put("nic", lif.path("location").path("port").path("name").asText(""));
            result.add(nic);
        }
        return result;
    }

    private static List<Map<String, Object>> getDisks() throws Exception {
        JsonNode data = apiCall("storage/disks");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode disk : data.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("computer", disk.path("node").path("name").asText(""));
            entry.put("interface", disk.path("type").asText(""));
            entry.put("size_bytes", disk.path("size").asLong());
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getStoragePools() throws Exception {
        JsonNode data = apiCall("storage/aggregates");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode agg : data.path("records")) {
            if (!agg.has("block_storage")) continue;
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("name", agg.path("name").asText());
            entry.put("size_bytes", agg.path("block_storage").path("primary").path("size").asLong());
            entry.put("free_space_bytes", agg.path("block_storage").path("primary").path("available").asLong());
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getStorageVolumes() throws Exception {
        JsonNode data = apiCall("storage/volumes");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode vol : data.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("name", vol.path("name").asText());
            entry.put("volume_id", vol.path("uuid").asText());
            entry.put("size_bytes", vol.path("size").asLong());
            entry.put("free_space_bytes", vol.path("space").path("available").asLong());
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getFileShares() throws Exception {
        JsonNode cifs = apiCall("protocols/cifs/shares");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode share : cifs.path("records")) {
            result.add(Map.of("path", share.path("path").asText()));
        }
        return result;
    }

    private static List<Map<String, Object>> getISCSIExports() throws Exception {
        JsonNode data = apiCall("protocols/san/iscsi/luns");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode lun : data.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("name", lun.path("name").asText());
            entry.put("lun", lun.path("lun_id").asInt());
            entry.put("export_id", lun.path("uuid").asText());
            entry.put("initiator_iqn", lun.path("initiator_iqn").asText(""));
            entry.put("iqn", lun.path("target_iqn").asText(""));
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getFCExports() throws Exception {
        JsonNode data = apiCall("protocols/san/fc/luns");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode lun : data.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("name", lun.path("name").asText());
            entry.put("lun", lun.path("lun_id").asInt());
            entry.put("export_id", lun.path("uuid").asText());
            entry.put("initiator_wwpn", lun.path("initiator_wwpn").asText(""));
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getFCPorts() throws Exception {
        JsonNode data = apiCall("network/fc/ports");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode port : data.path("records")) {
            result.add(Map.of("speed", port.path("speed").asText()));
        }
        return result;
    }

    private static List<Map<String, Object>> getStorageControllers() throws Exception {
        JsonNode data = apiCall("storage/controllers");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode ctrl : data.path("records")) {
            result.add(Map.of(
                    "name", ctrl.path("name").asText(),
                    "device_id", ctrl.path("uuid").asText()
            ));
        }
        return result;
    }
    private static List<Map<String, Object>> getSnapshots() throws Exception {
        JsonNode data = apiCall("storage/volumes/*/snapshots");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode snapshot : data.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("name", snapshot.path("name").asText());
            entry.put("volume", snapshot.path("volume").path("name").asText());
            entry.put("created", snapshot.path("create_time").asText());
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getVServers() throws Exception {
        JsonNode data = apiCall("svm/svms");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode vserver : data.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("name", vserver.path("name").asText());
            entry.put("state", vserver.path("state").asText());
            entry.put("subtype", vserver.path("subtype").asText());
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getQtrees() throws Exception {
        JsonNode data = apiCall("storage/qtrees");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode qtree : data.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("name", qtree.path("name").asText());
            entry.put("volume", qtree.path("volume").path("name").asText());
            entry.put("path", qtree.path("path").asText());
            result.add(entry);
        }
        return result;
    }

    private static List<Map<String, Object>> getStorageEfficiency() throws Exception {
        JsonNode data = apiCall("storage/volumes/*/efficiency");
        List<Map<String, Object>> result = new ArrayList<>();
        for (JsonNode efficiency : data.path("records")) {
            Map<String, Object> entry = new LinkedHashMap<>();
            entry.put("volume", efficiency.path("volume").path("name").asText());
            entry.put("compression_saved", efficiency.path("compression_saved").asLong());
            entry.put("deduplication_saved", efficiency.path("deduplication_saved").asLong());
            result.add(entry);
        }
        return result;
    }
}
