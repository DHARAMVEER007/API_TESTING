# Test Basic Authentication
$baseUrl = "http://localhost:9001"

Write-Host "Testing Basic Authentication..." -ForegroundColor Yellow

# Create Basic Auth header
$username = "Administrator"
$password = "Vtech@123"
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $username, $password)))

$headers = @{
    'Authorization' = "Basic $base64AuthInfo"
}

Write-Host "Using Basic Auth: Basic $base64AuthInfo" -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/security/authentication/cluster-tokens" -Method POST -Headers $headers
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
    
    # Parse the JSON response
    $jsonResponse = $response.Content | ConvertFrom-Json
    Write-Host "Token: $($jsonResponse.token.Substring(0,20))..." -ForegroundColor Green
    
    Write-Host ""
    Write-Host "SUCCESS: Basic Authentication working!" -ForegroundColor Green
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
}
