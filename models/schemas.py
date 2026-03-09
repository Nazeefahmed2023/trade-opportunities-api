from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime, timezone


class AnalysisRequest(BaseModel):
    """Request model for sector analysis."""
    sector: str = Field(..., min_length=2, max_length=100)
    
    @validator('sector')
    def validate_sector(cls, v):
        """Validate and sanitize sector name."""
        # Remove special characters and extra spaces
        cleaned = ' '.join(v.strip().split())
        if not cleaned.replace(' ', '').replace('-', '').isalnum():
            raise ValueError('Sector name must contain only letters, numbers, spaces, and hyphens')
        return cleaned


class AnalysisResponse(BaseModel):
    """Response model for sector analysis"""
    status: str = "success"
    sector: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    report: str
    session_id: str
    requests_remaining: int
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "sector": "pharmaceuticals",
                "timestamp": "2026-01-15T10:30:00Z",
                "report": "# Market Analysis Report: Pharmaceuticals\n\n...",
                "session_id": "abc123",
                "requests_remaining": 9,
                "metadata": {
                    "sources_found": 5,
                    "analysis_time": 3.2
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = "error"
    detail: str
    sector: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SessionInfo(BaseModel):
    """Session information model"""
    session_id: str
    requests_made: int
    requests_remaining: int
    reset_time: datetime
    created_at: datetime
