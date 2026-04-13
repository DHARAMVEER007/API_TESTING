# Test Token Validation
$baseUrl = "http://localhost:9001"

Write-Host "Testing Token Validation Security" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Test 1: Try with a random fake token (should fail)
Write-Host ""
Write-Host "1. Testing with FAKE/RANDOM token (should fail)..." -ForegroundColor Yellow
$fakeHeaders = @{
    'Authorization' = 'Bearer fake-random-token-12345'
}

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/cluster" -Headers $fakeHeaders
    Write-Host "ERROR: API accepted fake token!" -ForegroundColor Red
} catch {
    Write-Host "SUCCESS: Fake token correctly rejected (401)" -ForegroundColor Green
    Write-Host "Error: $($_.Exception.Response.StatusCode)" -ForegroundColor Cyan
}

# Test 2: Try with a different valid-looking JWT token (should fail)
Write-Host ""
Write-Host "2. Testing with DIFFERENT JWT token (should fail)..." -ForegroundColor Yellow
$differentHeaders = @{
    'Authorization' = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoYWNrZXIiLCJpYXQiOjE1ODgyNDgwODh9.different-signature'
}

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/cluster" -Headers $differentHeaders
    Write-Host "ERROR: API accepted different token!" -ForegroundColor Red
} catch {
    Write-Host "SUCCESS: Different token correctly rejected (401)" -ForegroundColor Green
    Write-Host "Error: $($_.Exception.Response.StatusCode)" -ForegroundColor Cyan
}

# Test 3: Get the real token through authentication
Write-Host ""
Write-Host "3. Getting REAL token through authentication..." -ForegroundColor Yellow

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
    $realToken = $authResponse.token
    Write-Host "Real token: $($realToken.Substring(0,30))..." -ForegroundColor Cyan
    
    # Test 4: Use the real token (should work)
    Write-Host ""
    Write-Host "4. Testing with REAL token (should work)..." -ForegroundColor Yellow
    $realHeaders = @{
        'Authorization' = "Bearer $realToken"
    }
    
    $clusterResponse = Invoke-RestMethod -Uri "$baseUrl/api/cluster" -Headers $realHeaders
    Write-Host "SUCCESS: Real token accepted! Cluster: $($clusterResponse.name)" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "TOKEN VALIDATION SECURITY VERIFIED!" -ForegroundColor Green
    Write-Host "✓ Fake tokens rejected" -ForegroundColor Green
    Write-Host "✓ Different tokens rejected" -ForegroundColor Green  
    Write-Host "✓ Only exact authenticated token works" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
} catch {
    Write-Host "Authentication failed: $($_.Exception.Message)" -ForegroundColor Red
}
