"""
Password hashing and security utilities
Provides secure password hashing with salt for user authentication
"""

from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import hashlib

class PasswordUtility:
    """Utility class for password hashing and validation."""
    
    # Configuration
    HASH_METHOD = 'pbkdf2:sha256'
    SALT_LENGTH = 32
    
    @staticmethod
    def generate_salt():
        """
        Generate a cryptographically secure salt.
        
        Returns:
            str: Hex-encoded salt string
        """
        return secrets.token_hex(PasswordUtility.SALT_LENGTH // 2)
    
    @staticmethod
    def hash_password(password, salt=None):
        """
        Hash a password with optional salt.
        
        Args:
            password (str): Plain text password to hash
            salt (str, optional): Salt to use. If None, a new salt is generated
            
        Returns:
            str: Werkzeug password hash string
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Werkzeug's generate_password_hash handles salt generation automatically
        # We pass salt parameter for configuration
        return generate_password_hash(
            password,
            method=PasswordUtility.HASH_METHOD,
            salt_length=PasswordUtility.SALT_LENGTH
        )
    
    @staticmethod
    def verify_password(password, password_hash):
        """
        Verify a password against its hash.
        
        Args:
            password (str): Plain text password to verify
            password_hash (str): Hash to verify against
            
        Returns:
            bool: True if password matches hash, False otherwise
        """
        if not password or not password_hash:
            return False
        
        try:
            return check_password_hash(password_hash, password)
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_password_strong(password):
        """
        Check if password meets strength requirements.
        
        Requirements:
        - At least 8 characters
        - Contains uppercase letter
        - Contains lowercase letter
        - Contains digit
        - Contains special character
        
        Args:
            password (str): Password to check
            
        Returns:
            tuple: (is_strong: bool, feedback: list of str)
        """
        feedback = []
        
        if len(password) < 8:
            feedback.append("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            feedback.append("Password must contain an uppercase letter")
        
        if not any(c.islower() for c in password):
            feedback.append("Password must contain a lowercase letter")
        
        if not any(c.isdigit() for c in password):
            feedback.append("Password must contain a digit")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            feedback.append("Password must contain a special character")
        
        is_strong = len(feedback) == 0
        return is_strong, feedback
    
    @staticmethod
    def hash_email(email):
        """
        Create a secure hash of an email address.
        Useful for gravatar or other integrations.
        
        Args:
            email (str): Email address to hash
            
        Returns:
            str: SHA256 hash of lowercase email
        """
        if not email:
            raise ValueError("Email cannot be empty")
        
        email_lower = email.lower().strip()
        return hashlib.sha256(email_lower.encode()).hexdigest()
