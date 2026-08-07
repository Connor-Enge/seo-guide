"""
Module for reading-length metadata in JSON-LD.
"""

def iso8601_duration(minutes) -> str:
    """Convert an integer number of minutes to an ISO-8601 duration string."""
    return f"PT{max(1, int(minutes))}M"

def word_count(text) -> int:
    """Count whitespace-separated word tokens in plain text."""
    return len(text.split())
