# ============================================================
#  RingHealth APK 灞€鍩熺綉娴嬭瘯 - 瀹屾暣鎸囧崡
# ============================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RingHealth LAN Testing Checklist" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Step 0: Check prerequisites ---
Write-Host "[Step 0] Checking environment..." -ForegroundColor Yellow

$checks = @(
    @{ name="Python (py)"; cmd="py --version"; expect="Python" },
    @{ name="JDK (java)"; cmd="java -version 2>&1"; expect="version" },
    @{ name="HBuilderX"; path="$env:USERPROFILE\AppData\Local\HBuilder X" },
    @{ name="ADB"; cmd="adb version 2>&1"; expect="Android Debug Bridge" }
)

$allOK = $true
foreach ($c in $checks) {
    if ($c.cmd) {
        $result = $c.cmd | cmd 2>&1
        if ($result -match $c.expect) { Write-Host "  [OK] $($c.name)" -ForegroundColor Green }
        else { Write-Host "  [!!] $($c.name) - NOT FOUND" -ForegroundColor Red; $allOK = $false }
    } elseif ($c.path) {
        if (Test-Path $c.path) { Write-Host "  [OK] $($c.name)" -ForegroundColor Green }
        else { Write-Host "  [!!] $($c.name) - NOT FOUND" -ForegroundColor Red; $allOK = $false }
    }
}

if (-not $allOK) {
    Write-Host ""
    Write-Host "[!] Some tools missing, but continuing..." -ForegroundColor Yellow
}

# --- Step 1: Get LAN IP ---
Write-Host ""
Write-Host "[Step 1] Network Configuration" -ForegroundColor Yellow
$lanIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -match 'WLAN|Ethernet|Wi-Fi' -and $_.IPAddress -notmatch '^127\.|^169\.|^172\.' }).IPAddress
if (-not $lanIP) { $lanIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch 'Loopback' -and $_.IPAddress -notmatch '^127\.|^169\.' })[0].IPAddress }
Write-Host "  Server LAN IP: $lanIP" -ForegroundColor White
Write-Host "  API URL: http://$lanIP`:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "  App.vue baseUrl should be: http://$lanIP`:5000" -ForegroundColor Gray

# Check App.vue
$appVue = Join-Path $PSScriptRoot "..\uniapp-client\App.vue"
if (Test-Path $appVue) {
    $content = Get-Content $appVue -Raw
    if ($content -match "baseUrl:\s*'http://([^']+)'") {
        $currentUrl = $Matches[1]
        if ($currentUrl -eq "http://$lanIP`:5000") {
            Write-Host "  [OK] App.vue baseUrl already set correctly" -ForegroundColor Green
        } else {
            Write-Host "  [!!] App.vue baseUrl is: $currentUrl" -ForegroundColor Yellow
            Write-Host "      Need to change to: http://$lanIP`:5000" -ForegroundColor Yellow
        }
    }
}

# --- Step 2: Firewall ---
Write-Host ""
Write-Host "[Step 2] Firewall (NEED ADMIN)" -ForegroundColor Yellow
Write-Host "  Please run this command as Administrator:" -ForegroundColor White
Write-Host "" 
Write-Host '  New-NetFirewallRule -DisplayName "RingHealth API"' -ForegroundColor Green
Write-Host '    -Direction Inbound -Protocol TCP -LocalPort 5000' -ForegroundColor Green  
Write-Host '    -Action Allow -Profile Private' -ForegroundColor Green
Write-Host ""
Write-Host "  Or via CMD (Admin):" -ForegroundColor Gray
Write-Host '  netsh advfirewall firewall add rule name="RingHealth API"' -ForegroundColor Green
Write-Host '    dir=in action=allow protocol=TCP localport=5000 profile=private' -ForegroundColor Green

# --- Step 3: Start Server ---
Write-Host ""
Write-Host "[Step 3] Start Backend Server" -ForegroundColor Yellow
Write-Host "  Open a NEW terminal and run:" -ForegroundColor White
Write-Host ""
Write-Host "    cd e:\鏅鸿兘浣揬ringhealth-app\server" -ForegroundColor Green
Write-Host "    py run.py" -ForegroundColor Green
Write-Host ""
Write-Host "  Expected output:" -ForegroundColor Gray
Write-Host "    Running on http://0.0.0.0:5000" -ForegroundColor DarkGray

# --- Step 4: Verify ---
Write-Host ""
Write-Host "[Step 4] Verify API is accessible" -ForegroundColor Yellow
Write-Host "  After server starts, run this to test:"
Write-Host ""
Write-Host "    curl http://$lanIP`:5000/api/v1/stats`" -ForegroundColor Green
Write-Host "    # or browser open: http://$lanIP`:5000/api/v1/stats`" -ForegroundColor Green

# --- Step 5: Package APK ---
Write-Host ""
Write-Host "[Step 5] Package APK with HBuilderX" -ForegroundColor Yellow
Write-Host "  1. Open HBuilderX -> Open project: e:\鏅鸿兘浣揬ringhealth-app\uniapp-client" -ForegroundColor White
Write-Host "  2. Menu: Publish -> Native App - Cloud Build" -ForegroundColor White
Write-Host "  3. Select Android" -ForegroundColor White
Write-Host "  4. Use certificate: ringhealth-release.keystore" -ForegroundColor White
Write-Host "  5. Wait for build completion (~5 min)" -ForegroundColor White
Write-Host "  6. Download APK file" -ForegroundColor White

# --- Step 6: Install & Test ---
Write-Host ""
Write-Host "[Step 6] Install on Phone & Test" -ForegroundColor Yellow
Write-Host "  Transfer options:" -ForegroundColor White
Write-Host "  A) USB: adb install ringhealth-app.apk" -ForegroundColor Green
Write-Host "  B) WeChat/QQ file transfer to phone" -ForegroundColor Green
Write-Host "  C) Copy to phone storage then install" -ForegroundColor Green
Write-Host ""
Write-Host "  Make sure PHONE is on SAME WiFi network!" -ForegroundColor Red
Write-Host "  Phone IP range: 192.168.2.*" -ForegroundColor Gray

# --- Test Checklist ---
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FUNCTIONAL TEST CHECKLIST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$tests = @(
    @{ n="1. Register new account";     d="Phone + Password + Register button" },
    @{ n="2. Login existing account";    d="Phone + Password + Login button" },
    @{ n="3. Dashboard data load";       d="Home page shows health data cards" },
    @{ n="4. Sleep page charts";         d="Sleep tab shows timeline + analysis" },
    @{ n="5. Improve tasks";             d="Improve tab shows AI plan + check items" },
    @{ n="6. Profile page";              d="Profile shows user info + membership" },
    @{ n="7. Device scan";               d="Device page scans BLE devices" },
    @{ n="8. Data center";               d="Data center shows history charts" },
    @{ n="9. TabBar navigation";         d="All 4 tabs switch correctly" },
    @{ n="10. API error handling";       d="Network error shows toast message" }
)

foreach ($t in $tests) {
    Write-Host "  [ ] $($t.n)" -ForegroundColor White
    Write-Host "      $($t.d)" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  GOOD LUCK!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

