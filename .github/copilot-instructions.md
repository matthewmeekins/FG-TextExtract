<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Text Extraction Project Instructions

This project processes 17,000 .txt files and extracts structured data into CSV format.

## Project Context
- Extract dates (invoice, due, order, ship dates with priority)
- Identify vendor names using character case patterns
- Find invoice numbers near "invoice" text
- Extract currency amounts (total and all instances)
- Generate text excerpts for searchability

## Code Guidelines
- Use regex patterns for text extraction
- Implement robust date parsing with multiple formats
- Handle file processing errors gracefully
- Use pandas for CSV output
- Include progress tracking for large batch processing
- Follow Python best practices for file I/O