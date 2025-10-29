"""Currency amount extraction module."""

import re
from typing import Dict, List, Optional


class CurrencyExtractor:
    """Extracts currency amounts from text."""
    
    def __init__(self):
        # Currency symbols
        self.currency_symbols = ['$', '€', '£', '¥', '₹', '¢', '₦', '₡', '₪', '₱', '₨', '₩', '₴', '₽']
        
        # Currency patterns
        self.currency_patterns = [
            # Symbol before amount: $123.45, $1,234.56
            r'[$€£¥₹¢₦₡₪₱₨₩₴₽]\s*([0-9,]+\.?[0-9]*)',
            
            # Amount with symbol after: 123.45$, 1234€
            r'([0-9,]+\.?[0-9]*)\s*[$€£¥₹¢₦₡₪₱₨₩₴₽]',
            
            # USD, EUR, etc. patterns
            r'([0-9,]+\.?[0-9]*)\s*(?:USD|EUR|GBP|JPY|INR|CAD|AUD)\b',
            r'(?:USD|EUR|GBP|JPY|INR|CAD|AUD)\s*([0-9,]+\.?[0-9]*)',
            
            # Total/amount keywords
            r'(?:total|amount|sum|due|balance|pay|price|cost)[:\s]*\$?\s*([0-9,]+\.?[0-9]*)',
            r'([0-9,]+\.?[0-9]*)\s*(?:total|due|balance)',
        ]
        
        # Keywords that might indicate the final/total amount
        self.total_keywords = [
            'total', 'grand total', 'amount due', 'balance due', 'final amount',
            'total amount', 'amount owed', 'total due', 'pay', 'payment',
            'sum', 'balance', 'invoice total', 'bill total'
        ]
    
    def extract_amounts(self, text: str) -> Dict[str, str]:
        """Extract currency amounts from text."""
        all_amounts = self._find_all_amounts(text)
        
        # Find the total amount (likely the last/largest amount)
        total_amount = self._find_total_amount(text, all_amounts)
        
        # Format other amounts (excluding the total)
        other_amounts = [amt for amt in all_amounts if amt != total_amount]
        
        return {
            'total': total_amount,
            'other_amounts': ', '.join(other_amounts) if other_amounts else ''
        }
    
    def _find_all_amounts(self, text: str) -> List[str]:
        """Find all currency amounts in the text."""
        amounts = []
        text_lower = text.lower()
        
        for pattern in self.currency_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                amount_str = match.group(1) if match.groups() else match.group(0)
                
                # Clean and validate the amount
                cleaned_amount = self._clean_amount(amount_str)
                if cleaned_amount and self._is_valid_amount(cleaned_amount):
                    # Format the amount consistently
                    formatted_amount = self._format_amount(cleaned_amount)
                    if formatted_amount not in amounts:
                        amounts.append(formatted_amount)
        
        # Sort amounts by value (descending) to help identify totals
        amounts.sort(key=lambda x: self._amount_to_float(x), reverse=True)
        
        return amounts
    
    def _find_total_amount(self, text: str, all_amounts: List[str]) -> str:
        """Find the most likely total amount."""
        if not all_amounts:
            return ""
        
        text_lower = text.lower()
        
        # Method 1: Look for amounts near total keywords
        for keyword in self.total_keywords:
            # Search for keyword followed by amount
            pattern = rf'{re.escape(keyword)}[:\s]*\$?\s*([0-9,]+\.?[0-9]*)'
            matches = re.finditer(pattern, text_lower)
            
            for match in matches:
                amount_str = match.group(1)
                cleaned = self._clean_amount(amount_str)
                if cleaned:
                    formatted = self._format_amount(cleaned)
                    if formatted in all_amounts:
                        return formatted
            
            # Search for amount followed by keyword
            pattern = rf'([0-9,]+\.?[0-9]*)\s*{re.escape(keyword)}'
            matches = re.finditer(pattern, text_lower)
            
            for match in matches:
                amount_str = match.group(1)
                cleaned = self._clean_amount(amount_str)
                if cleaned:
                    formatted = self._format_amount(cleaned)
                    if formatted in all_amounts:
                        return formatted
        
        # Method 2: Look for the last occurrence of the largest amount
        if all_amounts:
            largest_amount = all_amounts[0]  # Already sorted by value
            
            # Find the last occurrence of this amount in the text
            pattern = re.escape(largest_amount.replace('$', '').replace(',', ''))
            matches = list(re.finditer(pattern, text_lower))
            if matches:
                return largest_amount
        
        # Method 3: Return the largest amount as fallback
        return all_amounts[0] if all_amounts else ""
    
    def _clean_amount(self, amount_str: str) -> Optional[str]:
        """Clean and standardize an amount string."""
        if not amount_str:
            return None
        
        # Remove currency symbols and extra spaces
        cleaned = re.sub(r'[$€£¥₹¢₦₡₪₱₨₩₴₽]', '', amount_str)
        cleaned = cleaned.strip()
        
        # Remove any non-numeric characters except commas and periods
        cleaned = re.sub(r'[^\d,.]', '', cleaned)
        
        if not cleaned:
            return None
        
        return cleaned
    
    def _is_valid_amount(self, amount_str: str) -> bool:
        """Check if an amount string is valid."""
        if not amount_str:
            return False
        
        # Must contain at least one digit
        if not re.search(r'\d', amount_str):
            return False
        
        # Check for valid decimal format
        if '.' in amount_str:
            parts = amount_str.split('.')
            if len(parts) > 2:  # More than one decimal point
                return False
            if len(parts) == 2 and len(parts[1]) > 2:  # More than 2 decimal places
                return False
        
        # Convert to float to validate
        try:
            value = self._amount_to_float(amount_str)
            # Reasonable range for currency amounts
            return 0.01 <= value <= 999999999.99
        except (ValueError, TypeError):
            return False
    
    def _format_amount(self, amount_str: str) -> str:
        """Format amount consistently."""
        try:
            value = self._amount_to_float(amount_str)
            return f"${value:,.2f}"
        except (ValueError, TypeError):
            return f"${amount_str}"
    
    def _amount_to_float(self, amount_str: str) -> float:
        """Convert amount string to float."""
        if not amount_str:
            return 0.0
        
        # Remove dollar sign and other currency symbols
        cleaned = re.sub(r'[$€£¥₹¢₦₡₪₱₨₩₴₽]', '', amount_str)
        # Remove commas
        cleaned = cleaned.replace(',', '')
        
        return float(cleaned)