# Protocol APIs

## Overview

The Protocol APIs provide management capabilities for data access protocols in NetApp ONTAP, including CIFS/SMB file shares, iSCSI block storage, and Fibre Channel SAN services.

## Base Paths
- `/api/protocols/cifs/shares` - CIFS/SMB file shares
- `/api/protocols/san/iscsi` - iSCSI block storage protocol
- `/api/protocols/san/fc` - Fibre Channel block storage protocol

---

## CIFS/SMB Protocol

### 📁 GET /protocols/cifs/shares

**Purpose:** Get CIFS/SMB share information

**Description:** 
Retrieves information about CIFS/SMB shares, which provide Windows-style file access to volumes and qtrees.

#### Request

**Method:** `GET`  
**URL:** `/api/protocols/cifs/shares`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "name": "share_docs",
      "path": "/vol1/docs",
      "junction_path": "/docs",
      "volume": {
        "name": "vol_data_01",
        "uuid": "vol-uuid-001"
      },
      "svm": {
        "name": "svm1"
      },
      "comment": "Shared documents",
      "offline_files_mode": "manual",
      "symlink": false,
      "access_based_enumeration": true
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| name | string | Share name |
| path | string | Volume path |
| junction_path | string | NAS junction path |
| volume.name | string | Source volume name |
| volume.uuid | string | Source volume UUID |
| svm.name | string | Storage Virtual Machine |
| comment | string | Administrative comment |
| offline_files_mode | string | Offline files behavior |
| symlink | boolean | Symbolic link support |
| access_based_enumeration | boolean | Hide inaccessible files |

#### Offline Files Modes
- **manual** - User controls offline files
- **automatic** - System controls offline files
- **disabled** - No offline file support

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/protocols/cifs/shares \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## iSCSI Protocol

### 💽 GET /protocols/san/iscsi/luns

**Purpose:** Get iSCSI LUN information

**Description:** 
Retrieves information about iSCSI LUNs (Logical Unit Numbers), which provide block storage access over IP networks.

#### Request

**Method:** `GET`  
**URL:** `/api/protocols/san/iscsi/luns`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "lun-uuid-001",
      "name": "/vol1/lun1",
      "svm": {
        "name": "svm1"
      },
      "volume": {
        "name": "vol_data_01"
      },
      "size": 214748364800,
      "enabled": true,
      "mapped": true,
      "os_type": "windows",
      "space_reserved": false
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | LUN unique identifier |
| name | string | LUN path and name |
| svm.name | string | Storage Virtual Machine |
| volume.name | string | Containing volume |
| size | integer | LUN size in bytes |
| enabled | boolean | LUN operational state |
| mapped | boolean | Whether LUN is mapped to initiators |
| os_type | string | Operating system type |
| space_reserved | boolean | Space reservation setting |

#### OS Types
- **windows** - Windows operating systems
- **linux** - Linux operating systems
- **vmware** - VMware ESX/vSphere
- **hyper_v** - Microsoft Hyper-V
- **aix** - IBM AIX

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/protocols/san/iscsi/luns \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🔌 GET /protocols/san/iscsi/initiators

**Purpose:** Get iSCSI initiator information

**Description:** 
Retrieves information about iSCSI initiators, which are client systems that connect to iSCSI targets to access LUNs.

#### Request

**Method:** `GET`  
**URL:** `/api/protocols/san/iscsi/initiators`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "name": "iqn.1991-05.com.microsoft:client1",
      "igroup": {
        "name": "windows_servers"
      },
      "svm": {
        "name": "svm1"
      },
      "alias": "WinClient01",
      "os_type": "windows"
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| name | string | iSCSI Qualified Name (IQN) |
| igroup.name | string | Initiator group membership |
| svm.name | string | Storage Virtual Machine |
| alias | string | Friendly name for initiator |
| os_type | string | Operating system type |

#### IQN Format
- **Format:** `iqn.yyyy-mm.domain:identifier`
- **Example:** `iqn.1991-05.com.microsoft:client1`

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/protocols/san/iscsi/initiators \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🎯 GET /protocols/san/iscsi/targets

**Purpose:** Get iSCSI target information

**Description:** 
Retrieves information about iSCSI targets, which are storage endpoints that serve LUNs to iSCSI initiators.

#### Request

**Method:** `GET`  
**URL:** `/api/protocols/san/iscsi/targets`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "name": "iqn.1992-08.com.netapp:sn.123456789.lun1",
      "address": {
        "ip": "10.10.10.100",
        "port": 3260
      },
      "svm": {
        "name": "svm1"
      },
      "enabled": true,
      "lif": {
        "name": "lif_iscsi_1"
      }
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| name | string | Target IQN |
| address.ip | string | Target IP address |
| address.port | integer | Target port (usually 3260) |
| svm.name | string | Storage Virtual Machine |
| enabled | boolean | Target operational state |
| lif.name | string | Logical interface name |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/protocols/san/iscsi/targets \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Fibre Channel Protocol

### 🔗 GET /protocols/san/fc/luns

**Purpose:** Get Fibre Channel LUN information

**Description:** 
Retrieves information about Fibre Channel LUNs, which provide high-performance block storage access over FC networks.

#### Request

**Method:** `GET`  
**URL:** `/api/protocols/san/fc/luns`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "lun-uuid-002",
      "name": "/vol2/lun2",
      "svm": {
        "name": "svm2"
      },
      "volume": {
        "name": "vol2"
      },
      "size": 429496729600,
      "enabled": true,
      "mapped": true,
      "os_type": "linux",
      "space_reserved": true
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | LUN unique identifier |
| name | string | LUN path and name |
| svm.name | string | Storage Virtual Machine |
| volume.name | string | Containing volume |
| size | integer | LUN size in bytes |
| enabled | boolean | LUN operational state |
| mapped | boolean | Whether LUN is mapped to initiators |
| os_type | string | Operating system type |
| space_reserved | boolean | Space reservation setting |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/protocols/san/fc/luns \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🖥️ GET /protocols/san/fc/initiators

**Purpose:** Get Fibre Channel initiator information

**Description:** 
Retrieves information about Fibre Channel initiators, which are client HBAs that connect to FC targets.

#### Request

**Method:** `GET`  
**URL:** `/api/protocols/san/fc/initiators`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "name": "20:00:00:25:b5:00:00:01",
      "igroup": {
        "name": "linux_servers"
      },
      "svm": {
        "name": "svm2"
      },
      "alias": "LinuxHost01",
      "os_type": "linux"
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| name | string | World Wide Port Name (WWPN) |
| igroup.name | string | Initiator group membership |
| svm.name | string | Storage Virtual Machine |
| alias | string | Friendly name for initiator |
| os_type | string | Operating system type |

#### WWPN Format
- **Format:** `xx:xx:xx:xx:xx:xx:xx:xx`
- **Example:** `20:00:00:25:b5:00:00:01`

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/protocols/san/fc/initiators \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🎯 GET /protocols/san/fc/targets

**Purpose:** Get Fibre Channel target information

**Description:** 
Retrieves information about Fibre Channel targets, which are storage endpoints that serve LUNs via FC fabric.

#### Request

**Method:** `GET`  
**URL:** `/api/protocols/san/fc/targets`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "name": "50:0a:09:84:00:1a:01:02",
      "svm": {
        "name": "svm2"
      },
      "lif": {
        "name": "fc_lif_1"
      },
      "enabled": true,
      "node": {
        "name": "node-02"
      }
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| name | string | Target WWPN |
| svm.name | string | Storage Virtual Machine |
| lif.name | string | FC logical interface name |
| enabled | boolean | Target operational state |
| node.name | string | Physical node hosting target |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/protocols/san/fc/targets \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Common Use Cases

### 1. File Share Management
```bash
# List CIFS shares
curl -X GET http://localhost:8080/api/protocols/cifs/shares \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. iSCSI SAN Configuration
```bash
# Check iSCSI LUNs
curl -X GET http://localhost:8080/api/protocols/san/iscsi/luns \
  -H "Authorization: Bearer YOUR_TOKEN"

# List iSCSI initiators
curl -X GET http://localhost:8080/api/protocols/san/iscsi/initiators \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check iSCSI targets
curl -X GET http://localhost:8080/api/protocols/san/iscsi/targets \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Fibre Channel SAN Management
```bash
# List FC LUNs
curl -X GET http://localhost:8080/api/protocols/san/fc/luns \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check FC initiators
curl -X GET http://localhost:8080/api/protocols/san/fc/initiators \
  -H "Authorization: Bearer YOUR_TOKEN"

# List FC targets
curl -X GET http://localhost:8080/api/protocols/san/fc/targets \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Protocol Comparison

### File Protocols vs Block Protocols

#### File Protocols (CIFS/SMB, NFS)
- **Access Type** - File-level access
- **Use Cases** - File shares, home directories
- **Clients** - Windows, Linux, macOS
- **Network** - Ethernet/IP

#### Block Protocols (iSCSI, FC)
- **Access Type** - Block-level access
- **Use Cases** - Databases, virtual machines
- **Clients** - Servers with block storage needs
- **Network** - Ethernet (iSCSI) or FC fabric

### iSCSI vs Fibre Channel

| Aspect | iSCSI | Fibre Channel |
|--------|-------|---------------|
| Network | Ethernet/IP | FC fabric |
| Cost | Lower | Higher |
| Distance | Longer (routed) | Limited (fabric) |
| Performance | Good | Excellent |
| Complexity | Lower | Higher |

---

## Mock Data Summary

### CIFS Shares
- **share_docs** - Document share on vol_data_01

### iSCSI Configuration
- **LUN** - 200GB Windows LUN
- **Initiator** - Microsoft client (WinClient01)
- **Target** - 10.10.10.100:3260

### FC Configuration
- **LUN** - 400GB Linux LUN  
- **Initiator** - Linux host HBA
- **Target** - 16Gb FC port

---

## Related APIs

- [Network APIs](./network.md) - FC ports and ethernet interfaces for protocols
- [Storage APIs](./storage.md) - Volumes and LUNs for protocol access
- [SVM APIs](./svm.md) - Storage Virtual Machines hosting protocols
