# Simple test for authentication
$baseUrl = "http://localhost:9001"

Write-Host "Testing authentication..." -ForegroundColor Yellow

# Using Invoke-WebRequest for more control
$body = '{"username": "Administrator", "password": "Vtech@123"}'
$headers = @{
    'Content-Type' = 'application/json'
}

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/security/authentication/cluster-tokens" -Method POST -Body $body -Headers $headers
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
    
    # Parse the JSON response
    $jsonResponse = $response.Content | ConvertFrom-Json
    Write-Host "Token: $($jsonResponse.token.Substring(0,20))..." -ForegroundColor Green
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
}
