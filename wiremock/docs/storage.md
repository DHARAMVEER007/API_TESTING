# Storage Management APIs

## Overview

The Storage Management APIs provide comprehensive control over NetApp ONTAP storage resources including aggregates, volumes, disks, controllers, and qtrees.

## Base Paths
- `/api/storage/aggregates` - Storage aggregates
- `/api/storage/volumes` - Volumes and efficiency
- `/api/storage/disks` - Disk management and metrics
- `/api/storage/controllers` - Storage controllers
- `/api/storage/qtrees` - Qtree management

---

## Endpoints

### 📦 GET /storage/aggregates

**Purpose:** Get storage aggregates information

**Description:** 
Retrieves information about storage aggregates, which are collections of disks that provide the underlying storage for volumes.

#### Request

**Method:** `GET`  
**URL:** `/api/storage/aggregates`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "agg-uuid-001",
      "name": "aggr1_node1",
      "node": {
        "name": "node-01",
        "uuid": "node-uuid-001"
      },
      "block_storage": {
        "primary": {
          "size": 1099511627776,
          "used": 439804651110
        }
      },
      "type": "hybrid",
      "state": "online",
      "comment": "Root aggregate for node-01"
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Aggregate unique identifier |
| name | string | Aggregate name |
| node.name | string | Owning node name |
| node.uuid | string | Owning node UUID |
| block_storage.primary.size | integer | Total size in bytes |
| block_storage.primary.used | integer | Used space in bytes |
| type | string | Aggregate type (hybrid, ssd, hdd) |
| state | string | Aggregate state |
| comment | string | Administrative comment |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/storage/aggregates \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 💽 GET /storage/volumes

**Purpose:** Get volume information

**Description:** 
Retrieves information about FlexVol volumes including size, state, SVM assignment, and snapshot policies.

#### Request

**Method:** `GET`  
**URL:** `/api/storage/volumes`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "vol-uuid-001",
      "name": "vol_data_01",
      "svm": {
        "name": "svm1"
      },
      "aggregate": {
        "name": "aggr1_node1"
      },
      "type": "rw",
      "style": "flexvol",
      "state": "online",
      "junction_path": "/vol_data_01",
      "size": 536870912000,
      "space_guarantee": "volume",
      "snapshot_policy": {
        "name": "default"
      }
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Volume unique identifier |
| name | string | Volume name |
| svm.name | string | Storage Virtual Machine name |
| aggregate.name | string | Containing aggregate name |
| type | string | Volume type (rw, dp, ls) |
| style | string | Volume style (flexvol, flexgroup) |
| state | string | Volume state |
| junction_path | string | NAS junction path |
| size | integer | Volume size in bytes |
| space_guarantee | string | Space guarantee type |
| snapshot_policy.name | string | Snapshot policy name |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/storage/volumes \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 📈 GET /storage/volumes/efficiency

**Purpose:** Get storage efficiency information

**Description:** 
Retrieves storage efficiency statistics including compression and deduplication savings for volumes.

#### Request

**Method:** `GET`  
**URL:** `/api/storage/volumes/efficiency`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "volume_name": "vol_data_01",
      "volume_uuid": "vol-uuid-001",
      "compression_saved": 107374182400,
      "deduplication_saved": 214748364800,
      "total_space": 536870912000,
      "compression_ratio": 0.8,
      "deduplication_ratio": 0.6,
      "efficiency_status": "enabled",
      "last_scan_time": "2024-01-15T10:30:00Z",
      "scan_progress": 100
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| volume_name | string | Volume name |
| volume_uuid | string | Volume UUID |
| compression_saved | integer | Space saved by compression (bytes) |
| deduplication_saved | integer | Space saved by deduplication (bytes) |
| total_space | integer | Total volume space (bytes) |
| compression_ratio | number | Compression ratio (0-1) |
| deduplication_ratio | number | Deduplication ratio (0-1) |
| efficiency_status | string | Efficiency feature status |
| last_scan_time | string | Last efficiency scan timestamp |
| scan_progress | integer | Scan progress percentage |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/storage/volumes/efficiency \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 💿 GET /storage/disks

**Purpose:** Get disk information

**Description:** 
Retrieves information about physical disks in the storage system including type, size, location, and health status.

#### Request

**Method:** `GET`  
**URL:** `/api/storage/disks`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "disk-uuid-001",
      "name": "0a.00.0",
      "serial_number": "X477_12345678",
      "type": "SSD",
      "model": "X477_S1648A9",
      "vendor": "NetApp",
      "size": 1649267441664,
      "rpm": 10000,
      "state": "present",
      "location": {
        "shelf": 1,
        "bay": 0
      },
      "node": {
        "name": "node-01"
      }
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Disk unique identifier |
| name | string | Disk name |
| serial_number | string | Hardware serial number |
| type | string | Disk type (SSD, HDD, NVME) |
| model | string | Disk model number |
| vendor | string | Disk vendor |
| size | integer | Disk capacity in bytes |
| rpm | integer | Rotational speed (RPM) |
| state | string | Disk state |
| location.shelf | integer | Disk shelf number |
| location.bay | integer | Disk bay number |
| node.name | string | Owning node name |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/storage/disks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 📊 GET /storage/disks/{diskUuid}/metrics

**Purpose:** Get disk performance metrics

**Description:** 
Retrieves real-time performance metrics for a specific disk including IOPS, latency, utilization, and error counts.

#### Request

**Method:** `GET`  
**URL:** `/api/storage/disks/{diskUuid}/metrics`  
**Authentication:** Required

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| diskUuid | string | Yes | Disk UUID from disks endpoint |

#### Response

**Success Response (200 OK):**
```json
{
  "metrics": {
    "utilization_percent": 74.3,
    "iops": {
      "read": 120,
      "write": 95
    },
    "latency": {
      "read": 0.7,
      "write": 1.0
    },
    "temperature_celsius": 38,
    "errors": {
      "media": 0,
      "other": 1
    },
    "timestamp": "2025-07-16T14:00:00Z"
  }
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| utilization_percent | number | Disk utilization percentage |
| iops.read | integer | Read IOPS |
| iops.write | integer | Write IOPS |
| latency.read | number | Read latency in milliseconds |
| latency.write | number | Write latency in milliseconds |
| temperature_celsius | integer | Disk temperature |
| errors.media | integer | Media error count |
| errors.other | integer | Other error count |
| timestamp | string | Metrics timestamp |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/storage/disks/disk-uuid-001/metrics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🖥️ GET /storage/controllers

**Purpose:** Get storage controller information

**Description:** 
Retrieves information about storage controllers (nodes) including hardware specifications, HA configuration, and operational status.

#### Request

**Method:** `GET`  
**URL:** `/api/storage/controllers`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "ctrl-uuid-001",
      "name": "node-01",
      "model": "FAS2750",
      "vendor": "NetApp",
      "serial_number": "SN1234567890",
      "os_version": "NetApp Release 9.12.1P5",
      "location": "Rack 3, DC1",
      "ha": {
        "partner": "node-02",
        "state": "connected"
      },
      "cpu": {
        "cores": 12,
        "model": "Intel Xeon E5-2630"
      },
      "memory": {
        "size": "128GB"
      },
      "state": "online"
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Controller unique identifier |
| name | string | Controller/node name |
| model | string | Hardware model |
| vendor | string | Hardware vendor |
| serial_number | string | Hardware serial number |
| os_version | string | ONTAP version |
| location | string | Physical location |
| ha.partner | string | HA partner name |
| ha.state | string | HA relationship state |
| cpu.cores | integer | CPU core count |
| cpu.model | string | CPU model |
| memory.size | string | Memory size |
| state | string | Controller state |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/storage/controllers \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🌳 GET /storage/qtrees

**Purpose:** Get qtree information

**Description:** 
Retrieves information about qtrees, which are logical subdivisions within volumes that provide additional administrative control.

#### Request

**Method:** `GET`  
**URL:** `/api/storage/qtrees`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "qtree-uuid-001",
      "name": "qtree_docs",
      "volume": {
        "name": "vol_data_01",
        "uuid": "vol-uuid-001"
      },
      "path": "/vol_data_01/qtree_docs",
      "svm": {
        "name": "svm1"
      },
      "security_style": "unix",
      "export_policy": {
        "name": "default"
      },
      "oplocks": "enabled",
      "status": "online"
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Qtree unique identifier |
| name | string | Qtree name |
| volume.name | string | Parent volume name |
| volume.uuid | string | Parent volume UUID |
| path | string | Full qtree path |
| svm.name | string | Storage Virtual Machine name |
| security_style | string | Security style (unix, ntfs, mixed) |
| export_policy.name | string | NFS export policy name |
| oplocks | string | Opportunistic locks setting |
| status | string | Qtree status |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/storage/qtrees \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Common Use Cases

### 1. Storage Capacity Planning
```bash
# Check aggregate utilization
curl -X GET http://localhost:8080/api/storage/aggregates -H "Authorization: Bearer YOUR_TOKEN"

# Review volume sizes
curl -X GET http://localhost:8080/api/storage/volumes -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. Performance Monitoring
```bash
# Get disk metrics
curl -X GET http://localhost:8080/api/storage/disks/disk-uuid-001/metrics -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Efficiency Analysis
```bash
# Check storage efficiency savings
curl -X GET http://localhost:8080/api/storage/volumes/efficiency -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Hardware Inventory
```bash
# List storage controllers
curl -X GET http://localhost:8080/api/storage/controllers -H "Authorization: Bearer YOUR_TOKEN"

# List all disks
curl -X GET http://localhost:8080/api/storage/disks -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Storage Architecture

### Hierarchy
1. **Controllers** - Physical storage nodes
2. **Aggregates** - Collections of disks
3. **Volumes** - Logical storage containers
4. **Qtrees** - Subdivisions within volumes

### Types and States

#### Aggregate Types
- **hybrid** - Mix of SSD and HDD
- **ssd** - All SSD storage
- **hdd** - All HDD storage

#### Volume Types
- **rw** - Read-write volume
- **dp** - Data protection volume
- **ls** - Load-sharing volume

#### Disk Types
- **SSD** - Solid State Drive
- **HDD** - Hard Disk Drive
- **NVME** - NVMe SSD

#### Security Styles
- **unix** - UNIX-style permissions
- **ntfs** - Windows NTFS permissions
- **mixed** - Both UNIX and NTFS

---

## Related APIs

- [Cluster APIs](./cluster.md) - Cluster and node information
- [SVM APIs](./svm.md) - Storage Virtual Machine management
- [Protocol APIs](./protocols.md) - Protocol configuration for storage access
