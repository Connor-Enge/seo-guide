import re

def redundant_title_segment(title_text):
    """Detect an SEO 'redundant title' — a page <title> whose visible segments repeat."""
    if not title_text or not title_text.strip():
        return None
    
    separators = r'\s+[\u2014\u2013\u00B7|\-]\s+'
    segments = re.split(separators, title_text)
    segs = [s.strip() for s in segments if s.strip()]
    
    if len(segs) < 2:
        return None
    
    seen = set()
    for segment in segs:
        lower_segment = segment.lower()
        if lower_segment in seen:
            return segment
        seen.add(lower_segment)
    
    return None
