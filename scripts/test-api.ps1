# API test helper
# Run the server first, then invoke this script.
$BASE = "http://localhost:5000"
Invoke-RestMethod -Uri "$BASE/health" -Method GET
