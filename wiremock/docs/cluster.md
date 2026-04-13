# Cluster Management APIs

## Overview

The Cluster Management APIs provide information about the NetApp ONTAP cluster, including cluster details, version information, licensing, and node management.

## Base Paths
- `/api/cluster` - Cluster information
- `/api/cluster/nodes` - Node management

---

## Endpoints

### 🏢 GET /cluster

**Purpose:** Get cluster information and configuration

**Description:** 
Retrieves comprehensive information about the ONTAP cluster including name, UUID, contact information, nodes, and management interfaces.

#### Request

**Method:** `GET`  
**URL:** `/api/cluster`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "name": "cluster-01",
  "uuid": "3a1f9f10-1234-11eb-9a70-005056bb6e4b",
  "contact": "admin@example.com",
  "location": "Data Center A",
  "nodes": [
    {
      "name": "node1",
      "uuid": "d4e3a710-1234-11eb-9a70-005056bb6e4b"
    },
    {
      "name": "node2", 
      "uuid": "d4e3a711-1234-11eb-9a70-005056bb6e4b"
    }
  ],
  "management_interfaces": [
    {
      "ip": "10.0.0.100",
      "port": 443
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| name | string | Cluster name |
| uuid | string | Unique cluster identifier |
| contact | string | Administrator contact information |
| location | string | Physical location of cluster |
| nodes | array | Array of cluster nodes |
| nodes[].name | string | Node name |
| nodes[].uuid | string | Node UUID |
| management_interfaces | array | Cluster management interfaces |
| management_interfaces[].ip | string | Management IP address |
| management_interfaces[].port | integer | Management port number |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/cluster \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 📊 GET /cluster/version

**Purpose:** Get cluster software version information

**Description:** 
Retrieves detailed version information about the ONTAP software running on the cluster.

#### Request

**Method:** `GET`  
**URL:** `/api/cluster/version`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "version": {
    "full": "NetApp Release 9.12.1P5",
    "generation": "9",
    "major": "12", 
    "minor": "1",
    "build": "P5"
  },
  "build_date": "2024-01-15T12:34:56Z"
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| version.full | string | Full version string |
| version.generation | string | ONTAP generation number |
| version.major | string | Major version number |
| version.minor | string | Minor version number |
| version.build | string | Build/patch identifier |
| build_date | string | ISO 8601 timestamp of build |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/cluster/version \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 📜 GET /cluster/licensing/licenses

**Purpose:** Get cluster licensing information

**Description:** 
Retrieves information about all licenses installed on the cluster, including license status, expiration dates, and available features.

#### Request

**Method:** `GET`  
**URL:** `/api/cluster/licensing/licenses`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "licenses": [
    {
      "package": "Base",
      "serial_number": "1-80-000011",
      "installed": true,
      "scope": "cluster",
      "expiration_date": null,
      "features": ["NFS", "CIFS", "iSCSI"],
      "firmware_version": "9.12.1P5"
    },
    {
      "package": "SnapMirror",
      "serial_number": "1-80-000012", 
      "installed": true,
      "scope": "cluster",
      "expiration_date": "2026-01-01"
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| package | string | License package name |
| serial_number | string | License serial number |
| installed | boolean | Whether license is installed |
| scope | string | License scope (cluster/node) |
| expiration_date | string/null | License expiration date (YYYY-MM-DD) |
| features | array | Array of enabled features |
| firmware_version | string | Compatible firmware version |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/cluster/licensing/licenses \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🖥️ GET /cluster/nodes

**Purpose:** Get cluster node information

**Description:** 
Retrieves information about all nodes in the cluster, including health status, hardware details, and high-availability configuration.

#### Request

**Method:** `GET`  
**URL:** `/api/cluster/nodes`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
      "name": "node-01",
      "state": "healthy",
      "model": "FAS2750",
      "serial_number": "123456789",
      "ha": {
        "partner": "node-02",
        "state": "connected"
      },
      "version": {
        "full": "NetApp Release 9.12.1P5"
      }
    },
    {
      "uuid": "b2c3d4e5-6789-01ab-cdef-2345678901bc",
      "name": "node-02", 
      "state": "healthy",
      "model": "FAS2750",
      "serial_number": "987654321"
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Node unique identifier |
| name | string | Node name |
| state | string | Node health state |
| model | string | Hardware model |
| serial_number | string | Hardware serial number |
| ha.partner | string | HA partner node name |
| ha.state | string | HA relationship state |
| version.full | string | ONTAP version on node |

#### Node States

| State | Description |
|-------|-------------|
| healthy | Node is operating normally |
| degraded | Node has issues but is operational |
| failed | Node has failed |
| unknown | Node state cannot be determined |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/cluster/nodes \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Common Use Cases

### 1. Cluster Health Check
```bash
# Get cluster overview
curl -X GET http://localhost:8080/api/cluster -H "Authorization: Bearer YOUR_TOKEN"

# Check node health
curl -X GET http://localhost:8080/api/cluster/nodes -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. Version Verification
```bash
# Check ONTAP version
curl -X GET http://localhost:8080/api/cluster/version -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. License Audit
```bash
# Review all licenses
curl -X GET http://localhost:8080/api/cluster/licensing/licenses -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Mock Data Details

### Cluster Configuration
- **Name:** cluster-01
- **Location:** Data Center A
- **Nodes:** 2 (node1, node2)
- **Management IP:** 10.0.0.100:443

### Software Version
- **Version:** NetApp Release 9.12.1P5
- **Build Date:** 2024-01-15T12:34:56Z

### License Packages
- **Base License:** Includes NFS, CIFS, iSCSI
- **SnapMirror License:** Expires 2026-01-01

### Node Information
- **Model:** FAS2750
- **HA Configuration:** 2-node cluster with HA enabled
- **State:** All nodes healthy

---

## Related APIs

- [Storage APIs](./storage.md) - Manage storage resources on cluster nodes
- [Network APIs](./network.md) - Configure network interfaces on nodes
- [SVM APIs](./svm.md) - Manage Storage Virtual Machines
