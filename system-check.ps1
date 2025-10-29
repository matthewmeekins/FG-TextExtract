# Text Extraction Service - System Check Script
# Run this AFTER installing all dependencies

Write-Host "=== TEXT EXTRACTION SERVICE - SYSTEM CHECK ===" -ForegroundColor Green
Write-Host ""

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to check port availability
function Test-Port($port) {
    $connection = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
    return $connection.TcpTestSucceeded
}

# 1. Check Git
Write-Host "1. Checking Git..." -ForegroundColor Yellow
if (Test-Command git) {
    $gitVersion = git --version
    Write-Host "   ✓ Git installed: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ Git NOT FOUND - Install from https://git-scm.com/" -ForegroundColor Red
}

# 2. Check Node.js
Write-Host "2. Checking Node.js..." -ForegroundColor Yellow
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "   ✓ Node.js installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ Node.js NOT FOUND - Install from https://nodejs.org/" -ForegroundColor Red
}

# 3. Check NPM
Write-Host "3. Checking NPM..." -ForegroundColor Yellow
if (Test-Command npm) {
    $npmVersion = npm --version
    Write-Host "   ✓ NPM installed: $npmVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ NPM NOT FOUND - Should come with Node.js" -ForegroundColor Red
}

# 4. Check Python
Write-Host "4. Checking Python..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "   ✓ Python installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ Python NOT FOUND - Install from https://python.org/" -ForegroundColor Red
}

# 5. Check PIP
Write-Host "5. Checking PIP..." -ForegroundColor Yellow
if (Test-Command pip) {
    $pipVersion = pip --version
    Write-Host "   ✓ PIP installed: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ PIP NOT FOUND - Should come with Python" -ForegroundColor Red
}

# 6. Check PM2 (optional)
Write-Host "6. Checking PM2 (optional)..." -ForegroundColor Yellow
if (Test-Command pm2) {
    $pm2Version = pm2 --version
    Write-Host "   ✓ PM2 installed: $pm2Version" -ForegroundColor Green
} else {
    Write-Host "   ! PM2 not installed - Install with: npm install -g pm2" -ForegroundColor Orange
}

# 7. Check Port 3000
Write-Host "7. Checking Port 3000 availability..." -ForegroundColor Yellow
if (Test-Port 3000) {
    Write-Host "   ✗ Port 3000 is IN USE - Stop the service using it" -ForegroundColor Red
    Write-Host "     Find what's using it: netstat -ano | findstr :3000" -ForegroundColor Red
} else {
    Write-Host "   ✓ Port 3000 is AVAILABLE" -ForegroundColor Green
}

# 8. Check Windows Firewall for Port 3000
Write-Host "8. Checking Windows Firewall..." -ForegroundColor Yellow
$firewallRule = Get-NetFirewallRule -DisplayName "*3000*" -ErrorAction SilentlyContinue
if ($firewallRule) {
    Write-Host "   ✓ Firewall rule found for port 3000" -ForegroundColor Green
} else {
    Write-Host "   ! No firewall rule for port 3000" -ForegroundColor Orange
    Write-Host "     Create rule: New-NetFirewallRule -DisplayName 'Text Extraction Service' -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow" -ForegroundColor Orange
}

# 9. Check Execution Policy
Write-Host "9. Checking PowerShell Execution Policy..." -ForegroundColor Yellow
$policy = Get-ExecutionPolicy
if ($policy -eq "Restricted") {
    Write-Host "   ✗ Execution Policy is Restricted - Run: Set-ExecutionPolicy RemoteSigned" -ForegroundColor Red
} else {
    Write-Host "   ✓ Execution Policy: $policy" -ForegroundColor Green
}

# 10. Check Available Disk Space
Write-Host "10. Checking Disk Space..." -ForegroundColor Yellow
$disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
$freeGB = [math]::Round($disk.FreeSpace / 1GB, 2)
if ($freeGB -gt 5) {
    Write-Host "   ✓ Available disk space: $freeGB GB" -ForegroundColor Green
} else {
    Write-Host "   ⚠ Low disk space: $freeGB GB - Consider freeing up space" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== SYSTEM CHECK COMPLETE ===" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Fix any ✗ issues above" -ForegroundColor White
Write-Host "2. Run deployment script: .\deploy.ps1" -ForegroundColor White
Write-Host "3. Follow step-by-step installation guide" -ForegroundColor White