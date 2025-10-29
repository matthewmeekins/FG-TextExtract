# Text Extraction Project

A Python application for processing 17,000+ text files and extracting structured data into CSV format.

## Features

- **Date Extraction**: Identifies and prioritizes dates (invoice > due > order > ship > unknown)
- **Vendor Detection**: Uses character case patterns to identify potential vendor names
- **Invoice Number Extraction**: Finds invoice numbers near "invoice" text
- **Currency Processing**: Extracts total amounts and all currency instances
- **Text Excerpts**: Generates searchable previews of file content
- **Batch Processing**: Handles large volumes of files with progress tracking

## Project Structure

```
FG-TextExtract/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── data/
│   ├── input/                # Place your .txt files here
│   └── output/               # Generated CSV files
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
| `date_primary_yyyymmdd` | Primary date (highest priority) |
| `date1_yyyymmdd` to `date3_yyyymmdd` | All found dates |
| `date1_label` to `date3_label` | Date type labels |
| `date1_snippet` to `date3_snippet` | Context around dates |
| `date_count` | Number of dates found |
| `possible_vendor` | Potential vendor name |
| `invoice_no` | Extracted invoice number |
| `total` | Final/total amount |
| `other_amounts` | All other currency amounts |
| `errors` | Processing error messages |

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place Text Files**
   - Copy your .txt files to `data/input/`

3. **Run Processing**
   ```bash
   python main.py
   ```

4. **View Results**
   - Check `data/output/extracted_data.csv`
   - Review logs in `logs/processing.log`

## Configuration

Edit `src/config.py` or use environment variables:

```bash
export INPUT_DIR="path/to/your/txt/files"
export OUTPUT_FILE="path/to/output.csv"
export MAX_EXCERPT_LENGTH="500"
```

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

## Troubleshooting

**Common Issues:**
- **Empty output**: Check if .txt files are in `data/input/`
- **Encoding errors**: Files will be tried with multiple encodings
- **Memory issues**: Adjust batch size in config
- **No dates found**: Check date format patterns in `date_extractor.py`

**Logs Location:** `logs/processing.log`

## License

This project is for internal use.