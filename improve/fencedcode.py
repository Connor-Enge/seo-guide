import html

FENCE = chr(96) * 3   # three backtick characters

def consume_fence(lines, i):
    head = lines[i].rstrip()
    if not head.startswith(FENCE):
        return None
    lang = head[3:].strip()
    if lang and not all(c.isalnum() or c in "+#._-;" for c in lang):
        return None
    for k in range(i + 1, len(lines)):
        if lines[k].rstrip() == FENCE:
            inner = lines[i + 1:k]
            body = '\n'.join(html.escape(s, quote=False) for s in inner)
            open_tag = '<pre><code class="language-' + lang + '">' if lang else '<pre><code>'
            return (open_tag + body + '</code></pre>', k + 1)
    return None
