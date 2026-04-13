# SVM (Storage Virtual Machine) APIs

## Overview

The SVM APIs provide management capabilities for NetApp ONTAP Storage Virtual Machines (SVMs), also known as Vservers. SVMs are secure, isolated virtual machines that contain data volumes and serve data to clients through one or more network logical interfaces.

## Base Path
```
/api/svm/svms
```

---

## Endpoints

### 🏠 GET /svm/svms

**Purpose:** Get Storage Virtual Machine information

**Description:** 
Retrieves information about all SVMs in the cluster, including their configuration, state, supported protocols, and resource limits.

#### Request

**Method:** `GET`  
**URL:** `/api/svm/svms`  
**Authentication:** Required

#### Response

**Success Response (200 OK):**
```json
{
  "records": [
    {
      "uuid": "svm-uuid-001",
      "name": "svm1",
      "state": "running",
      "subtype": "default",
      "language": "c.utf_8",
      "max_volumes": 1000,
      "allowed_protocols": ["nfs", "cifs", "iscsi", "fc"]
    },
    {
      "uuid": "svm-uuid-002", 
      "name": "svm2",
      "state": "running",
      "subtype": "default",
      "language": "c.utf_8",
      "max_volumes": 500,
      "allowed_protocols": ["nfs", "cifs"]
    },
    {
      "uuid": "svm-uuid-003",
      "name": "svm_backup",
      "state": "stopped",
      "subtype": "dp_destination",
      "language": "c.utf_8",
      "max_volumes": 200,
      "allowed_protocols": ["nfs"]
    }
  ]
}
```

#### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | SVM unique identifier |
| name | string | SVM name |
| state | string | Operational state |
| subtype | string | SVM subtype/purpose |
| language | string | Default language setting |
| max_volumes | integer | Maximum number of volumes |
| allowed_protocols | array | Enabled data protocols |

#### SVM States

| State | Description |
|-------|-------------|
| running | SVM is operational and serving data |
| stopped | SVM is stopped and not serving data |
| starting | SVM is in the process of starting |
| stopping | SVM is in the process of stopping |

#### SVM Subtypes

| Subtype | Description |
|---------|-------------|
| default | Standard data-serving SVM |
| dp_destination | Data protection destination SVM |
| sync_destination | Synchronous replication destination |
| sync_source | Synchronous replication source |

#### Supported Protocols

| Protocol | Description |
|----------|-------------|
| nfs | Network File System |
| cifs | Common Internet File System (SMB) |
| iscsi | Internet Small Computer System Interface |
| fc | Fibre Channel |
| nvme | NVMe over Fabrics |
| s3 | Simple Storage Service |

#### Language Settings

| Language | Description |
|----------|-------------|
| c.utf_8 | English UTF-8 (default) |
| ja | Japanese |
| zh | Chinese |
| ko | Korean |

#### Example Usage

```bash
curl -X GET http://localhost:8080/api/svm/svms \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Common Use Cases

### 1. SVM Inventory and Status
```bash
# List all SVMs
curl -X GET http://localhost:8080/api/svm/svms \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check SVM states
curl -X GET http://localhost:8080/api/svm/svms \
  -H "Authorization: Bearer YOUR_TOKEN" | grep -E "(name|state)"
```

### 2. Protocol Configuration Audit
```bash
# Review protocol assignments
curl -X GET http://localhost:8080/api/svm/svms \
  -H "Authorization: Bearer YOUR_TOKEN" | grep -E "(name|allowed_protocols)"
```

### 3. Capacity Planning
```bash
# Check volume limits
curl -X GET http://localhost:8080/api/svm/svms \
  -H "Authorization: Bearer YOUR_TOKEN" | grep -E "(name|max_volumes)"
```

---

## SVM Architecture

### Multi-Tenancy
SVMs provide secure multi-tenancy by:
- **Isolation** - Each SVM has its own namespace
- **Security** - Independent authentication and authorization
- **Networking** - Dedicated logical interfaces
- **Protocols** - Configurable protocol support per SVM

### Resource Management
- **Volumes** - Each SVM can host multiple volumes
- **Aggregates** - Volumes can span multiple aggregates
- **Network** - SVMs use logical interfaces (LIFs)
- **Protocols** - Protocols are enabled per SVM

### Data Protection
- **SnapMirror** - SVM-level replication
- **SnapVault** - SVM-level backup
- **MetroCluster** - SVM disaster recovery

---

## SVM Types and Use Cases

### 1. Data SVMs (default)
- **Purpose** - Serve data to clients
- **Protocols** - NFS, CIFS, iSCSI, FC
- **Use Cases** - File shares, databases, virtual machines

**Example Configuration:**
```json
{
  "name": "svm1",
  "subtype": "default", 
  "state": "running",
  "allowed_protocols": ["nfs", "cifs", "iscsi", "fc"]
}
```

### 2. Data Protection SVMs
- **Purpose** - Receive replicated data
- **Protocols** - Limited during replication
- **Use Cases** - Backup, disaster recovery

**Example Configuration:**
```json
{
  "name": "svm_backup",
  "subtype": "dp_destination",
  "state": "stopped", 
  "allowed_protocols": ["nfs"]
}
```

### 3. Administrative SVMs
- **Purpose** - Cluster management
- **Protocols** - Management protocols only
- **Use Cases** - System administration

---

## Mock Data Details

### Production SVMs

#### svm1 (Primary Data SVM)
- **UUID:** svm-uuid-001
- **State:** running
- **Max Volumes:** 1000
- **Protocols:** NFS, CIFS, iSCSI, FC
- **Use Case:** Multi-protocol data serving

#### svm2 (Secondary Data SVM)  
- **UUID:** svm-uuid-002
- **State:** running
- **Max Volumes:** 500
- **Protocols:** NFS, CIFS
- **Use Case:** File services only

### Data Protection SVM

#### svm_backup (Backup SVM)
- **UUID:** svm-uuid-003
- **State:** stopped (typical for DP destination)
- **Max Volumes:** 200
- **Protocols:** NFS
- **Use Case:** Data protection destination

---

## SVM Management Best Practices

### 1. Naming Conventions
- Use descriptive names (e.g., `svm_finance`, `svm_hr`)
- Include environment indicators (e.g., `svm_prod`, `svm_dev`)
- Follow organizational standards

### 2. Protocol Assignment
- Enable only required protocols per SVM
- Consider security implications of each protocol
- Plan for future protocol needs

### 3. Resource Limits
- Set appropriate volume limits based on use case
- Monitor volume usage against limits
- Plan for growth and scaling

### 4. Network Configuration
- Assign dedicated LIFs to each SVM
- Plan IP addressing schemes
- Configure appropriate VLANs

---

## Related APIs

### Resources Managed by SVMs
- [Storage APIs](./storage.md) - Volumes and qtrees within SVMs
- [Protocol APIs](./protocols.md) - Data protocols served by SVMs
- [Network APIs](./network.md) - Network interfaces assigned to SVMs

### SVM Dependencies
- [Cluster APIs](./cluster.md) - Cluster resources hosting SVMs
- Aggregate APIs - Storage pools for SVM volumes
- Network APIs - Physical infrastructure for SVM LIFs

---

## Example Workflows

### 1. SVM Health Check
```bash
# Check all SVM states
curl -X GET http://localhost:8080/api/svm/svms \
  -H "Authorization: Bearer YOUR_TOKEN" | \
  jq '.records[] | {name: .name, state: .state, protocols: .allowed_protocols}'
```

### 2. Protocol Audit
```bash
# List SVMs by protocol support
curl -X GET http://localhost:8080/api/svm/svms \
  -H "Authorization: Bearer YOUR_TOKEN" | \
  jq '.records[] | select(.allowed_protocols | contains(["iscsi"]))' 
```

### 3. Capacity Review
```bash
# Check volume limits
curl -X GET http://localhost:8080/api/svm/svms \
  -H "Authorization: Bearer YOUR_TOKEN" | \
  jq '.records[] | {name: .name, max_volumes: .max_volumes}'
```

---

## Integration Points

SVMs are central to NetApp ONTAP storage architecture and integrate with:

- **Volumes** - Storage containers within SVMs
- **LIFs** - Network access points for SVMs  
- **Protocols** - Data access methods enabled per SVM
- **Security** - Authentication and authorization per SVM
- **Replication** - Data protection relationships between SVMs
