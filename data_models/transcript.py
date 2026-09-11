"""Transcript data models."""

from pydantic import BaseModel
from typing import List


class Speaker(BaseModel):
    """Meeting participant."""

    id: str
    name: str


class Segment(BaseModel):
    """Single speech segment from a meeting."""

    timestamp: str
    speaker_id: str
    speaker_name: str
    text: str


class Transcript(BaseModel):
    """Complete meeting transcript."""

    meeting_id: str
    duration_minutes: float
    speakers: List[Speaker]
    segments: List[Segment]
