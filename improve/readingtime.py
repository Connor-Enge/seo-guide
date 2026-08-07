def reading_minutes(text, wpm=220):
    """Estimate reading time in whole minutes from plain text."""
    words = len(text.split())
    if words == 0:
        return 1
    minutes = round(words / float(wpm))
    return max(1, int(minutes))
