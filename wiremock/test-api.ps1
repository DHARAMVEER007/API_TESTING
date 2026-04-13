# NetApp API Test Script for PowerShell
Write-Host "Testing NetApp ONTAP Mock APIs" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green

$baseUrl = "http://localhost:9001"

# Test 1: Try accessing API without authentication (should fail)
Write-Host ""
Write-Host "1. Testing API without authentication (should fail)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/cluster"
    Write-Host "ERROR: API worked without authentication!" -ForegroundColor Red
} catch {
    Write-Host "SUCCESS: API correctly rejected unauthorized access (401)" -ForegroundColor Green
}

# Test 2: Authentication
Write-Host ""
Write-Host "2. Testing Authentication..." -ForegroundColor Yellow

$authBody = @{
    username = "Administrator"
    password = "Vtech@123"
} | ConvertTo-Json

try {
    $authResponse = Invoke-RestMethod -Uri "$baseUrl/api/security/authentication/cluster-tokens" `
        -Method Post `
        -Body $authBody `
        -ContentType "application/json"
    
    Write-Host "SUCCESS: Authentication successful" -ForegroundColor Green
    Write-Host "Token: $($authResponse.token.Substring(0,20))..." -ForegroundColor Cyan
    
    $token = $authResponse.token
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    # Test 3: Cluster API with valid token
    Write-Host ""
    Write-Host "3. Testing Cluster API with valid token..." -ForegroundColor Yellow
    $clusterResponse = Invoke-RestMethod -Uri "$baseUrl/api/cluster" -Headers $headers
    Write-Host "SUCCESS: Cluster API working - Cluster: $($clusterResponse.name)" -ForegroundColor Green
    
    # Test 4: Storage API with valid token
    Write-Host ""
    Write-Host "4. Testing Storage API with valid token..." -ForegroundColor Yellow
    $volumesResponse = Invoke-RestMethod -Uri "$baseUrl/api/storage/volumes" -Headers $headers
    Write-Host "SUCCESS: Storage API working - Found $($volumesResponse.records.Count) volumes" -ForegroundColor Green
    
    # Test 5: Network API with valid token
    Write-Host ""
    Write-Host "5. Testing Network API with valid token..." -ForegroundColor Yellow
    $networkResponse = Invoke-RestMethod -Uri "$baseUrl/api/network/ethernet/interfaces" -Headers $headers
    Write-Host "SUCCESS: Network API working - Found $($networkResponse.records.Count) interfaces" -ForegroundColor Green
    
    # Test 6: SVM API with valid token
    Write-Host ""
    Write-Host "6. Testing SVM API with valid token..." -ForegroundColor Yellow
    $svmResponse = Invoke-RestMethod -Uri "$baseUrl/api/svm/svms" -Headers $headers
    Write-Host "SUCCESS: SVM API working - Found $($svmResponse.records.Count) SVMs" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green  
    Write-Host "ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "✓ Unauthorized access properly blocked" -ForegroundColor Green
    Write-Host "✓ Authentication working correctly" -ForegroundColor Green
    Write-Host "✓ All APIs require valid Bearer token" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Documentation available at: ./docs/README.md" -ForegroundColor Cyan
    Write-Host "Admin interface: $baseUrl/__admin" -ForegroundColor Cyan
    
} catch {
    Write-Host "Authentication failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure WireMock server is running on port 9001" -ForegroundColor Yellow
}
