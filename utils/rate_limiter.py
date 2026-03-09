from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
import time


class RateLimiter:
    """In-memory rate limiter using token bucket algorithm."""

    def __init__(self, max_requests: int, time_window: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, list] = {}  # session_id -> list of timestamps
        
    def is_allowed(self, session_id: str) -> tuple[bool, int, Optional[datetime]]:
        """
        Check if request is allowed for session
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Tuple of (is_allowed, requests_remaining, reset_time)
        """
        current_time = time.time()
        
        # Initialize session if not exists
        if session_id not in self.requests:
            self.requests[session_id] = []
        
        # Remove old requests outside time window
        cutoff_time = current_time - self.time_window
        self.requests[session_id] = [
            req_time for req_time in self.requests[session_id]
            if req_time > cutoff_time
        ]
        
        # Check if limit exceeded
        if len(self.requests[session_id]) >= self.max_requests:
            # Calculate reset time
            oldest_request = min(self.requests[session_id])
            reset_timestamp = oldest_request + self.time_window
            reset_time = datetime.fromtimestamp(reset_timestamp, tz=timezone.utc)
            
            return False, 0, reset_time
        
        # Add current request
        self.requests[session_id].append(current_time)
        
        requests_remaining = self.max_requests - len(self.requests[session_id])
        
        # Calculate next reset time
        if self.requests[session_id]:
            oldest_request = min(self.requests[session_id])
            reset_timestamp = oldest_request + self.time_window
            reset_time = datetime.fromtimestamp(reset_timestamp)
        else:
            reset_time = datetime.now(timezone.utc) + timedelta(seconds=self.time_window)
        
        return True, requests_remaining, reset_time
    
    def get_session_info(self, session_id: str) -> Dict:
        """
        Get session rate limit information
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with session info
        """
        current_time = time.time()
        
        if session_id not in self.requests:
            return {
                "requests_made": 0,
                "requests_remaining": self.max_requests,
                "reset_time": datetime.now(timezone.utc) + timedelta(seconds=self.time_window)
            }
        
        # Clean old requests
        cutoff_time = current_time - self.time_window
        valid_requests = [
            req_time for req_time in self.requests[session_id]
            if req_time > cutoff_time
        ]
        
        requests_made = len(valid_requests)
        requests_remaining = max(0, self.max_requests - requests_made)
        
        if valid_requests:
            oldest_request = min(valid_requests)
            reset_timestamp = oldest_request + self.time_window
            reset_time = datetime.fromtimestamp(reset_timestamp, tz=timezone.utc)
        else:
            reset_time = datetime.now(timezone.utc) + timedelta(seconds=self.time_window)
        
        return {
            "requests_made": requests_made,
            "requests_remaining": requests_remaining,
            "reset_time": reset_time
        }
    
    def reset_session(self, session_id: str):
        """Reset rate limit for a session"""
        if session_id in self.requests:
            del self.requests[session_id]
