"""Date extraction module for identifying and parsing dates from text."""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional
import dateutil.parser as date_parser


class DateExtractor:
    """Extracts dates from text with priority-based classification."""
    
    def __init__(self):
        # Date patterns with their corresponding labels
        self.date_patterns = {
            'invoice': [
                r'invoice\s*date[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'inv\s*date[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'invoice[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
            ],
            'due': [
                r'due\s*date[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'payment\s*due[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'due[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
            ],
            'order': [
                r'order\s*date[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'po\s*date[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'purchase\s*date[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
            ],
            'ship': [
                r'ship\s*date[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'shipping\s*date[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
                r'shipped[:\s]*([0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2,4})',
            ]
        }
        
        # Generic date patterns for unknown types
        self.generic_patterns = [
            r'[0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{4}',  # MM/DD/YYYY or DD/MM/YYYY
            r'[0-9]{4}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{1,2}',  # YYYY/MM/DD
            r'[0-9]{1,2}[\/\-\.][0-9]{1,2}[\/\-\.][0-9]{2}',  # MM/DD/YY
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+[0-9]{1,2},?\s+[0-9]{4}',  # Month DD, YYYY
            r'[0-9]{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+[0-9]{4}',  # DD Month YYYY
        ]
    
    def extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract all dates from text with labels and context."""
        dates = []
        text_lower = text.lower()
        
        # First, try labeled patterns
        for label, patterns in self.date_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    date_str = match.group(1) if match.groups() else match.group(0)
                    parsed_date = self._parse_date(date_str)
                    if parsed_date:
                        dates.append({
                            'raw_date': date_str,
                            'formatted_date': parsed_date.strftime('%m/%d/%Y'),
                            'label': label,
                            'snippet': self._get_context_snippet(text, match.start(), match.end()),
                            'confidence': 'high'
                        })
        
        # Then try generic patterns for unlabeled dates
        if len(dates) < 3:  # Only if we haven't found enough dates
            for pattern in self.generic_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    date_str = match.group(0)
                    # Skip if this date was already found with a label
                    if any(d['raw_date'].lower() == date_str.lower() for d in dates):
                        continue
                    
                    parsed_date = self._parse_date(date_str)
                    if parsed_date:
                        dates.append({
                            'raw_date': date_str,
                            'formatted_date': parsed_date.strftime('%m/%d/%Y'),
                            'label': 'unknown',
                            'snippet': self._get_context_snippet(text, match.start(), match.end()),
                            'confidence': 'medium'
                        })
        
        # Remove duplicates and sort by priority
        unique_dates = self._remove_duplicates(dates)
        return unique_dates[:3]  # Return up to 3 dates
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        try:
            # Clean the date string
            date_str = date_str.strip()
            
            # Try parsing with dateutil
            parsed = date_parser.parse(date_str, fuzzy=True)
            
            # Validate the year is reasonable (between 1900 and 2100)
            if 1900 <= parsed.year <= 2100:
                return parsed
            
        except (ValueError, TypeError, OverflowError):
            pass
        
        return None
    
    def _get_context_snippet(self, text: str, start: int, end: int, context_length: int = 50) -> str:
        """Get a context snippet around the matched date."""
        snippet_start = max(0, start - context_length)
        snippet_end = min(len(text), end + context_length)
        
        snippet = text[snippet_start:snippet_end].strip()
        
        # Clean up the snippet
        snippet = ' '.join(snippet.split())
        
        return snippet
    
    def _remove_duplicates(self, dates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate dates, keeping the one with highest priority."""
        unique_dates = []
        seen_dates = set()
        
        # Priority order for labels
        priority = {'invoice': 1, 'due': 2, 'order': 3, 'ship': 4, 'unknown': 5}
        
        # Sort by priority first
        sorted_dates = sorted(dates, key=lambda d: priority.get(d['label'], 5))
        
        for date_info in sorted_dates:
            formatted_date = date_info['formatted_date']
            if formatted_date not in seen_dates:
                seen_dates.add(formatted_date)
                unique_dates.append(date_info)
        
        return unique_dates