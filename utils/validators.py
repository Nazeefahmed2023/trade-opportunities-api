import re
from typing import Optional


def sanitize_sector_name(sector: str) -> str:
    """
    Sanitize and validate sector name.

    Args:
        sector: Raw sector name

    Returns:
        Cleaned sector name

    Raises:
        ValueError: If sector name is invalid
    """
    if not sector:
        raise ValueError("Sector name cannot be empty")
    
    # Remove extra whitespace
    cleaned = ' '.join(sector.strip().split())
    
    # Check length
    if len(cleaned) < 2:
        raise ValueError("Sector name must be at least 2 characters")
    
    if len(cleaned) > 100:
        raise ValueError("Sector name must be less than 100 characters")
    
    # Allow letters, numbers, spaces, and hyphens
    if not re.match(r'^[a-zA-Z0-9\s\-]+$', cleaned):
        raise ValueError("Sector name must contain only letters, numbers, spaces, and hyphens")
    
    return cleaned


def validate_api_key(api_key: Optional[str]) -> bool:
    """
    Validate API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False
    
    # Basic validation: should be at least 8 characters
    if len(api_key) < 8:
        return False
    
    return True


def format_sector_for_search(sector: str) -> str:
    """
    Format sector name for search queries
    
    Args:
        sector: Cleaned sector name
        
    Returns:
        Formatted search query
    """
    # Add context for better search results
    return f"{sector} sector India market analysis news trends 2026"


def truncate_text(text: str, max_length: int = 10000) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."
