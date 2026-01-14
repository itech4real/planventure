"""
JWT token generation and validation utilities
Provides secure token management for user authentication
"""

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token, get_jwt_identity
from datetime import datetime, timedelta
import os

class JWTUtility:
    """Utility class for JWT token operations."""
    
    # Default token expiration times
    ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 24))  # hours
    REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30))  # days
    
    @staticmethod
    def create_tokens(user_id, additional_claims=None):
        """
        Create both access and refresh tokens for a user.
        
        Args:
            user_id (int): User ID to encode in token
            additional_claims (dict, optional): Extra claims to add to token
            
        Returns:
            dict: Dictionary with 'access_token' and 'refresh_token'
        """
        if not user_id:
            raise ValueError("User ID is required")
        
        claims = {'user_id': int(user_id)}
        if additional_claims:
            claims.update(additional_claims)
        
        access_token = create_access_token(
            identity=str(user_id),
            expires_delta=timedelta(hours=JWTUtility.ACCESS_TOKEN_EXPIRES),
            additional_claims=claims
        )
        
        refresh_token = create_refresh_token(
            identity=str(user_id),
            expires_delta=timedelta(days=JWTUtility.REFRESH_TOKEN_EXPIRES),
            additional_claims=claims
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': JWTUtility.ACCESS_TOKEN_EXPIRES * 3600  # seconds
        }
    
    @staticmethod
    def create_access_token(user_id, additional_claims=None):
        """
        Create an access token for a user.
        
        Args:
            user_id (int): User ID to encode in token
            additional_claims (dict, optional): Extra claims to add
            
        Returns:
            str: JWT access token
        """
        if not user_id:
            raise ValueError("User ID is required")
        
        claims = {'user_id': int(user_id)}
        if additional_claims:
            claims.update(additional_claims)
        
        return create_access_token(
            identity=str(user_id),
            expires_delta=timedelta(hours=JWTUtility.ACCESS_TOKEN_EXPIRES),
            additional_claims=claims
        )
    
    @staticmethod
    def create_refresh_token(user_id, additional_claims=None):
        """
        Create a refresh token for a user.
        
        Args:
            user_id (int): User ID to encode in token
            additional_claims (dict, optional): Extra claims to add
            
        Returns:
            str: JWT refresh token
        """
        if not user_id:
            raise ValueError("User ID is required")
        
        claims = {'user_id': int(user_id)}
        if additional_claims:
            claims.update(additional_claims)
        
        return create_refresh_token(
            identity=str(user_id),
            expires_delta=timedelta(days=JWTUtility.REFRESH_TOKEN_EXPIRES),
            additional_claims=claims
        )
    
    @staticmethod
    def verify_token(token):
        """
        Verify and decode a JWT token.
        
        Args:
            token (str): JWT token to verify
            
        Returns:
            dict: Decoded token payload
            
        Raises:
            Exception: If token is invalid or expired
        """
        if not token:
            raise ValueError("Token is required")
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            decoded = decode_token(token)
            return decoded
        except Exception as e:
            raise ValueError(f"Invalid token: {str(e)}")
    
    @staticmethod
    def get_user_id_from_token(token):
        """
        Extract user ID from a JWT token.
        
        Args:
            token (str): JWT token
            
        Returns:
            int: User ID from token
            
        Raises:
            ValueError: If token is invalid
        """
        try:
            decoded = JWTUtility.verify_token(token)
            return decoded.get('sub') or decoded.get('user_id')
        except Exception as e:
            raise ValueError(f"Cannot extract user ID: {str(e)}")
    
    @staticmethod
    def is_token_expired(token):
        """
        Check if a token is expired.
        
        Args:
            token (str): JWT token
            
        Returns:
            bool: True if token is expired, False otherwise
        """
        try:
            decoded = JWTUtility.verify_token(token)
            exp = decoded.get('exp')
            
            if not exp:
                return True
            
            return datetime.utcfromtimestamp(exp) < datetime.utcnow()
        except:
            return True
    
    @staticmethod
    def get_token_expiry_time(token):
        """
        Get the expiration time of a token.
        
        Args:
            token (str): JWT token
            
        Returns:
            datetime: Token expiration datetime, or None if invalid
        """
        try:
            decoded = JWTUtility.verify_token(token)
            exp = decoded.get('exp')
            
            if exp:
                return datetime.utcfromtimestamp(exp)
            return None
        except:
            return None
    
    @staticmethod
    def get_time_until_expiry(token):
        """
        Get the time remaining until token expiration.
        
        Args:
            token (str): JWT token
            
        Returns:
            timedelta: Time remaining, or None if invalid/expired
        """
        try:
            expiry = JWTUtility.get_token_expiry_time(token)
            if expiry:
                remaining = expiry - datetime.utcnow()
                if remaining.total_seconds() > 0:
                    return remaining
            return None
        except:
            return None
