"""
Email validation and verification utilities
Provides email format validation and verification functions
"""

import re
from flask import render_template_string

class EmailUtility:
    """Utility class for email validation and operations."""
    
    # Email regex pattern (RFC 5322 simplified)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    )
    
    # List of disposable email domains
    DISPOSABLE_DOMAINS = {
        'tempmail.com', '10minutemail.com', 'guerrillamail.com',
        'mailinator.com', 'fakeinbox.com', 'throwaway.email',
        'maildrop.cc', 'sharklasers.com', 'yopmail.com'
    }
    
    @staticmethod
    def validate_email_format(email):
        """
        Validate email format.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        if not email:
            return False, "Email address is required"
        
        email = email.strip().lower()
        
        if len(email) > 254:
            return False, "Email address is too long"
        
        if not EmailUtility.EMAIL_PATTERN.match(email):
            return False, "Email address format is invalid"
        
        local_part, domain = email.rsplit('@', 1)
        
        if len(local_part) > 64:
            return False, "Email local part is too long"
        
        if local_part.startswith('.') or local_part.endswith('.'):
            return False, "Email local part cannot start or end with a dot"
        
        if '..' in local_part:
            return False, "Email local part cannot contain consecutive dots"
        
        return True, "Email format is valid"
    
    @staticmethod
    def is_disposable_email(email):
        """
        Check if email uses a disposable email service.
        
        Args:
            email (str): Email address to check
            
        Returns:
            bool: True if email is from disposable domain, False otherwise
        """
        if not email:
            return False
        
        try:
            domain = email.lower().rsplit('@', 1)[1]
            return domain in EmailUtility.DISPOSABLE_DOMAINS
        except (IndexError, AttributeError):
            return False
    
    @staticmethod
    def normalize_email(email):
        """
        Normalize email address (lowercase, strip whitespace).
        
        Args:
            email (str): Email address to normalize
            
        Returns:
            str: Normalized email address
        """
        if not email:
            return ""
        
        return email.strip().lower()
    
    @staticmethod
    def extract_username_from_email(email):
        """
        Extract username part from email address.
        
        Args:
            email (str): Email address
            
        Returns:
            str: Username part (local part)
        """
        if not email:
            return ""
        
        try:
            return email.rsplit('@', 1)[0]
        except IndexError:
            return ""
    
    @staticmethod
    def validate_email_domain(email):
        """
        Validate email domain exists (basic check).
        
        Args:
            email (str): Email address to validate
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        if not email:
            return False, "Email is required"
        
        try:
            domain = email.rsplit('@', 1)[1]
            
            if not domain:
                return False, "Email domain is empty"
            
            # Basic domain validation
            if len(domain) < 3 or '.' not in domain:
                return False, "Email domain format is invalid"
            
            parts = domain.split('.')
            for part in parts:
                if not part or len(part) > 63:
                    return False, "Email domain part is invalid"
            
            return True, "Email domain is valid"
        except (IndexError, AttributeError):
            return False, "Email domain validation failed"
    
    @staticmethod
    def validate_email_comprehensive(email, allow_disposable=False):
        """
        Perform comprehensive email validation.
        
        Args:
            email (str): Email address to validate
            allow_disposable (bool): Allow disposable email services
            
        Returns:
            tuple: (is_valid: bool, errors: list)
        """
        errors = []
        
        # Check format
        is_valid, message = EmailUtility.validate_email_format(email)
        if not is_valid:
            errors.append(message)
            return False, errors
        
        # Check domain
        is_valid, message = EmailUtility.validate_email_domain(email)
        if not is_valid:
            errors.append(message)
            return False, errors
        
        # Check disposable
        if not allow_disposable and EmailUtility.is_disposable_email(email):
            errors.append("Disposable email addresses are not allowed")
            return False, errors
        
        return True, errors
