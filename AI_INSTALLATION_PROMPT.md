# AI Assistant Prompt for Windows Server Installation

Copy and paste this entire prompt to ChatGPT to get expert guidance through the installation process:

---

**CONTEXT: You are helping me install a Text Extraction Service on a Windows Server. This is a Node.js web application with Python backend that processes .txt files and extracts structured data to CSV format.**

**PROJECT DETAILS:**
- Repository: https://github.com/matthewmeekins/FG-TextExtract
- Branch: web-service
- Web Interface: Runs on port 3000
- Backend: Python CLI for text processing
- Frontend: Node.js Express server with file upload

**SYSTEM REQUIREMENTS:**
- Windows Server 2016+ or Windows 10+
- Node.js v14+ LTS
- Python 3.8+ (with pip)
- Git for Windows
- 2GB+ RAM, 1GB+ disk space
- Port 3000 available

**INSTALLATION COMPONENTS NEEDED:**
1. Git for Windows
2. Node.js LTS (v18+) with npm
3. Python 3.8+ with pip (MUST add to PATH)
4. Optional: PM2 for production service
5. Optional: Chocolatey package manager

**PROJECT STRUCTURE:**
```
C:\TextExtraction\FG-TextExtract\
├── main.py                    # Python CLI application
├── web_server.js              # Node.js Express web service
├── package.json               # Node.js dependencies
├── requirements.txt           # Python dependencies
├── public/                    # Web interface files
├── data/input/               # Input .txt files (CLI mode)
├── data/output/              # Generated CSV files
├── temp/                     # Temporary upload storage
└── logs/                     # Processing logs
```

**DEPENDENCIES:**
Python packages: pandas, numpy, python-dateutil, tqdm, regex
Node.js packages: express, multer, path, fs

**INSTALLATION SCRIPTS PROVIDED:**
1. `system-check.ps1` - Validates all dependencies and system readiness
2. `deploy.ps1` - Automated deployment and setup
3. `QUICK_COMMANDS.ps1` - Copy/paste command reference

**COMMON ISSUES TO WATCH FOR:**
- Python not in PATH (most common issue)
- Port 3000 already in use
- PowerShell execution policy restrictions
- Windows Firewall blocking port 3000
- Missing Visual C++ redistributables for Python packages
- npm permission issues

**SUCCESS CRITERIA:**
- Web interface accessible at http://localhost:3000
- Can upload ZIP/TXT files through web interface
- Python CLI works: `python main.py --help`
- No errors in system check script

**PRODUCTION DEPLOYMENT:**
- Uses PM2 process manager
- Runs as Windows service
- Automatic startup on boot
- Log management and monitoring

**MY CURRENT SITUATION:**
I have a fresh/blank Windows server environment and need step-by-step guidance through the entire installation process. I want to understand each step and troubleshoot any issues that arise.

**PLEASE HELP ME:**
1. Guide me through the dependency installation process
2. Help me run and interpret the system check script results
3. Walk me through the deployment script execution
4. Troubleshoot any errors or issues that come up
5. Verify the installation is working correctly
6. Set up production service if needed

**COMMUNICATION STYLE:**
- Provide clear, step-by-step instructions
- Explain what each command does
- Help me understand any error messages
- Offer alternative solutions if something doesn't work
- Ask clarifying questions about my specific environment

**START HERE:** Ask me about my current Windows environment (version, admin access, etc.) and guide me through checking what's already installed before we begin the installation process.

---

**[PASTE THIS PROMPT TO CHATGPT AND IT WILL HAVE ALL THE CONTEXT NEEDED TO HELP YOU THROUGH THE INSTALLATION]**