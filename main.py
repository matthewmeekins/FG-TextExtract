"""
Text Extraction and Processing Tool

This script processes .txt files and extracts structured data into CSV format.
It extracts dates, vendor names, invoice numbers, currency amounts, and text excerpts.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from tqdm import tqdm

from src.extractors.date_extractor import DateExtractor
from src.extractors.vendor_extractor import VendorExtractor
from src.extractors.invoice_extractor import InvoiceExtractor
from src.extractors.currency_extractor import CurrencyExtractor
from src.utils.file_utils import read_text_file
from src.config import Config


class TextProcessor:
    """Main class for processing text files and extracting data."""
    
    def __init__(self, config: Config):
        self.config = config
        self.date_extractor = DateExtractor()
        self.vendor_extractor = VendorExtractor()
        self.invoice_extractor = InvoiceExtractor()
        self.currency_extractor = CurrencyExtractor()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/processing.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single text file and extract all data."""
        try:
            # Read file content
            text_content = read_text_file(file_path)
            if not text_content:
                return self._create_empty_result(file_path.name, "Empty file")
            
            # Extract data
            result = {
                'filename': file_path.name,
                'text_excerpt': self._create_text_excerpt(text_content),
            }
            
            # Extract dates
            dates = self.date_extractor.extract_dates(text_content)
            result.update(self._format_dates(dates))
            
            # Extract vendor
            result['possible_vendor'] = self.vendor_extractor.extract_vendor(text_content)
            
            # Extract invoice number
            result['invoice_no'] = self.invoice_extractor.extract_invoice_number(text_content)
            
            # Extract currency amounts
            amounts = self.currency_extractor.extract_amounts(text_content)
            result['total'] = amounts.get('total', '')
            result['other_amounts'] = amounts.get('other_amounts', '')
            
            result['errors'] = ''
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return self._create_empty_result(file_path.name, str(e))
    
    def process_directory(self, input_dir: Path, output_file: Path) -> None:
        """Process all .txt files in a directory and save to CSV."""
        txt_files = list(input_dir.glob("*.txt"))
        
        if not txt_files:
            self.logger.warning(f"No .txt files found in {input_dir}")
            return
        
        self.logger.info(f"Found {len(txt_files)} .txt files to process")
        
        results = []
        for file_path in tqdm(txt_files, desc="Processing files"):
            result = self.process_file(file_path)
            results.append(result)
        
        # Save to CSV
        self._save_to_csv(results, output_file)
        self.logger.info(f"Processing complete. Results saved to {output_file}")
    
    def _create_text_excerpt(self, text: str, max_length: int = 500) -> str:
        """Create a searchable text excerpt."""
        # Clean up the text and create excerpt
        cleaned_text = ' '.join(text.split())
        if len(cleaned_text) <= max_length:
            return cleaned_text
        return cleaned_text[:max_length] + "..."
    
    def _format_dates(self, dates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format extracted dates into CSV columns."""
        result = {
            'date_primary_mmddyyyy': '',
            'date1_mmddyyyy': '',
            'date1_label': '',
            'date1_snippet': '',
            'date2_mmddyyyy': '',
            'date2_label': '',
            'date2_snippet': '',
            'date3_mmddyyyy': '',
            'date3_label': '',
            'date3_snippet': '',
            'date_count': len(dates)
        }
        
        if not dates:
            return result
        
        # Sort dates by priority (invoice > due > order > ship > unknown)
        priority_order = {'invoice': 1, 'due': 2, 'order': 3, 'ship': 4, 'unknown': 5}
        sorted_dates = sorted(dates, key=lambda d: priority_order.get(d.get('label', 'unknown'), 5))
        
        # Set primary date
        if sorted_dates:
            result['date_primary_mmddyyyy'] = sorted_dates[0].get('formatted_date', '')
        
        # Set up to 3 dates
        for i, date_info in enumerate(sorted_dates[:3]):
            idx = i + 1
            result[f'date{idx}_mmddyyyy'] = date_info.get('formatted_date', '')
            result[f'date{idx}_label'] = date_info.get('label', '')
            result[f'date{idx}_snippet'] = date_info.get('snippet', '')
        
        return result
    
    def _create_empty_result(self, filename: str, error: str = '') -> Dict[str, Any]:
        """Create an empty result with error information."""
        return {
            'filename': filename,
            'text_excerpt': '',
            'date_primary_mmddyyyy': '',
            'date1_mmddyyyy': '',
            'date1_label': '',
            'date1_snippet': '',
            'date2_mmddyyyy': '',
            'date2_label': '',
            'date2_snippet': '',
            'date3_mmddyyyy': '',
            'date3_label': '',
            'date3_snippet': '',
            'date_count': 0,
            'possible_vendor': '',
            'invoice_no': '',
            'total': '',
            'other_amounts': '',
            'errors': error
        }
    
    def _save_to_csv(self, results: List[Dict[str, Any]], output_file: Path) -> None:
        """Save results to CSV file."""
        if not results:
            self.logger.warning("No results to save")
            return
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Define column order
        columns = [
            'filename', 'text_excerpt', 'date_primary_mmddyyyy',
            'date1_mmddyyyy', 'date1_label', 'date1_snippet',
            'date2_mmddyyyy', 'date2_label', 'date2_snippet',
            'date3_mmddyyyy', 'date3_label', 'date3_snippet',
            'date_count', 'possible_vendor', 'invoice_no',
            'total', 'other_amounts', 'errors'
        ]
        
        # Create DataFrame and save
        df = pd.DataFrame(results)
        df = df.reindex(columns=columns, fill_value='')
        df.to_csv(output_file, index=False, encoding='utf-8')


def main():
    """Main entry point."""
    config = Config()
    processor = TextProcessor(config)
    
    input_dir = Path(config.input_directory)
    output_file = Path(config.output_file)
    
    if not input_dir.exists():
        print(f"Error: Input directory {input_dir} does not exist")
        return
    
    processor.process_directory(input_dir, output_file)


if __name__ == "__main__":
    main()