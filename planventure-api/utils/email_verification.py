"""
Email verification utilities for PlanVenture API
"""
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import create_access_token, decode_token


class EmailVerificationUtility:
    """Utility for managing email verification tokens."""
    
    @staticmethod
    def create_verification_token(email: str, secret_key: str = None) -> str:
        """
        Create a verification token for email confirmation.
        
        Args:
            email: Email address to verify
            secret_key: JWT secret key (uses app config if not provided)
        
        Returns:
            Verification token
        """
        payload = {
            'email': email,
            'type': 'email_verification',
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return create_access_token(identity=email, expires_delta=timedelta(hours=24))
    
    @staticmethod
    def verify_email_token(token: str, secret_key: str = None) -> dict:
        """
        Verify and decode an email verification token.
        
        Args:
            token: Token to verify
            secret_key: JWT secret key
        
        Returns:
            Decoded token payload or None if invalid
        """
        try:
            decoded = decode_token(token)
            if decoded.get('type') == 'email_verification':
                return decoded
            return None
        except Exception:
            return None
    
    @staticmethod
    def send_verification_email(email: str, verification_token: str, base_url: str = "http://localhost:5000") -> bool:
        """
        Send verification email (stub - implement with email service).
        
        Args:
            email: Recipient email
            verification_token: Token for verification
            base_url: Base URL for verification link
        
        Returns:
            True if sent successfully, False otherwise
        """
        # TODO: Implement with actual email service (SendGrid, Mailgun, etc.)
        verification_link = f"{base_url}/auth/verify-email?token={verification_token}"
        print(f"[EMAIL] Verification link for {email}: {verification_link}")
        return True
    
    @staticmethod
    def send_password_reset_email(email: str, reset_token: str, base_url: str = "http://localhost:5000") -> bool:
        """
        Send password reset email.
        
        Args:
            email: Recipient email
            reset_token: Token for password reset
            base_url: Base URL for reset link
        
        Returns:
            True if sent successfully, False otherwise
        """
        # TODO: Implement with actual email service
        reset_link = f"{base_url}/auth/reset-password?token={reset_token}"
        print(f"[EMAIL] Password reset link for {email}: {reset_link}")
        return True


def require_email_verified(f):
    """
    Decorator to require email verification before accessing endpoint.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Check if user's email is verified
        return f(*args, **kwargs)
    return decorated_function
