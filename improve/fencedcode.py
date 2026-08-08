import html

FENCE = chr(96) * 3

def consume_fence(lines, i):
    head = lines[i].rstrip()
    if not head.startswith(FENCE):
        return None
    lang = head[3:].strip()
    if lang and any(c for c in lang if not (c.isalnum() or c in "+#._-;")):
        return None
    k = i + 1
    while k < len(lines) and lines[k].rstrip() != FENCE:
        k += 1
    if k == len(lines):
        return None
    inner = lines[i+1:k]
    body = '\n'.join(html.escape(s, quote=False) for s in inner)
    open_tag = '<pre' + (' data-lang="' + lang + '"' if lang else '') + '><code' + (' class="language-' + lang + '"' if lang else '') + '>'
    return (open_tag + body + '</code></pre>', k + 1)
