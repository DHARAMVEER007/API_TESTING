# NetApp ONTAP WireMock Setup Guide

## Quick Start

### 1. Start the Mock Server

**Windows:**
```cmd
start-wiremock.bat
```

**Linux/macOS:**
```bash
chmod +x start-wiremock.sh
./start-wiremock.sh
```

**Manual:**
```bash
java -jar wiremock-standalone-3.13.1.jar --port 8080 --root-dir .
```

### 2. Test the APIs

**Windows:**
```cmd
# Install Git Bash or WSL to run the test script
bash test-apis.sh
```

**Linux/macOS:**
```bash
chmod +x test-apis.sh
./test-apis.sh
```

### 3. Access Points

- **Mock Server:** http://localhost:8080
- **Admin Interface:** http://localhost:8080/__admin
- **Documentation:** [docs/README.md](docs/README.md)

---

## Directory Structure

```
wiremock/
├── wiremock-standalone-3.13.1.jar    # WireMock server
├── mappings/                          # API endpoint mappings
│   ├── auth/
│   │   └── authentication.json       # Authentication endpoints
│   ├── cluster/
│   │   ├── cluster.json              # Cluster information
│   │   └── nodes.json                # Node management
│   ├── storage/
│   │   ├── aggregates.json           # Storage aggregates
│   │   ├── controllers.json          # Storage controllers
│   │   ├── disks.json                # Disk management
│   │   ├── volumes.json              # Volume management
│   │   └── qtrees.json               # Qtree management
│   ├── network/
│   │   ├── network.json              # Ethernet and IP interfaces
│   │   └── fc-ports.json             # Fibre Channel ports
│   ├── protocols/
│   │   ├── protocols.json            # CIFS shares
│   │   ├── iscsi.json                # iSCSI protocol
│   │   └── fc.json                   # Fibre Channel protocol
│   └── svm/
│       └── svms.json                 # Storage Virtual Machines
├── docs/                             # API documentation
│   ├── README.md                     # Main documentation
│   ├── authentication.md             # Auth API docs
│   ├── cluster.md                    # Cluster API docs
│   ├── storage.md                    # Storage API docs
│   ├── network.md                    # Network API docs
│   ├── protocols.md                  # Protocol API docs
│   └── svm.md                        # SVM API docs
├── start-wiremock.bat               # Windows startup script
├── start-wiremock.sh                # Linux/macOS startup script
├── test-apis.sh                     # API test script
└── SETUP.md                         # This file
```

---

## Configuration Options

### Basic Configuration

The mock server runs with these default settings:
- **Port:** 8080
- **Host:** localhost (all interfaces)
- **Mappings:** ./mappings/
- **Response Templating:** Enabled
- **Verbose Logging:** Enabled

### Custom Configuration

You can customize the server by modifying the startup scripts:

```bash
java -jar wiremock-standalone-3.13.1.jar \
  --port 9090 \                      # Custom port
  --bind-address 0.0.0.0 \          # Bind to all interfaces
  --root-dir /path/to/wiremock \    # Custom directory
  --https-port 8443 \               # Enable HTTPS
  --verbose                         # Detailed logging
```

### Environment Variables

You can set these environment variables:

```bash
export WIREMOCK_PORT=8080
export WIREMOCK_HOST=localhost
export WIREMOCK_ROOT=/path/to/wiremock
```

---

## Authentication

### Default Credentials

The mock server accepts these credentials:
- **Username:** `admin`
- **Password:** `password`

### Getting a Token

```bash
curl -X POST http://localhost:8080/api/security/authentication/cluster-tokens \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

### Using the Token

Include the token in all API requests:

```bash
curl -X GET http://localhost:8080/api/cluster \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## API Endpoints Summary

| Category | Base Path | Endpoints | Documentation |
|----------|-----------|-----------|---------------|
| Authentication | `/api/security/authentication` | 1 | [authentication.md](docs/authentication.md) |
| Cluster | `/api/cluster` | 3 | [cluster.md](docs/cluster.md) |
| Storage | `/api/storage` | 8 | [storage.md](docs/storage.md) |
| Network | `/api/network` | 3 | [network.md](docs/network.md) |
| Protocols | `/api/protocols` | 7 | [protocols.md](docs/protocols.md) |
| SVM | `/api/svm` | 1 | [svm.md](docs/svm.md) |

**Total Endpoints:** 23

---

## Testing and Validation

### Automated Testing

Run the test script to validate all endpoints:

```bash
./test-apis.sh
```

### Manual Testing

1. **Start the server**
2. **Authenticate** to get a token
3. **Test endpoints** using curl or Postman
4. **Check responses** match expected format

### Example Test Sequence

```bash
# 1. Get token
TOKEN=$(curl -s -X POST http://localhost:8080/api/security/authentication/cluster-tokens \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' | \
  grep -o '"token":"[^"]*' | cut -d'"' -f4)

# 2. Test cluster info
curl -X GET http://localhost:8080/api/cluster \
  -H "Authorization: Bearer $TOKEN"

# 3. Test storage volumes
curl -X GET http://localhost:8080/api/storage/volumes \
  -H "Authorization: Bearer $TOKEN"
```

---

## Troubleshooting

### Common Issues

#### Server Won't Start
- **Check Java version:** Requires Java 8 or higher
- **Check port availability:** Port 8080 might be in use
- **Check file permissions:** Ensure jar file is executable

```bash
# Check Java version
java -version

# Check port usage
netstat -an | grep 8080

# Make jar executable
chmod +x wiremock-standalone-3.13.1.jar
```

#### API Returns 404
- **Check URL path:** Ensure exact path from mappings
- **Check HTTP method:** GET/POST must match mapping
- **Check server logs:** Look for mapping errors

#### Authentication Fails
- **Check credentials:** Must be exactly `admin`/`password`
- **Check Content-Type:** Must be `application/json`
- **Check request body:** Must be valid JSON

### Debug Mode

Enable debug logging:

```bash
java -jar wiremock-standalone-3.13.1.jar \
  --port 8080 \
  --root-dir . \
  --verbose
```

### Admin Interface

Access the admin interface for debugging:
- **URL:** http://localhost:8080/__admin
- **Mappings:** View all configured endpoints
- **Requests:** See request/response history
- **Logs:** View server logs

---

## Integration with Development

### Using in Tests

```javascript
// Example Jest test
describe('NetApp API Client', () => {
  beforeAll(async () => {
    // Start WireMock server
    wiremockServer = spawn('java', ['-jar', 'wiremock-standalone-3.13.1.jar']);
  });

  it('should authenticate successfully', async () => {
    const response = await fetch('http://localhost:8080/api/security/authentication/cluster-tokens', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'admin', password: 'password' })
    });
    expect(response.status).toBe(201);
  });
});
```

### Using with Docker

```dockerfile
FROM openjdk:11-jre-slim
COPY wiremock-standalone-3.13.1.jar /app/
COPY mappings/ /app/mappings/
WORKDIR /app
EXPOSE 8080
CMD ["java", "-jar", "wiremock-standalone-3.13.1.jar", "--port", "8080"]
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Start NetApp Mock Server
  run: |
    java -jar wiremock/wiremock-standalone-3.13.1.jar \
      --port 8080 \
      --root-dir wiremock &
    sleep 5

- name: Run API Tests
  run: |
    npm test
```

---

## Support and Documentation

- **📚 API Documentation:** [docs/README.md](docs/README.md)
- **🔧 WireMock Documentation:** http://wiremock.org/docs/
- **🐛 Issues:** Check server logs and admin interface
- **💡 Examples:** See test-apis.sh for usage examples
