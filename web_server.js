// @ts-nocheck
const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const unzipper = require('unzipper');

const app = express();
const PORT = 3000;

// Create temp directory for uploads
const tempDir = path.join(__dirname, 'temp');
if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir, { recursive: true });
}

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, tempDir);
    },
    filename: (req, file, cb) => {
        // Create unique filename with timestamp
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, `upload-${uniqueSuffix}.zip`);
    }
});

const upload = multer({ 
    storage: storage,
    fileFilter: (req, file, cb) => {
        if (file.mimetype === 'application/zip' || 
            file.originalname.endsWith('.zip') ||
            file.mimetype === 'text/plain' || 
            file.originalname.endsWith('.txt')) {
            cb(null, true);
        } else {
            cb(new Error('Only ZIP files and TXT files are allowed!'), false);
        }
    },
    limits: {
        fileSize: 500 * 1024 * 1024 // 500MB limit
    }
});

// Add request logging middleware FIRST
app.use((req, res, next) => {
    const logMessage = `${new Date().toISOString()} - ${req.method} ${req.url}`;
    console.log(logMessage);
    
    // Also write to file
    fs.appendFileSync('server.log', logMessage + '\n');
    
    next();
});

// Serve static files with explicit MIME types
app.use(express.static('public', {
    setHeaders: (res, path) => {
        if (path.endsWith('.css')) {
            res.setHeader('Content-Type', 'text/css');
        }
    }
}));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Explicit routes for CSS files
app.get('/bootstrap.css', (req, res) => {
    res.setHeader('Content-Type', 'text/css');
    res.sendFile(path.join(__dirname, 'public', 'bootstrap.css'));
});

app.get('/styles.css', (req, res) => {
    res.setHeader('Content-Type', 'text/css');
    res.sendFile(path.join(__dirname, 'public', 'styles.css'));
});

app.post('/upload', upload.array('files'), async (req, res) => {
    if (!req.files || req.files.length === 0) {
        return res.status(400).send('No files uploaded');
    }
    
    const jobId = Date.now();
    const extractDir = path.join(tempDir, `job-${jobId}`);
    const outputFile = path.join(tempDir, `results-${jobId}.csv`);
    
    try {
        // Create extraction directory
        fs.mkdirSync(extractDir, { recursive: true });
        
        // Process each file
        for (const file of req.files) {
            if (file.originalname.endsWith('.zip')) {
                // Extract ZIP file
                await new Promise((resolve, reject) => {
                    fs.createReadStream(file.path)
                        .pipe(unzipper.Extract({ path: extractDir }))
                        .on('close', resolve)
                        .on('error', reject);
                });
            } else if (file.originalname.endsWith('.txt')) {
                // Copy TXT file directly
                const destPath = path.join(extractDir, file.originalname);
                fs.copyFileSync(file.path, destPath);
            }
        }
        
        // Call Python script
        await new Promise((resolve, reject) => {
            const pythonPath = path.join(__dirname, 'venv', 'bin', 'python');
            const scriptPath = path.join(__dirname, 'main.py');
            
            const python = spawn(pythonPath, [scriptPath, '--input', extractDir, '--output', outputFile]);
            
            python.on('close', (code) => {
                if (code === 0) {
                    resolve();
                } else {
                    reject(new Error(`Python script exited with code ${code}`));
                }
            });
            
            python.on('error', reject);
        });
        
        // Send CSV file back
        res.download(outputFile, 'extracted_data.csv', (err) => {
            // Cleanup temp files
            req.files.forEach(file => {
                if (fs.existsSync(file.path)) fs.unlinkSync(file.path);
            });
            fs.rmSync(extractDir, { recursive: true, force: true });
            fs.unlinkSync(outputFile);
            
            if (err) {
                console.error('Download error:', err);
            }
        });
        
    } catch (error) {
        console.error('Processing error:', error);
        res.status(500).send('Error processing files: ' + error.message);
        
        // Cleanup on error
        req.files.forEach(file => {
            if (fs.existsSync(file.path)) fs.unlinkSync(file.path);
        });
        if (fs.existsSync(extractDir)) fs.rmSync(extractDir, { recursive: true, force: true });
        if (fs.existsSync(outputFile)) fs.unlinkSync(outputFile);
    }
});

app.listen(PORT, () => {
    console.log(`🚀 Text Extraction Service running at http://localhost:${PORT}`);
    console.log('Upload ZIP files to extract structured data to CSV');
});