# Quick Installation Commands for Windows Server

# 1. PREPARE POWERSHELL (Run as Administrator)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. INSTALL CHOCOLATEY (Optional but recommended)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 3. INSTALL DEPENDENCIES (Choose one method)

# Method A: Chocolatey (if installed above)
choco install nodejs python git -y

# Method B: Manual downloads (if no Chocolatey)
# Node.js: https://nodejs.org/en/download/
# Python: https://www.python.org/downloads/windows/ (CHECK "Add to PATH")
# Git: https://git-scm.com/download/win

# 4. DOWNLOAD AND RUN DEPLOYMENT SCRIPTS
mkdir C:\temp
cd C:\temp

# Download the repository
git clone https://github.com/matthewmeekins/FG-TextExtract.git
cd FG-TextExtract
git checkout web-service

# Run system check
.\system-check.ps1

# Run deployment (fix any issues from system check first)
.\deploy.ps1

# For production deployment with PM2 service
.\deploy.ps1 -Production

# 5. START THE SERVICE
cd C:\TextExtraction\FG-TextExtract
node web_server.js

# 6. ACCESS THE WEB INTERFACE
# Open browser to: http://localhost:3000

# 7. PRODUCTION SERVICE COMMANDS (if using PM2)
pm2 start web_server.js --name "text-extraction-service"
pm2 startup
pm2 save
pm2 status

# 8. TROUBLESHOOTING COMMANDS

# Check what's using port 3000
netstat -ano | findstr :3000

# Kill process on port 3000
$process = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($process) { Stop-Process -Id $process.OwningProcess -Force }

# Test Python
python --version
python -c "import pandas; print('Python working')"

# Test Node
node --version
node -e "console.log('Node working')"

# Check firewall rule
Get-NetFirewallRule -DisplayName "*Text Extraction*"

# Create firewall rule manually
New-NetFirewallRule -DisplayName "Text Extraction Service" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow

# View PM2 logs
pm2 logs text-extraction-service

# Restart PM2 service
pm2 restart text-extraction-service