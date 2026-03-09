from fastapi import Request, HTTPException, status
from fastapi.security import APIKeyHeader
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Dict


# API Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


class SessionManager:
    """Manage user sessions in memory."""

    def __init__(self):
        self.sessions: Dict[str, dict] = {}
    
    def create_session(self, api_key: str) -> str:
        """Create a new session for API key"""
        # Generate session ID from API key + timestamp
        session_id = hashlib.sha256(
            f"{api_key}{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:32]
        
        self.sessions[session_id] = {
            "api_key": api_key,
            "created_at": datetime.now(timezone.utc),
            "last_activity": datetime.now(timezone.utc)
        }
        
        return session_id
    
    def get_session(self, session_id: str) -> dict:
        """Get session information"""
        return self.sessions.get(session_id)
    
    def update_activity(self, session_id: str):
        """Update last activity time for session"""
        if session_id in self.sessions:
            self.sessions[session_id]["last_activity"] = datetime.now(timezone.utc)
    
    def get_or_create_session(self, api_key: str) -> str:
        """Get existing session or create new one"""
        # Look for existing session with this API key
        for session_id, session_data in self.sessions.items():
            if session_data["api_key"] == api_key:
                self.update_activity(session_id)
                return session_id
        
        # Create new session
        return self.create_session(api_key)


# Global session manager
session_manager = SessionManager()


async def verify_api_key(request: Request, api_key: str = None) -> str:
    """
    Verify API key and return session ID
    
    Args:
        request: FastAPI request object
        api_key: API key from header
        
    Returns:
        Session ID
        
    Raises:
        HTTPException: If API key is invalid
    """
    from config import get_settings
    settings = get_settings()
    
    # Get API key from header
    if api_key is None:
        api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Please provide X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # Verify API key
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key. Please check your credentials.",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # Get or create session
    session_id = session_manager.get_or_create_session(api_key)
    
    return session_id
