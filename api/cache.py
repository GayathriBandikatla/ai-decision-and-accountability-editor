"""Simple in-memory cache for analysis results."""

import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class AnalysisCache:
    """Cache for transcript analysis results."""

    def __init__(self, ttl_hours: int = 24):
        """Initialize cache with TTL (time-to-live) in hours."""
        self.cache: Dict[str, tuple[Any, datetime]] = {}
        self.ttl = timedelta(hours=ttl_hours)

    def get_key(self, transcript_text: str) -> str:
        """Generate cache key from transcript hash."""
        return hashlib.sha256(transcript_text.encode()).hexdigest()

    def get(self, transcript_text: str) -> Optional[Any]:
        """Get cached result if exists and not expired."""
        key = self.get_key(transcript_text)

        if key not in self.cache:
            return None

        result, timestamp = self.cache[key]

        # Check if expired
        if datetime.now() - timestamp > self.ttl:
            del self.cache[key]
            return None

        return result

    def set(self, transcript_text: str, result: Any) -> None:
        """Cache analysis result."""
        key = self.get_key(transcript_text)
        self.cache[key] = (result, datetime.now())

    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()

    def size(self) -> int:
        """Get cache size."""
        return len(self.cache)

# Global cache instance
analysis_cache = AnalysisCache(ttl_hours=24)
