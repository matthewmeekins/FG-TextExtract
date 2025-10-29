"""Vendor name extraction module using character case patterns."""

import re
from typing import Optional, List


class VendorExtractor:
    """Extracts potential vendor names from text using character case patterns."""
    
    def __init__(self):
        # Common vendor-related keywords that might appear near vendor names
        self.vendor_keywords = [
            'vendor', 'supplier', 'company', 'corp', 'corporation', 'inc', 'incorporated',
            'ltd', 'limited', 'llc', 'llp', 'pllc', 'co', 'group', 'enterprises',
            'services', 'solutions', 'systems', 'technologies', 'industries'
        ]
        
        # Words to exclude as they're unlikely to be vendor names
        self.exclude_words = [
            'invoice', 'bill', 'receipt', 'statement', 'total', 'amount', 'payment',
            'date', 'number', 'account', 'customer', 'order', 'purchase', 'sale',
            'tax', 'shipping', 'delivery', 'address', 'phone', 'email', 'website',
            'terms', 'conditions', 'description', 'quantity', 'price', 'subtotal',
            'discount', 'balance', 'due', 'paid', 'remit', 'billing', 'contact'
        ]
    
    def extract_vendor(self, text: str) -> str:
        """Extract the most likely vendor name from text."""
        candidates = []
        
        # Method 1: Look for capitalized words/phrases near vendor keywords
        keyword_candidates = self._find_near_keywords(text)
        candidates.extend(keyword_candidates)
        
        # Method 2: Look for title case company names
        title_case_candidates = self._find_title_case_names(text)
        candidates.extend(title_case_candidates)
        
        # Method 3: Look for all caps company names
        all_caps_candidates = self._find_all_caps_names(text)
        candidates.extend(all_caps_candidates)
        
        # Method 4: Look for company suffixes
        suffix_candidates = self._find_company_suffixes(text)
        candidates.extend(suffix_candidates)
        
        # Score and select the best candidate
        if candidates:
            best_candidate = self._select_best_candidate(candidates)
            return best_candidate
        
        return ""
    
    def _find_near_keywords(self, text: str) -> List[str]:
        """Find potential vendor names near vendor-related keywords."""
        candidates = []
        
        for keyword in self.vendor_keywords:
            # Look for the keyword and extract nearby capitalized text
            pattern = rf'(?i)\b{re.escape(keyword)}\b.{{0,100}}'
            matches = re.finditer(pattern, text)
            
            for match in matches:
                context = match.group(0)
                # Find capitalized words in the context
                cap_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', context)
                candidates.extend(cap_words)
        
        return candidates
    
    def _find_title_case_names(self, text: str) -> List[str]:
        """Find title case company names (First Letter Capitalized)."""
        # Pattern for title case words/phrases
        pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4}\b'
        matches = re.findall(pattern, text)
        
        # Filter out common non-vendor phrases
        filtered = []
        for match in matches:
            if not any(exclude.lower() in match.lower() for exclude in self.exclude_words):
                if len(match.split()) >= 2:  # Prefer multi-word names
                    filtered.append(match)
        
        return filtered
    
    def _find_all_caps_names(self, text: str) -> List[str]:
        """Find all caps company names."""
        # Pattern for all caps words (likely company names)
        pattern = r'\b[A-Z]{2,}(?:\s+[A-Z]{2,})*\b'
        matches = re.findall(pattern, text)
        
        # Filter out common abbreviations and non-vendor terms
        filtered = []
        for match in matches:
            if (len(match) >= 3 and 
                not any(exclude.upper() in match for exclude in self.exclude_words) and
                not re.match(r'^[A-Z]{1,3}$', match)):  # Exclude short abbreviations
                filtered.append(match)
        
        return filtered
    
    def _find_company_suffixes(self, text: str) -> List[str]:
        """Find company names by looking for common business suffixes."""
        suffix_patterns = [
            r'\b[A-Z][a-zA-Z\s&]+(?:Corp|Corporation|Inc|Incorporated|Ltd|Limited|LLC|LLP|PLLC|Co)\b',
            r'\b[A-Z][a-zA-Z\s&]+(?:Group|Enterprises|Services|Solutions|Systems|Technologies|Industries)\b'
        ]
        
        candidates = []
        for pattern in suffix_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            candidates.extend(matches)
        
        return candidates
    
    def _select_best_candidate(self, candidates: List[str]) -> str:
        """Select the best vendor candidate based on scoring."""
        if not candidates:
            return ""
        
        # Score candidates
        scored_candidates = []
        for candidate in candidates:
            score = self._score_candidate(candidate)
            scored_candidates.append((candidate, score))
        
        # Sort by score (highest first) and return the best
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        return scored_candidates[0][0].strip()
    
    def _score_candidate(self, candidate: str) -> int:
        """Score a vendor candidate based on various factors."""
        score = 0
        candidate_lower = candidate.lower()
        
        # Prefer longer names (but not too long)
        length = len(candidate)
        if 10 <= length <= 50:
            score += 10
        elif 5 <= length <= 60:
            score += 5
        
        # Prefer names with multiple words
        word_count = len(candidate.split())
        if word_count >= 2:
            score += 15
        
        # Bonus for business suffixes
        business_suffixes = ['corp', 'corporation', 'inc', 'incorporated', 'ltd', 'limited', 
                           'llc', 'llp', 'pllc', 'co', 'group', 'enterprises']
        if any(suffix in candidate_lower for suffix in business_suffixes):
            score += 20
        
        # Bonus for title case formatting
        if candidate.istitle():
            score += 10
        
        # Penalty for containing excluded words
        if any(exclude in candidate_lower for exclude in self.exclude_words):
            score -= 20
        
        # Penalty for all caps (unless it's short)
        if candidate.isupper() and len(candidate) > 10:
            score -= 5
        
        # Penalty for containing numbers
        if re.search(r'\d', candidate):
            score -= 10
        
        return score