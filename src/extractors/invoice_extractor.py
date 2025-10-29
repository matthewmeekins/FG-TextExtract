"""Invoice number extraction module."""

import re
from typing import Optional


class InvoiceExtractor:
    """Extracts invoice numbers from text."""
    
    def __init__(self):
        # Patterns to find invoice numbers
        self.invoice_patterns = [
            # Look for "Invoice" followed by number-like patterns
            r'invoice\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
            r'inv\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
            r'invoice\s*(?:number|no|num)\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
            r'inv\s*(?:number|no|num)\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
            
            # Look for "Invoice:" or "Invoice #" patterns
            r'invoice\s*[:#]\s*([A-Z0-9\-]{3,20})',
            r'inv\s*[:#]\s*([A-Z0-9\-]{3,20})',
            
            # Look for standalone patterns near "invoice"
            r'(?:invoice|inv).*?([A-Z]{1,3}[0-9]{3,10})',
            r'(?:invoice|inv).*?([0-9]{3,10}[A-Z]{0,3})',
            
            # Bill number patterns
            r'bill\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
            r'bill\s*(?:number|no|num)\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
        ]
    
    def extract_invoice_number(self, text: str) -> str:
        """Extract invoice number from text."""
        text_lines = text.split('\n')
        
        # First, try line-by-line search for better context
        for line in text_lines:
            line_lower = line.lower().strip()
            if 'invoice' in line_lower or 'inv' in line_lower or 'bill' in line_lower:
                invoice_num = self._extract_from_line(line)
                if invoice_num:
                    return invoice_num
        
        # If not found, try full text search
        text_lower = text.lower()
        for pattern in self.invoice_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                invoice_num = match.group(1) if match.groups() else match.group(0)
                if self._is_valid_invoice_number(invoice_num):
                    return invoice_num.upper()
        
        return ""
    
    def _extract_from_line(self, line: str) -> str:
        """Extract invoice number from a single line."""
        line_lower = line.lower()
        
        # Simple patterns for line-based extraction
        patterns = [
            r'invoice\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
            r'inv\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
            r'bill\s*#?\s*:?\s*([A-Z0-9\-]{3,20})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line_lower, re.IGNORECASE)
            if match:
                invoice_num = match.group(1)
                if self._is_valid_invoice_number(invoice_num):
                    return invoice_num.upper()
        
        # Look for standalone alphanumeric patterns in invoice lines
        if 'invoice' in line_lower:
            # Find alphanumeric patterns
            alphanumeric_matches = re.findall(r'\b[A-Z0-9\-]{3,20}\b', line, re.IGNORECASE)
            for match in alphanumeric_matches:
                if self._is_valid_invoice_number(match):
                    return match.upper()
        
        return ""
    
    def _is_valid_invoice_number(self, candidate: str) -> bool:
        """Check if a candidate string looks like a valid invoice number."""
        if not candidate or len(candidate) < 3:
            return False
        
        # Remove common separators
        cleaned = candidate.replace('-', '').replace('_', '').replace(' ', '')
        
        # Must contain at least one digit
        if not re.search(r'\d', cleaned):
            return False
        
        # Should be mostly alphanumeric
        if not re.match(r'^[A-Z0-9\-_]{3,20}$', candidate, re.IGNORECASE):
            return False
        
        # Exclude common false positives
        false_positives = [
            'invoice', 'number', 'total', 'amount', 'date', 'due',
            'paid', 'balance', 'tax', 'shipping', 'subtotal'
        ]
        
        if candidate.lower() in false_positives:
            return False
        
        # Prefer patterns with both letters and numbers
        has_letter = re.search(r'[A-Z]', candidate, re.IGNORECASE)
        has_digit = re.search(r'\d', candidate)
        
        if has_letter and has_digit:
            return True
        
        # Accept pure numeric if it's long enough
        if candidate.isdigit() and len(candidate) >= 4:
            return True
        
        return False