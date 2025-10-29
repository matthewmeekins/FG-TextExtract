"""Configuration settings for the text extraction project."""

import os
from pathlib import Path


class Config:
    """Configuration class for the text processing application."""
    
    def __init__(self):
        # Default settings
        self.input_directory = os.getenv('INPUT_DIR', 'data/input')
        self.output_file = os.getenv('OUTPUT_FILE', 'data/output/extracted_data.csv')
        self.log_directory = os.getenv('LOG_DIR', 'logs')
        
        # Text excerpt settings
        self.max_excerpt_length = int(os.getenv('MAX_EXCERPT_LENGTH', '500'))
        
        # Date extraction settings
        self.max_dates_per_file = int(os.getenv('MAX_DATES_PER_FILE', '3'))
        
        # Currency extraction settings
        self.currency_symbols = ['$', '€', '£', '¥', '₹']
        
        # Vendor extraction settings
        self.min_vendor_length = int(os.getenv('MIN_VENDOR_LENGTH', '3'))
        self.max_vendor_length = int(os.getenv('MAX_VENDOR_LENGTH', '50'))
        
        # Processing settings
        self.batch_size = int(os.getenv('BATCH_SIZE', '100'))
        self.max_file_size_mb = int(os.getenv('MAX_FILE_SIZE_MB', '10'))
        
        # Ensure directories exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            Path(self.input_directory),
            Path(self.output_file).parent,
            Path(self.log_directory)
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)