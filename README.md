# Text Extraction Service

A comprehensive text extraction solution with both Python CLI and web interface for processing .txt files and extracting structured data into CSV format.

## Features

- **Web Interface**: User-friendly branded web application
- **CLI Support**: Command-line interface for automated processing
- **Date Extraction**: Identifies and prioritizes dates (invoice > due > order > ship > unknown)
- **Vendor Detection**: Uses character case patterns to identify potential vendor names
- **Invoice Number Extraction**: Finds invoice numbers near "invoice" text
- **Currency Processing**: Extracts total amounts and all currency instances
- **Text Excerpts**: Generates searchable previews of file content
- **Batch Processing**: Handles large volumes of files with progress tracking
- **File Upload**: Supports ZIP files containing multiple .txt files or individual .txt files

## Project Structure

```
FG-TextExtract/
├── main.py                    # Main Python CLI application
├── web_server.js              # Node.js Express web service
├── package.json               # Node.js dependencies
├── requirements.txt           # Python dependencies
├── public/                    # Web interface files
│   ├── index.html            # Branded web interface
│   ├── bootstrap.css         # CSS framework
│   └── styles.css            # Custom theme styles
├── data/
│   ├── input/                # Place your .txt files here (CLI mode)
│   └── output/               # Generated CSV files
├── temp/                     # Temporary upload storage (web mode)
├── logs/                     # Processing logs
└── src/
    ├── config.py             # Configuration settings
    ├── extractors/           # Data extraction modules
    │   ├── date_extractor.py
    │   ├── vendor_extractor.py
    │   ├── invoice_extractor.py
    │   └── currency_extractor.py
    └── utils/
        └── file_utils.py     # File handling utilities
```

## CSV Output Columns

| Column | Description |
|--------|-------------|
| `filename` | Original file name |
| `text_excerpt` | Searchable text preview (500 chars) |
| `date_primary_mmddyyyy` | Primary date in US format (MM/DD/YYYY) |
| `date1_mmddyyyy` to `date3_mmddyyyy` | All found dates in US format |
| `date1_label` to `date3_label` | Date type labels |
| `date1_snippet` to `date3_snippet` | Context around dates |
| `date_count` | Number of dates found |
| `possible_vendor` | Potential vendor name |
| `invoice_no` | Extracted invoice number |
| `total` | Final/total amount |
| `other_amounts` | All other currency amounts |
| `errors` | Processing error messages |

## Quick Start

### Web Interface (Recommended)

1. **Install Dependencies**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Node.js dependencies
   npm install
   ```

2. **Start Web Service**
   ```bash
   node web_server.js
   ```

3. **Access Interface**
   - Open browser to `http://localhost:3000`
   - Upload ZIP files containing .txt files or individual .txt files
   - Download processed CSV results

### Command Line Interface

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place Text Files**
   - Copy your .txt files to `data/input/`

3. **Run Processing**
   ```bash
   # Basic usage (processes data/input/ folder)
   python main.py
   
   # Custom input/output paths
   python main.py --input /path/to/txt/files --output /path/to/output.csv
   ```

4. **View Results**
   - Check output CSV file
   - Review logs in `logs/processing.log`

## Configuration

### Web Service Configuration

The web service runs on port 3000 by default and includes:
- File upload handling (ZIP and TXT files)
- Temporary file storage in `temp/` directory
- Branded web interface
- Real-time processing feedback

### CLI Configuration

Edit `src/config.py` or use command line arguments:

```bash
# Command line arguments
python main.py --input "path/to/your/txt/files" --output "path/to/output.csv"

# Environment variables
export INPUT_DIR="path/to/your/txt/files"
export OUTPUT_FILE="path/to/output.csv"
export MAX_EXCERPT_LENGTH="500"
```

## Dependencies

### Python Requirements
- pandas
- numpy
- python-dateutil
- tqdm
- regex

### Node.js Requirements
- express
- multer
- path
- fs

## Date Priority System

The system prioritizes dates in this order:
1. **Invoice dates** - highest priority
2. **Due dates** - payment deadlines
3. **Order dates** - purchase orders
4. **Ship dates** - shipping information
5. **Unknown dates** - other detected dates

## Vendor Detection

Uses multiple strategies:
- **Case patterns** - Title Case Company Names
- **Business suffixes** - Corp, Inc, LLC, etc.
- **Keyword proximity** - Text near "vendor", "supplier"
- **ALL CAPS** - Company names in capitals

## Error Handling

- Gracefully handles file encoding issues
- Logs processing errors for debugging
- Continues processing if individual files fail
- Validates file sizes and formats

## Performance

- Progress tracking with tqdm
- Batch processing for memory efficiency
- Configurable file size limits
- Parallel processing ready architecture

## Development

### Python Development
Run tests:
```bash
pytest
```

Format code:
```bash
black .
```

Lint code:
```bash
flake8 .
```

### Web Service Development
Start in development mode:
```bash
node web_server.js
```

Check logs:
```bash
tail -f server.log
```

Test endpoints:
```bash
curl -I http://localhost:3000/
curl -I http://localhost:3000/bootstrap.css
```

## Troubleshooting

### Web Service Issues
- **Port 3000 in use**: Check if another service is running on port 3000
- **Upload fails**: Ensure file size is under 500MB limit
- **CSS not loading**: Clear browser cache and refresh
- **Service won't start**: Check if Node.js dependencies are installed with `npm install`

### CLI Issues
- **Empty output**: Check if .txt files are in specified input directory
- **Encoding errors**: Files will be tried with multiple encodings
- **Memory issues**: Adjust batch size in config
- **No dates found**: Check date format patterns in `date_extractor.py`

**Logs Location:** `logs/processing.log`

## Support

For assistance with this text extraction service, contact your system administrator.

## License

This project is for internal use.