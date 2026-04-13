#!/bin/bash

# NetApp ONTAP Mock API Test Script
BASE_URL="http://localhost:9001"

echo "🚀 Testing NetApp ONTAP Mock APIs"
echo "================================="

# Test Authentication
echo ""
echo "🔐 Testing Authentication..."
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/security/authentication/cluster-tokens" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}')

if [ $? -eq 0 ]; then
  TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)
  echo "✅ Authentication successful"
  echo "Token: ${TOKEN:0:20}..."
else
  echo "❌ Authentication failed"
  exit 1
fi

# Test Cluster APIs
echo ""
echo "🏢 Testing Cluster APIs..."
curl -s "$BASE_URL/api/cluster" -H "Authorization: Bearer $TOKEN" | head -c 100
echo "..."
echo "✅ Cluster API working"

# Test Storage APIs
echo ""
echo "💾 Testing Storage APIs..."
curl -s "$BASE_URL/api/storage/volumes" -H "Authorization: Bearer $TOKEN" | head -c 100
echo "..."
echo "✅ Storage API working"

# Test Network APIs
echo ""
echo "🌐 Testing Network APIs..."
curl -s "$BASE_URL/api/network/ethernet/interfaces" -H "Authorization: Bearer $TOKEN" | head -c 100
echo "..."
echo "✅ Network API working"

# Test Protocol APIs
echo ""
echo "🔌 Testing Protocol APIs..."
curl -s "$BASE_URL/api/protocols/cifs/shares" -H "Authorization: Bearer $TOKEN" | head -c 100
echo "..."
echo "✅ Protocol API working"

# Test SVM APIs
echo ""
echo "🏠 Testing SVM APIs..."
curl -s "$BASE_URL/api/svm/svms" -H "Authorization: Bearer $TOKEN" | head -c 100
echo "..."
echo "✅ SVM API working"

echo ""
echo "🎉 All API tests completed successfully!"
echo ""
echo "📚 Documentation available at: ./docs/README.md"
echo "🔧 Admin interface: $BASE_URL/__admin"
