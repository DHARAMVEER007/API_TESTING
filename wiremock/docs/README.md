# NetApp ONTAP API Mock Server Documentation

This WireMock setup provides comprehensive mock responses for NetApp ONTAP REST APIs. The mock server simulates the behavior of a NetApp ONTAP cluster to help with development and testing.

## Quick Start

1. **Start WireMock Server:**
   ```bash
   java -jar wiremock-standalone-3.13.1.jar --port 8080 --root-dir ./wiremock
   ```

2. **Base URL:** 
   ```
   http://localhost:8080
   ```

3. **Authentication:**
   All endpoints (except authentication) require a valid token. First authenticate:
   ```bash
   curl -X POST http://localhost:8080/api/security/authentication/cluster-tokens \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"password"}'
   ```

## API Categories

### 🔐 [Authentication APIs](./authentication.md)
- Cluster token authentication
- Session management

### 🖥️ [Cluster Management APIs](./cluster.md)
- Cluster information and version
- Node management
- Licensing

### 💾 [Storage Management APIs](./storage.md)
- Aggregates
- Volumes and efficiency
- Disks and metrics
- Controllers
- Qtrees

### 🌐 [Network APIs](./network.md)
- Ethernet interfaces
- IP interfaces  
- Fibre Channel ports

### 🔌 [Protocol APIs](./protocols.md)
- CIFS/SMB shares
- iSCSI LUNs, initiators, targets
- Fibre Channel LUNs, initiators, targets

### 🏠 [SVM (Storage Virtual Machine) APIs](./svm.md)
- SVM management and configuration

## Common Response Format

All APIs return JSON responses with a common structure:

```json
{
  "records": [
    {
      // Resource objects
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/resource"
    }
  }
}
```

## Error Responses

Error responses follow this format:

```json
{
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE"
  }
}
```

## Testing with curl

All endpoints can be tested with curl. Examples are provided in each API documentation file.

## WireMock Configuration

- **Mappings Directory:** `mappings/` - Contains all API endpoint mappings
- **Docs Directory:** `docs/` - API documentation
- **Port:** 8080 (configurable)
- **Admin Interface:** http://localhost:8080/__admin

## Support Matrix

This mock server supports the following NetApp ONTAP API endpoints:

| Category | Endpoints | Status |
|----------|-----------|--------|
| Authentication | 1 | ✅ Complete |
| Cluster | 3 | ✅ Complete |
| Storage | 8 | ✅ Complete |
| Network | 3 | ✅ Complete |
| Protocols | 7 | ✅ Complete |
| SVM | 1 | ✅ Complete |

**Total Endpoints Mocked:** 23
