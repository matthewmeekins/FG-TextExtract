# Windows Server Deployment Guide
## Text Extraction Service - Complete Installation Guide

---

## 📋 **INSTALLATION ORDER - Complete List**

### **Phase 1: Core System Dependencies**
1. **Windows Subsystem for Linux (WSL2)** - Optional but recommended
   - Download: Windows Store → Ubuntu 22.04 LTS
   - Or PowerShell: `wsl --install`

2. **Git for Windows**
   - Download: https://git-scm.com/download/win
   - Or Chocolatey: `choco install git`

3. **Node.js LTS (v18+)**
   - Download: https://nodejs.org/en/download/
   - Or Chocolatey: `choco install nodejs`

4. **Python 3.8+ (with pip)**
   - Download: https://www.python.org/downloads/windows/
   - Or Chocolatey: `choco install python`
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation

### **Phase 2: Optional Package Managers**
5. **Chocolatey** - Optional but helpful
   - PowerShell (Admin): `Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))`

6. **PM2 Process Manager** - For production service
   - After Node.js: `npm install -g pm2`
   - Windows Service: `npm install -g pm2-windows-service`

### **Phase 3: Project Dependencies**
7. **Python Packages** (from requirements.txt)
   - pandas, numpy, python-dateutil, tqdm, regex

8. **Node.js Packages** (from package.json)
   - express, multer, path, fs

---

## 🔧 **SYSTEM CHECK SCRIPT**

Save as: `system-check.ps1`

```powershell
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
```

---

## 🚀 **DEPLOYMENT SCRIPT**

Save as: `deploy.ps1`

```powershell
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
```

---

## 📋 **STEP-BY-STEP INSTALLATION GUIDE**

### **Step 1: Prepare System**
```powershell
# Open PowerShell as Administrator
# Set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Optional: Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### **Step 2: Install Dependencies (Choose Method)**

**Method A: Manual Downloads**
- Node.js: https://nodejs.org/en/download/
- Python: https://www.python.org/downloads/windows/
- Git: https://git-scm.com/download/win

**Method B: Chocolatey (if installed)**
```powershell
choco install nodejs python git -y
```

### **Step 3: Download and Run Scripts**
```powershell
# Download scripts to C:\temp
mkdir C:\temp
cd C:\temp

# Download system-check.ps1 and deploy.ps1 (copy from above)
# Or download from repository if available

# Run system check
.\system-check.ps1

# Fix any issues, then run deployment
.\deploy.ps1
```

### **Step 4: Start Service**
```powershell
# Navigate to installation
cd C:\TextExtraction\FG-TextExtract

# Start development server
node web_server.js

# Or for production (if PM2 installed)
pm2 start web_server.js --name "text-extraction-service"
pm2 startup
pm2 save
```

### **Step 5: Verify Installation**
```powershell
# Check service is running
# Open browser to: http://localhost:3000

# Test CLI
python main.py --help

# Check logs
Get-Content server.log -Wait
```

---

## 🔧 **TROUBLESHOOTING COMMANDS**

```powershell
# Check what's using port 3000
netstat -ano | findstr :3000

# Kill process on port 3000
$process = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($process) { Stop-Process -Id $process.OwningProcess -Force }

# Restart service
pm2 restart text-extraction-service

# View PM2 logs
pm2 logs text-extraction-service

# Check Python packages
pip list

# Check Node packages
npm list

# Test Python directly
python -c "import pandas; print('Pandas working')"

# Test Node directly
node -e "console.log('Node working')"
```

---

## 📝 **QUICK REFERENCE**

**Service Commands:**
```powershell
# Start manually
cd C:\TextExtraction\FG-TextExtract
node web_server.js

# Start with PM2
pm2 start web_server.js --name text-extraction-service

# Stop service
pm2 stop text-extraction-service

# Restart service
pm2 restart text-extraction-service

# View status
pm2 status

# View logs
pm2 logs text-extraction-service
```

**File Locations:**
- Installation: `C:\TextExtraction\FG-TextExtract\`
- Uploads: `C:\TextExtraction\FG-TextExtract\temp\`
- Output: `C:\TextExtraction\FG-TextExtract\data\output\`
- Logs: `C:\TextExtraction\FG-TextExtract\logs\`
- Server Log: `C:\TextExtraction\FG-TextExtract\server.log`