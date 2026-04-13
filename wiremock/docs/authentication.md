# Authentication APIs

## Overview

The Authentication API provides secure access to NetApp ONTAP cluster resources through token-based authentication.

## Base Path
```
/api/security/authentication
```

---

## Endpoints

### 🔑 POST /cluster-tokens

**Purpose:** Authenticate with the cluster and obtain an access token

**Description:** 
This endpoint authenticates a user with username/password credentials and returns a JWT token for accessing other APIs. The token must be included in the Authorization header of subsequent requests.

#### Request

**Method:** `POST`  
**URL:** `/api/security/authentication/cluster-tokens`  
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| username | string | Yes | NetApp cluster username |
| password | string | Yes | NetApp cluster password |

#### Response

**Success Response (201 Created):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTU4ODI0ODA4OCwiZXhwIjoxNTg4MjUxNjg4fQ.token123"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

#### Example Usage

**Successful Authentication:**
```bash
curl -X POST http://localhost:8080/api/security/authentication/cluster-tokens \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password"
  }'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTU4ODI0ODA4OCwiZXhwIjoxNTg4MjUxNjg4fQ.token123"
}
```

**Failed Authentication:**
```bash
curl -X POST http://localhost:8080/api/security/authentication/cluster-tokens \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "wrongpassword"
  }'
```

**Response:**
```json
{
  "error": "Invalid credentials"
}
```

#### Using the Token

Once you have the token, include it in subsequent API calls:

```bash
curl -X GET http://localhost:8080/api/cluster \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTU4ODI0ODA4OCwiZXhwIjoxNTg4MjUxNjg4fQ.token123"
```

---

## Mock Configuration

### Valid Credentials
- **Username:** `admin`
- **Password:** `password`

### Token Details
- **Type:** JWT (JSON Web Token)
- **Algorithm:** HS256
- **Expiration:** 1 hour (configurable)
- **Example Token:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTU4ODI0ODA4OCwiZXhwIjoxNTg4MjUxNjg4fQ.token123`

### Behavior
- Any credentials other than `admin`/`password` will return 401 Unauthorized
- Successful authentication returns 201 Created with token
- Token is required for all other API endpoints (though not validated in mock)

---

## Security Notes

⚠️ **Important:** This is a mock server for development/testing only. In production:

1. Use strong, unique passwords
2. Implement proper token validation
3. Use HTTPS for all authentication requests
4. Implement token refresh mechanisms
5. Follow NetApp ONTAP security best practices

---

## Related APIs

After authentication, you can access:
- [Cluster APIs](./cluster.md) - Cluster information and management
- [Storage APIs](./storage.md) - Storage resource management  
- [Network APIs](./network.md) - Network configuration
- [Protocol APIs](./protocols.md) - Protocol configuration
- [SVM APIs](./svm.md) - Storage Virtual Machine management
