# Network APIs

## Overview

The Network APIs provide management and monitoring capabilities for NetApp ONTAP network interfaces, including Ethernet interfaces, IP logical interfaces (LIFs), and Fibre Channel ports.

## Base Paths
- `/api/network/ethernet/interfaces` - Physical ethernet interfaces
- `/api/network/ip/interfaces` - IP logical interfaces
- `/api/network/fc/ports` - Fibre Channel ports

---

## Endpoints

### 🌐 GET /network/ethernet/interfaces

**Purpose:** Get ethernet interface information

**Description:** 
Retrieves information about physical ethernet interfaces on cluster nodes, including MAC addresses, speed, and operational status.

#### Request

**Method:** `GET`  
**URL:** `/api/network/ethernet/interfaces`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "name": "e0a",
      "node": {
        "name": "node-01",
        "uuid": "abcd-1234-efgh-5678"
      },
      "mac": "00:a0:98:12:34:56",
      "speed": "10Gb",
      "status": "up",
      "type": "physical",
      "enabled": true
    },
    {
      "name": "e0b",
      "node": {
        "name": "node-02"
      },
      "mac": "00:a0:98:12:34:57",
      "speed": "1Gb",
      "status": "down",
      "type": "physical",
      "enabled": false
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| name | string | Interface name |
| node.name | string | Node hosting the interface |
| node.uuid | string | Node UUID |
| mac | string | MAC address |
| speed | string | Interface speed |
| status | string | Operational status (up, down) |
| type | string | Interface type (physical, virtual) |
| enabled | boolean | Administrative state |

#### Interface Speeds
- **10Gb** - 10 Gigabit Ethernet
- **1Gb** - 1 Gigabit Ethernet
- **100Mb** - 100 Megabit Ethernet
- **10Mb** - 10 Megabit Ethernet

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/network/ethernet/interfaces \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🔌 GET /network/ip/interfaces

**Purpose:** Get IP logical interfaces (LIFs)

**Description:** 
Retrieves information about IP logical interfaces, which provide network access to SVMs and their data services.

#### Request

**Method:** `GET`  
**URL:** `/api/network/ip/interfaces`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "ip": {
        "address": "192.168.1.100",
        "netmask": "255.255.255.0"
      },
      "location": {
        "port": {
          "name": "e0a"
        }
      }
    },
    {
      "ip": {
        "address": "192.168.1.101", 
        "netmask": "255.255.255.0"
      },
      "location": {
        "port": {
          "name": "e0b"
        }
      }
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| ip.address | string | IP address |
| ip.netmask | string | Subnet mask |
| location.port.name | string | Physical port hosting the LIF |

#### Common IP Configurations

| Network Type | Typical Use | Example |
|--------------|-------------|---------|
| Management | Cluster/Node management | 192.168.1.100/24 |
| Data | Client data access | 10.1.1.100/24 |
| Intercluster | Cluster replication | 172.16.1.100/24 |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/network/ip/interfaces \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🔗 GET /network/fc/ports

**Purpose:** Get Fibre Channel port information

**Description:** 
Retrieves information about Fibre Channel ports, including World Wide Port Names (WWPN), state, speed, and fabric connectivity.

#### Request

**Method:** `GET`  
**URL:** `/api/network/fc/ports`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "port-uuid-001",
      "name": "0a",
      "wwpn": "50:0a:09:84:00:1a:01:02",
      "node": {
        "name": "node-01",
        "uuid": "node-uuid-001"
      },
      "port_type": "target",
      "state": "online",
      "speed": "16Gb",
      "enabled": true,
      "fabric": {
        "name": "fabric-A"
      }
    },
    {
      "uuid": "port-uuid-002",
      "name": "0b",
      "wwpn": "50:0a:09:84:00:1a:01:03",
      "state": "offline",
      "speed": "8Gb"
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Port unique identifier |
| name | string | Port name |
| wwpn | string | World Wide Port Name |
| node.name | string | Node hosting the port |
| node.uuid | string | Node UUID |
| port_type | string | Port type (target, initiator) |
| state | string | Port state (online, offline) |
| speed | string | Port speed |
| enabled | boolean | Administrative state |
| fabric.name | string | Connected fabric name |

#### FC Port Speeds
- **32Gb** - 32 Gigabit FC
- **16Gb** - 16 Gigabit FC
- **8Gb** - 8 Gigabit FC
- **4Gb** - 4 Gigabit FC

#### Port States
- **online** - Port is operational and connected
- **offline** - Port is not operational
- **standby** - Port is in standby mode
- **error** - Port has errors

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/network/fc/ports \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 📊 GET /network/fc/ports/{portUuid}/metrics

**Purpose:** Get Fibre Channel port performance metrics

**Description:** 
Retrieves real-time performance metrics for a specific FC port including throughput, errors, and utilization.

#### Request

**Method:** `GET`  
**URL:** `/api/network/fc/ports/{portUuid}/metrics`  
**Authentication:** Required

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| portUuid | string | Yes | FC port UUID from ports endpoint |

#### Response

**Success Response (200 OK):**
```json
{
  "metrics": {
    "throughput": {
      "received": 300000000,
      "sent": 280000000
    },
    "errors": {
      "rx": 0,
      "tx": 2
    },
    "utilization_percent": 65.0,
    "timestamp": "2025-07-16T13:00:00Z"
  }
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| throughput.received | integer | Received bytes per second |
| throughput.sent | integer | Sent bytes per second |
| errors.rx | integer | Receive error count |
| errors.tx | integer | Transmit error count |
| utilization_percent | number | Port utilization percentage |
| timestamp | string | Metrics timestamp |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/network/fc/ports/port-uuid-001/metrics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Common Use Cases

### 1. Network Interface Inventory
```bash
# List all ethernet interfaces
curl -X GET http://localhost:8080/api/network/ethernet/interfaces \
  -H "Authorization: Bearer YOUR_TOKEN"

# List all IP interfaces
curl -X GET http://localhost:8080/api/network/ip/interfaces \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. Fibre Channel SAN Management
```bash
# List FC ports
curl -X GET http://localhost:8080/api/network/fc/ports \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check FC port performance
curl -X GET http://localhost:8080/api/network/fc/ports/port-uuid-001/metrics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Network Troubleshooting
```bash
# Check interface status
curl -X GET http://localhost:8080/api/network/ethernet/interfaces \
  -H "Authorization: Bearer YOUR_TOKEN" | grep -E "(name|status)"

# Verify FC connectivity
curl -X GET http://localhost:8080/api/network/fc/ports \
  -H "Authorization: Bearer YOUR_TOKEN" | grep -E "(name|state|fabric)"
```

---

## Network Architecture

### Interface Types

#### Physical Interfaces
- **Ethernet Ports** - e0a, e0b, e0c, etc.
- **FC Ports** - 0a, 0b, 0c, etc.
- **InfiniBand** - ib0a, ib0b (cluster interconnect)

#### Logical Interfaces (LIFs)
- **Data LIFs** - Serve data protocols (NFS, CIFS, iSCSI)
- **Management LIFs** - Cluster and SVM management
- **Intercluster LIFs** - Cluster peering and replication
- **Cluster LIFs** - Internal cluster communication

### Network Redundancy

#### High Availability
- **Link Aggregation** - Multiple physical links
- **Interface Groups** - Bonding for redundancy
- **VLAN Tagging** - Network segmentation

#### Multipathing
- **FC Multipathing** - Multiple paths to storage
- **Ethernet Multipathing** - Load balancing and failover

---

## Mock Data Details

### Ethernet Interfaces
- **e0a** - 10Gb interface on node-01 (up)
- **e0b** - 1Gb interface on node-02 (down)

### IP Interfaces
- **192.168.1.100/24** - Data LIF on e0a
- **192.168.1.101/24** - Data LIF on e0b

### FC Ports
- **Port 0a** - 16Gb FC port (online, fabric-A)
- **Port 0b** - 8Gb FC port (offline)

### Performance Metrics
- **Throughput** - ~300MB/s received, ~280MB/s sent
- **Utilization** - 65% average
- **Errors** - Minimal TX errors, no RX errors

---

## Related APIs

- [Cluster APIs](./cluster.md) - Node information for network interfaces
- [Protocol APIs](./protocols.md) - Protocol configuration using network interfaces
- [Storage APIs](./storage.md) - SAN storage accessible via FC networks
