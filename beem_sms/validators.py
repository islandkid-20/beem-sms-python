"""
Input validation utilities for Beem SMS SDK
"""

import re
from typing import List


class PhoneNumberValidator:
    """Phone number validation utilities"""
    
    # Basic international phone number regex (simplified)
    PHONE_PATTERN = re.compile(r'^\+?[1-9]\d{7,14}$')
    
    # Tanzania-specific patterns
    TANZANIA_PATTERNS = [
        re.compile(r'^\+255[67]\d{8}$'),  # +255 6XXXXXXXX or +255 7XXXXXXXX
        re.compile(r'^255[67]\d{8}$'),    # 255 6XXXXXXXX or 255 7XXXXXXXX
        re.compile(r'^0[67]\d{8}$'),      # 06XXXXXXXX or 07XXXXXXXX
    ]
    
    @classmethod
    def validate(cls, phone_number: str) -> bool:
        """Validate phone number format"""
        if not phone_number:
            return False
        
        # Remove spaces, dashes, and parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', phone_number)
        
        # Check general international format
        if cls.PHONE_PATTERN.match(cleaned):
            return True
        
        # Check Tanzania-specific formats
        return any(pattern.match(cleaned) for pattern in cls.TANZANIA_PATTERNS)
    
    @classmethod
    def clean(cls, phone_number: str) -> str:
        """Clean and format phone number to international format"""
        cleaned = re.sub(r'[\s\-\(\)]', '', phone_number)
        
        # Handle Tanzania numbers
        if cleaned.startswith('0'):
            # Convert 07XXXXXXXX to +255 7XXXXXXXX
            cleaned = f"+255{cleaned[1:]}"
        elif cleaned.startswith('255') and not cleaned.startswith('+'):
            # Convert 255 7XXXXXXXX to +255 7XXXXXXXX  
            cleaned = f"+{cleaned}"
        elif not cleaned.startswith('+'):
            # Assume it needs +255 prefix for Tanzania
            cleaned = f"+255{cleaned}"
        
        return cleaned
    
    @classmethod
    def validate_batch(cls, phone_numbers: List[str]) -> List[bool]:
        """Validate a batch of phone numbers"""
        return [cls.validate(number) for number in phone_numbers]