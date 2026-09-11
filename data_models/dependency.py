"""Dependency data model."""

from pydantic import BaseModel, Field


class Dependency(BaseModel):
    """Relationship between decisions and action items."""

    source_id: str = Field(..., description="Decision or action item ID")
    target_id: str = Field(..., description="Decision or action item ID")
    relationship: str = Field(
        ...,
        description="Type: blocks, depends_on, conflicts_with, enables",
    )
    confidence: float = Field(..., ge=0, le=1, description="Confidence score 0-1")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "source_id": "dec_001",
                "target_id": "action_002",
                "relationship": "enables",
                "confidence": 0.85,
            }
        }
