# Script to test PATCH /accounts/me/ endpoint
# Usage: Run this after logging in to get a token

# Get token from localStorage (you need to be logged in first)
$token = "YOUR_JWT_TOKEN_HERE"
$apiUrl = "https://backenddoccheck-production-0a1c.up.railway.app/api/accounts/me/"

# Test data
$body = @{
    first_name = "TestFirstName"
    last_name = "TestLastName"
    email = "test@example.com"
    phone = "+1234567890"
} | ConvertTo-Json

Write-Host "Testing PATCH request to: $apiUrl"
Write-Host "Token: $token"
Write-Host "Body: $body"

$headers = @{
    'Authorization' = "Bearer $token"
    'Content-Type' = 'application/json'
}

$response = Invoke-WebRequest -Uri $apiUrl `
    -Method PATCH `
    -Headers $headers `
    -Body $body `
    -ContentType 'application/json' `
    -ErrorAction Continue

Write-Host "Status: $($response.StatusCode)"
Write-Host "Response: $($response.Content)"
