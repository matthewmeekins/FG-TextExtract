# Text Extraction Service - Deployment Script
# Run this AFTER system check passes

param(
    [string]$InstallPath = "C:\TextExtraction",
    [switch]$Production = $false
)

Write-Host "=== TEXT EXTRACTION SERVICE - DEPLOYMENT ===" -ForegroundColor Green
Write-Host "Installation Path: $InstallPath" -ForegroundColor Cyan
Write-Host ""

# Create installation directory
Write-Host "1. Creating installation directory..." -ForegroundColor Yellow
if (!(Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null
    Write-Host "   ✓ Created: $InstallPath" -ForegroundColor Green
} else {
    Write-Host "   ✓ Directory exists: $InstallPath" -ForegroundColor Green
}

# Set location
Set-Location $InstallPath

# Clone repository
Write-Host "2. Cloning repository..." -ForegroundColor Yellow
if (Test-Path "FG-TextExtract") {
    Write-Host "   ! Repository already exists, pulling latest..." -ForegroundColor Orange
    Set-Location "FG-TextExtract"
    git pull origin web-service
} else {
    git clone https://github.com/matthewmeekins/FG-TextExtract.git
    Set-Location "FG-TextExtract"
    git checkout web-service
    Write-Host "   ✓ Repository cloned" -ForegroundColor Green
}

# Install Python dependencies
Write-Host "3. Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "   ✓ Python packages installed" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Error installing Python packages: $_" -ForegroundColor Red
    exit 1
}

# Install Node.js dependencies
Write-Host "4. Installing Node.js dependencies..." -ForegroundColor Yellow
try {
    npm install
    Write-Host "   ✓ Node.js packages installed" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Error installing Node.js packages: $_" -ForegroundColor Red
    exit 1
}

# Create required directories
Write-Host "5. Creating required directories..." -ForegroundColor Yellow
$directories = @("data\input", "data\output", "temp", "logs")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "   ✓ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "   ✓ Exists: $dir" -ForegroundColor Green
    }
}

# Set permissions
Write-Host "6. Setting permissions..." -ForegroundColor Yellow
$acl = Get-Acl .
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Users", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
$acl.SetAccessRule($accessRule)
Set-Acl . $acl
Write-Host "   ✓ Permissions set" -ForegroundColor Green

# Configure firewall
Write-Host "7. Configuring Windows Firewall..." -ForegroundColor Yellow
try {
    $existingRule = Get-NetFirewallRule -DisplayName "Text Extraction Service" -ErrorAction SilentlyContinue
    if (!$existingRule) {
        New-NetFirewallRule -DisplayName "Text Extraction Service" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow | Out-Null
        Write-Host "   ✓ Firewall rule created" -ForegroundColor Green
    } else {
        Write-Host "   ✓ Firewall rule already exists" -ForegroundColor Green
    }
} catch {
    Write-Host "   ⚠ Could not configure firewall (requires admin): $_" -ForegroundColor Yellow
}

# Test installation
Write-Host "8. Testing installation..." -ForegroundColor Yellow
Write-Host "   Testing Python CLI..." -ForegroundColor Cyan
try {
    $testResult = python main.py --help
    Write-Host "   ✓ Python CLI working" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python CLI test failed: $_" -ForegroundColor Red
}

Write-Host "   Testing Node.js server..." -ForegroundColor Cyan
$job = Start-Job -ScriptBlock { 
    Set-Location $using:InstallPath\FG-TextExtract
    node web_server.js 
}
Start-Sleep 3
if ($job.State -eq "Running") {
    Write-Host "   ✓ Node.js server starts successfully" -ForegroundColor Green
    Stop-Job $job
    Remove-Job $job
} else {
    Write-Host "   ✗ Node.js server failed to start" -ForegroundColor Red
}

# Production setup
if ($Production) {
    Write-Host "9. Setting up production service..." -ForegroundColor Yellow
    try {
        npm install -g pm2
        npm install -g pm2-windows-service
        pm2 start web_server.js --name "text-extraction-service"
        pm2 save
        pm2-service-install
        Write-Host "   ✓ Production service configured" -ForegroundColor Green
    } catch {
        Write-Host "   ✗ Production setup failed: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== DEPLOYMENT COMPLETE ===" -ForegroundColor Green
Write-Host ""
Write-Host "INSTALLATION LOCATION: $InstallPath\FG-TextExtract" -ForegroundColor Cyan
Write-Host ""
Write-Host "TO START THE SERVICE:" -ForegroundColor Cyan
Write-Host "cd $InstallPath\FG-TextExtract" -ForegroundColor White
Write-Host "node web_server.js" -ForegroundColor White
Write-Host ""
Write-Host "ACCESS THE WEB INTERFACE:" -ForegroundColor Cyan
Write-Host "http://localhost:3000" -ForegroundColor White